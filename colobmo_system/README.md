# Colombo System

Colombo is an autoresearch system for Oracle Complexity. Brain fixes the Setting, assigns Tasks to Cells, maintains a Live Complexity Bracket, and integrates results into a self-contained proof and report. Independent Verifiers review Cell results and the final adopted proof.

The release directory is named `colobmo_system`. The independent `colombo_memory_agent` is included as a subdirectory. Previous research runs, credentials, virtual environments, model transcripts, and workstation configuration are excluded.

## Layout

```text
colobmo_system/
  agents/                     # Brain, Cell, Experiment, Verifier, Lean, Writing instructions
  src/colombo/                # System implementation
  colombo_memory_agent/       # Independent Curator/Reviewer and publication tools
  long_term_memory/           # Four scientific libraries
  .long_term_memory_state/    # Required indexes, pinned scientific objects, review commitments
  config.toml                # Brain/Cell configuration
  downstream.toml            # Separate Lean/Writing configuration
  tests/                     # Offline regression tests
  scripts/run_validation.py  # Offline Brain/Cell test runner
  run.py                     # Brain command line
  run_cell.py                # Standalone Cell command line
  run_pipeline.py            # Optional independent Lean/Writing pipeline
```

See [source responsibilities](SOURCE_LAYOUT.md), [Memory usage](docs/MEMORY.md), and [downstream Agents](docs/DOWNSTREAM.md).

## Setup

Use Python 3.11 or newer. Run commands from `colobmo_system/` unless otherwise stated:

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r colombo_memory_agent/requirements.txt
```

Native research Agents require a working, authenticated Codex CLI. Configure its authentication and model access in your own environment. External search and hosted experiments use environment variables:

```sh
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
export SERPER_API_KEY='YOUR_SERPER_API_KEY'
export JINA_API_KEY='YOUR_JINA_API_KEY'
```

These are placeholders. Set only the services you use, and keep real credentials outside the repository. The hosted Experiment API is separate from the native CLI login.

## Run a research task

Create a goal file containing the mathematical Setting, Oracle model, target guarantee, parameter domain, and relevant materials. Preview and preparation do not launch a model:

```sh
python run.py config
python run.py run path/to/goal.md --run-dir runs/example --prepare-only
```

Start research in a new or empty run directory:

```sh
python run.py run path/to/goal.md --run-dir runs/research
python run.py status --run-dir runs/research
python run.py resume --run-dir runs/research
```

`status` rebuilds exported views; it is not strictly read-only. Supply additional files with `--material` and requirements with `--criterion`. Original input files are retained in the run.

Standalone Cell:

```sh
python run_cell.py path/to/goal.md --run-dir runs/cell
python run_cell.py --run-dir runs/cell --resume
```

See [Cell usage](agents/cell/README.md) and [Experiment Cell usage](agents/experiment_cell/README.md).

## Configuration and workflow

`config.toml` is the sole Brain/Cell configuration. Its selected default profile is `hard`; set the first line to `profile = "standard"` for the smaller preset. `--config` selects a complete replacement file without merging overlays.

| Allocation | Hard | Standard |
| --- | ---: | ---: |
| Waves | 8 | 3 |
| Dispatches per Wave | 6 | 3 |
| Concurrent outer Cells | 4 | 2 |
| Final integration and review timeout, seconds | 7200 | 7200 |

Research has no run-wide deadline. Cell starts, reviews, Challenges, Subcells, Experiments, artifact sizes, and infrastructure operations retain their respective configured limits. Usage is cumulative across resume; an unknown external request must not be repeated automatically.

```text
plan -> Cells -> Result Verifier -> update/prune
     -> further research within the remaining Wave allocation
     -> integrate -> final Verifier -> report
```

Tasks have fixed scopes and self-contained input packages. Result review is tied to the exact Task attempt; final review is tied to the exact adopted ProofDraft. Pruning requires reviewed premises and a matching relation audit. Empirical results may guide research but do not certify mathematical Bounds.

`completed` requires explicit final approval of the current goal, matching pinned evidence, and checked proof steps. Open research questions outside the certified goal remain visible. Ending a workflow, a partial review, or a mismatched proof version does not establish completion. An ended run affected by stale completion metadata can be reconciled without new model calls:

```sh
python run.py reconcile-final-review --run-dir runs/example
```

Reconciliation appends corrective progress/conclusion records after validating the original bindings. It preserves the proof, open questions, original reviews, historical conclusions, and usage counters. Replaying the command is idempotent.

## Records and reports

SQLite is authoritative; JSON and Markdown are rebuildable exports. Models use formal MCP tools rather than editing SQL or authoritative exports.

| Run path | Contents |
| --- | --- |
| `input/` | Original goal, copied materials, pinned Setting |
| `research.json` | GoalProgress, Tasks, Waves, reviews, and audits |
| `proof_draft.json` | Adopted proof versions and final review |
| `working_notes.json` | Optional research notes |
| `proof/current.md` | Current adopted proof |
| `output/final.md` | Final report and certification status |

## Scientific Memory

The bundled privacy-projected library contains 388 published records and 43 leads. Keep `long_term_memory/` and `.long_term_memory_state/` together. Scientific identifiers use stable names without local snapshot suffixes. Source versions, material hashes, scientific references, and original review/publication hash commitments are preserved. A privacy projection is not a new independent review; see [review identity and privacy](docs/MEMORY_PRIVACY_PUBLICATION.md).

Brain and proof Cells have read-only `scientific_memory`. Verifier, Recovery, and Experiment have no live Memory reader. The nested [Memory Agent](colombo_memory_agent/README.md) performs independent Curator/Reviewer jobs and explicitly authorized publication; the proof scheduler does not launch it.

## Optional Lean and Writing

`run_pipeline.py` consumes exported research through a separate file handoff. Lean and Writing have separate instructions, configuration, outputs, and acceptance gates. They do not modify Brain/Cell records. Provision a pinned Lean project in `downstream.toml` before use. Research completion alone does not guarantee downstream acceptance. See [downstream requirements](docs/DOWNSTREAM.md).

## Offline tests

```sh
python -B scripts/run_validation.py --suite brain
python -B scripts/run_validation.py --suite cell
python -B -m unittest discover -s tests/memory
python -B -m unittest discover -s tests/downstream
python -B -m unittest discover -s colombo_memory_agent/tests
```

The suites use simulated model/API backends and local workers. They do not launch paid research by default. Compiler-dependent tests may skip when a suitable Lean environment is unavailable. Generated test output is excluded from version control.

Product branding is unversioned. Instruction, workflow, storage, and scientific schema versions remain in data contracts for compatibility; literature versions and immutable review identifiers retain their original meanings.
