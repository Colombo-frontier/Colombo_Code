"""One-way file pipeline. Optional Brain execution stays behind its existing CLI."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tomllib

from colombo.downstream.handoff import digest, from_brain_run, validate_package
from colombo.downstream.model import NativeModel
from colombo.lean_agent.evidence import validate_lean_result
from colombo.shared.file_io import atomic_write, json_bytes

PROJECT = Path(__file__).resolve().parents[3]


def load_config(path=None):
    config = tomllib.loads(Path(path or PROJECT/'downstream.toml').read_text(encoding='utf-8-sig'))
    if set(config) != {'enabled','writing_enabled','lean','writing','model'}:
        raise ValueError('Use a complete independent downstream configuration')
    if type(config['enabled']) is not bool or type(config['writing_enabled']) is not bool:
        raise ValueError('Feature switches must be booleans')
    if set(config['lean']) != {'lean_project','lake_bin','max_compile_attempts','compile_timeout_seconds','timeout_seconds'}:
        raise ValueError('Unexpected Lean configuration')
    if set(config['writing']) != {'timeout_seconds'}:
        raise ValueError('Unexpected writing configuration')
    if set(config['model']) != {'codex_bin','auth_home','model','reasoning_effort','search_enabled'}:
        raise ValueError('Unexpected independent model configuration')
    for section, names in [('lean',['max_compile_attempts','compile_timeout_seconds','timeout_seconds']),('writing',['timeout_seconds'])]:
        for name in names:
            if type(config[section][name]) is not int or config[section][name] <= 0:
                raise ValueError(f'{section}.{name} must be positive integer')
    for section, names in [('lean',['lean_project','lake_bin']),('model',['codex_bin','auth_home','model','reasoning_effort'])]:
        if any(not isinstance(config[section][name],str) for name in names):
            raise ValueError('Paths/model selections must be strings')
    if type(config['model']['search_enabled']) is not bool:
        raise ValueError('model.search_enabled must be boolean')
    if config['lean']['lean_project'] and not Path(config['lean']['lean_project']).is_absolute():
        raise ValueError('lean_project must be an absolute path')
    return config


def run(package, output_dir, config, *, lean_model=None, writing_model=None, stage='all', lean_result=None):
    if stage not in {'all','lean','writing'}:
        raise ValueError('Unknown downstream stage')
    if not config['enabled'] or stage == 'writing' and not config['writing_enabled']:
        return {'status':'disabled'}
    validate_package(package)
    output = Path(output_dir).resolve(); output.mkdir(parents=True, exist_ok=True)
    lock = output/'.pipeline.lock'
    with lock.open('x') as f:
        f.write('Pipeline active; inspect prior process before clearing a stale lock.\n')
    try:
        binding = {'package_sha256':digest(package),'config_sha256':digest(config)}
        if (output/'binding.json').exists():
            if json.loads((output/'binding.json').read_text()) != binding:
                raise ValueError('Use a separate output directory for changed inputs/configuration')
        else:
            if any(p.name != '.pipeline.lock' for p in output.iterdir()):
                raise ValueError('Output directory must be new or have a matching pipeline binding')
            atomic_write(output/'binding.json',json_bytes(binding))
        atomic_write(output/'handoff.json',json_bytes(package))
        if stage != 'writing':
            from colombo.lean_agent.agent import run as run_lean
            lean_result = run_lean(package,output/'lean',config['lean'],lean_model or NativeModel(PROJECT,'lean',config['model']))
        elif not isinstance(lean_result,dict):
            raise ValueError('Writing-only invocation requires a Lean result')
        if lean_result.get('status') == 'passed':
            validate_lean_result(package, lean_result)
        origin = 'imported' if stage == 'writing' else 'local_agent'
        summary = {'status':lean_result['status'],'proof_sha256':package['proof_sha256'],
            'lean_status':lean_result['status'],'writing_status':'skipped',
            'lean_evidence_origin':origin,
            'lean_evidence_validation': ('embedded_structure_and_bindings'
                                         if lean_result['status'] == 'passed' else 'not_passed')}
        if lean_result['status'] == 'passed' and config['writing_enabled'] and stage != 'lean':
            from colombo.writing_agent.agent import run as run_writing
            result = run_writing(package,lean_result,output/'writing',config['writing'],
                                 writing_model or NativeModel(PROJECT,'writing',config['model']),
                                 evidence_origin=origin)
            summary.update(status='completed',writing_status=result['status'])
        atomic_write(output/'pipeline.json',json_bytes(summary))
        return summary
    except Exception as exc:
        atomic_write(output/'pipeline-error.json',json_bytes({'status':'stopped','error_type':type(exc).__name__,'message':str(exc)}))
        raise
    finally:
        lock.unlink(missing_ok=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Independent Brain-output -> Lean Agent -> Writing Agent launcher')
    parser.add_argument('--config',type=Path)
    parser.add_argument('--brain-run',type=Path,help='Existing Brain run, read exported files only')
    parser.add_argument('--input',type=Path,help='Previously frozen handoff.json')
    parser.add_argument('--material',action='append',type=Path,default=[],help='Selected additional draft/source text')
    parser.add_argument('--output-dir',type=Path)
    parser.add_argument('--stage',choices=['all','lean','writing'],default='all')
    parser.add_argument('--lean-result',type=Path,help='Passed standalone Lean result for writing-only invocation')
    parser.add_argument('brain_args',nargs=argparse.REMAINDER,help='Optional: -- run/resume [normal Brain CLI arguments]')
    args = parser.parse_args(argv)
    try:
        config = load_config(args.config)
        if args.brain_args:
            command = args.brain_args[1:] if args.brain_args[0] == '--' else args.brain_args
            if not command or command[0] not in {'run','resume'} or not args.brain_run:
                raise ValueError('Brain execution requires --brain-run and -- run/resume arguments')
            run_dirs = []
            for i, token in enumerate(command):
                if token == '--run-dir':
                    if i+1 >= len(command): raise ValueError('Missing Brain --run-dir value')
                    run_dirs.append(command[i+1])
                elif token.startswith('--run-dir='):
                    run_dirs.append(token.split('=',1)[1])
            if run_dirs:
                if len(run_dirs) != 1 or Path(run_dirs[0]).resolve()!=args.brain_run.resolve():
                    raise ValueError('Brain command needs one --run-dir matching --brain-run')
            else:
                command += ['--run-dir',str(args.brain_run.resolve())]
            completed = subprocess.run([sys.executable,'-B',str(PROJECT/'run.py'),*command],cwd=PROJECT)
            if completed.returncode != 0:
                return completed.returncode
        if not config['enabled']:
            print(json.dumps({'status':'disabled'})); return 0
        if bool(args.input) == bool(args.brain_run):
            raise ValueError('Provide exactly one --input or --brain-run')
        if args.input and args.material:
            raise ValueError('Materials must be frozen when preparing the Brain handoff')
        output = (args.output_dir or PROJECT/'downstream_runs'/(args.brain_run.name if args.brain_run else args.input.stem)).resolve()
        if args.brain_run:
            brain = args.brain_run.resolve()
            if output.is_relative_to(brain) or brain.is_relative_to(output):
                raise ValueError('Downstream output must be separate from the Brain run')
        if args.input and args.input.resolve().is_relative_to(output):
            # Reusing the pipeline's own frozen handoff is allowed; other input paths remain read-only.
            if args.input.resolve()!=output/'handoff.json':
                raise ValueError('Output may not contain the supplied input file')
        package = validate_package(json.loads(args.input.read_text(encoding='utf-8-sig'))) if args.input else from_brain_run(args.brain_run,args.material)
        if args.stage == 'writing' and not args.lean_result:
            raise ValueError('Writing-only invocation requires --lean-result')
        lean_input = json.loads(args.lean_result.read_text(encoding='utf-8-sig')) if args.lean_result else None
        result = run(package,output,config,stage=args.stage,lean_result=lean_input)
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0 if result['status'] in {'disabled','completed','passed','draft','draft_with_gaps'} else 2
    except Exception as exc:
        print(f'{type(exc).__name__}: {exc}',file=sys.stderr); return 2

