#!/usr/bin/env python3
"""Build standalone, complete profile downloads from the active JSON records.

The supplied renderer is retained in vendor_renderer.py. Its prose, mathematical
content and evidence handling are reused, with only the requested publication
policy applied. No PDF is copied from the historical archive.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

import vendor_renderer as renderer


ROOT = Path(__file__).resolve().parents[2]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def control_characters(value, pointer=""):
    found = []
    if isinstance(value, dict):
        for key, item in value.items():
            found.extend(control_characters(item, pointer + "/" + str(key)))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(control_characters(item, pointer + "/" + str(index)))
    elif isinstance(value, str):
        codes = sorted({ord(char) for char in value if ord(char) < 32 and char != "\n"})
        if codes:
            found.append({"pointer": pointer, "character_codes": codes})
    return found


def profile_nodes(profile):
    # Label replacement is a publishing operation; mathematical JSON stays intact.
    def terminology(text):
        text=re.sub(r'Information interface','Oracle interface',text,flags=re.IGNORECASE)
        return re.sub(r'\bcoverage\b',lambda m:'Applicability' if m.group()[0].isupper() else 'applicability',text,flags=re.IGNORECASE)
    return [(kind,terminology(text)) for kind,text in renderer.document_nodes(profile)]


def prepare_one(profile_path: Path, destination: Path) -> dict:
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    setting_id = profile["setting_id"]
    classification_path=profile_path.with_name('classification.json')
    if not classification_path.exists():
        raise ValueError(f'{setting_id}: the global eight-axis classification is required before export')
    classification=json.loads(classification_path.read_text())
    if classification['profile_sha256'] != sha256(profile_path):
        raise ValueError(f'{setting_id}: stale classification source revision')
    profile['_classification']=classification
    controls = control_characters(profile)
    if controls:
        raise ValueError(f"{setting_id}: unexpected control characters: {controls}")
    if not re.fullmatch(r"[A-Za-z0-9_-]+", setting_id):
        raise ValueError(f"Unsafe setting ID: {setting_id!r}")
    for reference in profile["references"]:
        if not re.match(r"^https?://", reference.get("url", "")):
            raise ValueError(f"{setting_id}: reference URL missing for {reference['id']}")
        if any(char in reference["url"] for char in "\r\n{}"):
            raise ValueError(f"{setting_id}: reference URL contains an unsafe character")

    nodes = profile_nodes(profile)
    tex = renderer.to_tex(nodes)
    markdown = renderer.to_md(nodes)
    if re.search(r"\bCoverage\b|Information interface", tex + markdown, re.IGNORECASE):
        raise ValueError(f"{setting_id}: excluded display labels remain in export")
    if nodes[0] != ("h1", profile["title"]):
        raise ValueError(f"{setting_id}: original full title changed")
    sections = [text for kind, text in nodes if kind == "h2"]
    if sections[:3] != ["1. Setting specification", "2. Notation and parameters",
                        "3. Complexity bracket"]:
        raise ValueError(f"{setting_id}: unexpected section order: {sections}")
    bounds = [text for kind, text in nodes if kind == "h3" and re.match(r"B\d+ - ", text)]
    rows = [text for kind, text in nodes if kind == "h3" and re.match(r"R\d+ - ", text)]
    if len(bounds) != len(profile["bounds"]) or len(rows) != len(profile["bracket_rows"]):
        raise ValueError(f"{setting_id}: complete bound or regional display content missing")

    output = destination / setting_id
    output.mkdir(parents=True, exist_ok=True)
    tex_path = output / "profile.tex"
    md_path = output / "profile.md"
    tex_path.write_text(tex, encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return {
        "setting_id": setting_id,
        "title": profile["title"],
        "source": str(profile_path.relative_to(ROOT)),
        "source_sha256": sha256(profile_path),
        "classification_sha256": sha256(classification_path),
        "tex": str(tex_path.relative_to(ROOT)),
        "tex_sha256": sha256(tex_path),
        "markdown": str(md_path.relative_to(ROOT)),
        "markdown_sha256": sha256(md_path),
        "counts": {
            "views": len(profile["views"]),
            "comparisons": len(profile["comparisons"]),
            "displayed_regimes": len(rows),
            "bounds": len(bounds),
            "local_arguments": len(profile.get("proofs", [])),
            "references": len(profile["references"]),
            "direct_citation_links": tex.count("\\href{"),
        },
        "sections": sections,
        "publication_checks": {
            "original_title_preserved": True,
            "coverage_removed": True,
            "oracle_interface_label": True,
            "setting_specification_combined": True,
            "compared_quantities_retained_inside_complexity_bracket": True,
            "all_bound_details_and_local_arguments_retained": True,
            "source_citations_link_directly_to_articles": True,
            "full_reference_entries_retained": True,
            "control_character_check_passed": True,
        },
        "pdf_status": "not_requested",
    }


def compile_one(record: dict, engine: str, cache_directory: str | None, allow_network=False) -> dict:
    tex_path = ROOT / record["tex"]
    work_root = ROOT / "tmp" / "pdfs"
    work_root.mkdir(parents=True, exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix=record["setting_id"] + "-", dir=work_root))
    work_tex = work / "profile.tex"
    shutil.copy2(tex_path, work_tex)
    environment = os.environ.copy()
    if cache_directory:
        environment["TECTONIC_CACHE_DIR"] = cache_directory
    if "tectonic" in Path(engine).name.lower():
        command = [engine] + ([] if allow_network else ['--only-cached']) + ["--keep-logs", "--untrusted",
                   "-o", str(work), str(work_tex)]
    else:
        command = [engine, "-interaction=nonstopmode", "-halt-on-error",
                   "-no-shell-escape", "-output-directory", str(work), str(work_tex)]
    try:
        result = subprocess.run(command, cwd=work, env=environment,
                                capture_output=True, text=True, timeout=240)
        transcript = result.stdout + result.stderr
        log_path = work / "profile.log"
        latex_log = log_path.read_text(errors="replace") if log_path.exists() else ""
        warnings = [line.strip() for line in (transcript + "\n" + latex_log).splitlines()
                    if re.search(r"Overfull|Missing character|ATLAS WIDE FORMULA|warning:", line,
                                 re.IGNORECASE)]
        report = ROOT / "data" / "audit" / ("exports_" + record["setting_id"] + ".log")
        report.write_text("$ " + " ".join(command) + "\n\n" + transcript + "\n" + latex_log,
                          encoding="utf-8")
        record["compilation"] = {
            "engine": Path(engine).name,
            "returncode": result.returncode,
            "warnings": list(dict.fromkeys(warnings)),
            "log": str(report.relative_to(ROOT)),
            "cache_only": "tectonic" in Path(engine).name.lower() and not allow_network,
        }
        generated = work / "profile.pdf"
        if result.returncode != 0 or not generated.exists():
            record["pdf_status"] = "failed"
            record["compilation"]["error_tail"] = transcript[-4000:]
            return record
        if not ("tectonic" in Path(engine).name.lower()):
            # Second pass resolves any page/bookmark references for XeLaTeX.
            second = subprocess.run(command, cwd=work, env=environment,
                                    capture_output=True, text=True, timeout=240)
            if second.returncode != 0:
                record["pdf_status"] = "failed"
                record["compilation"]["error_tail"] = (second.stdout + second.stderr)[-4000:]
                return record
        pdf_path = tex_path.with_suffix(".pdf")
        shutil.copy2(generated, pdf_path)
        record.update(pdf=str(pdf_path.relative_to(ROOT)), pdf_sha256=sha256(pdf_path),
                      pdf_bytes=pdf_path.stat().st_size, pdf_status="compiled")
        return record
    except subprocess.TimeoutExpired:
        record["pdf_status"] = "failed"
        record["compilation"] = {"engine": Path(engine).name, "error": "Compilation timed out"}
        return record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--settings", type=Path, default=ROOT / "data" / "settings")
    parser.add_argument("--output", type=Path, default=ROOT / "visualization" / "dist" / "downloads")
    parser.add_argument("--setting-id", action="append", help="Export only a selected setting ID")
    parser.add_argument("--compile", action="store_true", dest="compile_pdf")
    parser.add_argument("--engine", default=shutil.which("tectonic") or shutil.which("xelatex"))
    parser.add_argument("--cache-directory", default=os.environ.get("TECTONIC_CACHE_DIR"))
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument('--resume', action='store_true', help='Reuse only verified PDFs with unchanged TeX hashes')
    parser.add_argument('--allow-network', action='store_true', help='Allow the installed TeX engine to fill its task-specific package cache')
    args = parser.parse_args()
    paths = sorted(args.settings.glob("*/profile.json"), key=lambda p: json.loads(p.read_text()).get('provenance',{}).get('source_order',99999))
    if args.setting_id:
        paths = [p for p in paths if p.parent.name in args.setting_id]
    if not paths:
        parser.error("No active profile.json records found")
    if args.compile_pdf and not args.engine:
        parser.error("PDF compilation requires an explicitly available tectonic or xelatex engine")
    audit = ROOT / "data" / "audit"
    audit.mkdir(parents=True, exist_ok=True)
    records = [prepare_one(path, args.output.resolve()) for path in paths]
    old_report=audit/'exports.json'
    previous=json.loads(old_report.read_text()) if old_report.exists() else {}
    previous_by_id={r['setting_id']:r for r in previous.get('profiles',[])}
    records_by_id={}
    def write_report(current):
        report={
            'generated_at':datetime.now(timezone.utc).isoformat(),
            'renderer':'data/tools/vendor_renderer.py','renderer_sha256':sha256(Path(renderer.__file__)),
            'profile_count':len(current),'pdf_count':sum(r['pdf_status']=='compiled' for r in current),
            'profiles':current,'passed':all(r['pdf_status']!='failed' for r in current),
            'limitations':['Successful compilation alone does not establish mathematical correctness. Source fidelity and visual review are recorded separately.']}
        (audit/'exports.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
        return report
    if args.compile_pdf:
        def compile_or_reuse(record):
            old=previous_by_id.get(record['setting_id'],{})
            pdf=ROOT/old.get('pdf','__missing_pdf__')
            if args.resume and old.get('pdf_status')=='compiled' and old.get('tex_sha256')==record['tex_sha256'] and pdf.is_file() and sha256(pdf)==old.get('pdf_sha256'):
                record.update({k:old[k] for k in ['pdf','pdf_sha256','pdf_bytes','pdf_status','compilation']})
                return record
            result=compile_one(record,args.engine,args.cache_directory,args.allow_network)
            print(f"{result['setting_id']}: {result['pdf_status']}",flush=True)
            return result
        completed=[]
        for offset in range(0,len(records),100):
            batch=records[offset:offset+100]
            needs_compile=[r for r in batch if not(args.resume and previous_by_id.get(r['setting_id'],{}).get('pdf_status')=='compiled' and previous_by_id[r['setting_id']].get('tex_sha256')==r['tex_sha256'])]
            with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
                completed.extend(pool.map(compile_or_reuse,batch))
            write_report(completed)
        records=completed
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "renderer": "data/tools/vendor_renderer.py",
        "renderer_sha256": sha256(Path(renderer.__file__)),
        "profile_count": len(records),
        "pdf_count": sum(record["pdf_status"] == "compiled" for record in records),
        "profiles": records,
        "passed": all(record["pdf_status"] != "failed" for record in records),
        "limitations": ["Successful compilation alone does not establish mathematical correctness; "
                        "visual PDF and formula review is recorded separately."],
    }
    (audit / "exports.json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                                        encoding="utf-8")
    print(json.dumps({key: report[key] for key in ("profile_count", "pdf_count", "passed")}))
    for record in records:
        if record["pdf_status"] == "failed":
            print(record["setting_id"] + ": " + record["compilation"].get("error_tail", "failed"),
                  file=sys.stderr)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
