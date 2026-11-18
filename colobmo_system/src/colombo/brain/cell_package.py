"""Build fixed self-contained Cell packages and close authorized Markdown dependencies."""
from __future__ import annotations

import json
import hashlib
import posixpath
import copy
import re
import shutil
import uuid
from colombo.shared.file_io import Path, io_path, atomic_write, json_bytes, json_equal
from colombo.brain.research_store import Store, StoreError, linked
from html.parser import HTMLParser
import os
from types import SimpleNamespace
from urllib.parse import quote, unquote, urlsplit
from colombo.brain.package_markdown import create_markdown_parser, apply_literal_spans


class PackageDependencyError(StoreError):
    """Actionable formatting/dependency feedback, without guessing author intent."""
    def __init__(self, source, destination, line, reason):
        self.details = {"kind": "package_dependency", "source": source,
                        "destination": destination, "line": line, "reason": reason}
        location = f"{source}:{line}" if line else source
        super().__init__(f"{location}: {reason}. Check whether this is a real dependency or "
                         "ambiguous Markdown formula; preserve frozen source content.")


def _dependency_refs(value):
    """Only typed dependency links, never arbitrary strings or proof step IDs."""
    singles = {"result_ref", "material_ref", "proof_ref", "source_ref", "review_ref", "comparison_review_ref"}
    plurals = {"dependency_refs", "material_refs", "source_refs"}
    if isinstance(value, dict):
        for key, item in value.items():
            if key in singles and item and isinstance(item, (str, dict)):
                if not isinstance(item, dict) or "kind" not in item:
                    yield item
            elif key in plurals and isinstance(item, list):
                for ref in item:
                    if isinstance(ref, (str, dict)) and (not isinstance(ref, dict) or "kind" not in ref):
                        yield ref
            elif isinstance(item, (dict, list)):
                yield from _dependency_refs(item)
    elif isinstance(value, list):
        for item in value:
            yield from _dependency_refs(item)


def _default_artifacts(store, ref):
    artifacts = store.artifact_entries(ref)
    if store.record_kind(ref) != "result" or store.get_meta("config", {}).get("workflow", {}).get("version", 2) < 3:
        return artifacts
    result = store.read_record(ref)
    reported = (result.get("empirical_report") or {}).get("artifact_paths", [])
    names = {"manuscript.md", "draft.md", "report.md", "empirical_report.json",
             "empirical_submission.json", "memory_snapshot.json", "problem.md"}
    return [a for a in artifacts if any(a["path"].endswith("/artifacts/" + name) for name in names)
            or any(a["path"].endswith("/artifacts/" + p) for p in reported)]


def _progress_snapshot(store, package):
    ref = store.get_meta("progress_ref")
    if not ref:
        return None
    saved = copy.deepcopy(store.read_record(ref))
    progress = saved.get("progress", saved)
    ids = package.get("regime_ids")
    if ids is None:
        return progress
    bracket = progress.get("bracket", {})
    if (not isinstance(ids, list) or any(not isinstance(r, str) for r in ids)
            or not set(ids).issubset({r["id"] for r in bracket.get("regimes", [])})):
        raise StoreError("package.regime_ids must name existing GoalProgress regimes")
    bracket["regimes"] = [r for r in bracket.get("regimes", []) if r["id"] in ids]
    bounds = {b for r in bracket["regimes"] for b in r["lower_bound_ids"] + r["upper_bound_ids"]}
    bracket["bounds"] = [b for b in bracket.get("bounds", []) if b["id"] in bounds]
    if bounds != {b["id"] for b in bracket["bounds"]}:
        raise StoreError("Bracket snapshot refers to a missing Bound")
    return {"bracket": bracket, "source_progress_ref": ref}


def _verify_existing(destination, request):
    if linked(destination) or not destination.is_dir():
        raise StoreError("Package destination must be an ordinary directory")
    path = destination / "manifest.json"
    if linked(path) or not path.is_file():
        raise StoreError("Existing package is incomplete")
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if not json_equal(manifest.get("request"), request):
        raise StoreError("Frozen package belongs to a different task input")
    expected = {"manifest.json"}
    for item in manifest.get("files", []):
        rel = Path(item["path"])
        if rel.is_absolute() or rel.drive or ".." in rel.parts:
            raise StoreError("Package manifest path escapes destination")
        current = destination
        for part in rel.parts:
            current /= part
            if linked(current):
                raise StoreError("Package contains linked paths")
        if not current.is_file():
            raise StoreError("Frozen package file is missing")
        if item.get("sha256") and hashlib.sha256(current.read_bytes()).hexdigest() != item["sha256"]:
            raise StoreError("Frozen package content differs")
        expected.add(rel.as_posix())
    actual = set()
    for item in destination.rglob("*"):
        if linked(item):
            raise StoreError("Package contains linked paths")
        if item.is_file():
            actual.add(item.relative_to(destination).as_posix())
    if actual != expected:
        raise StoreError("Package contains unexpected or missing files")
    return manifest


def _select_sources(store, package):
    if not isinstance(package, dict) or not isinstance(package.get("items"), list):
        raise StoreError("Task requires explicit package.items")
    for key in ("background", "selection_reason"):
        if not isinstance(package.get(key), str):
            raise StoreError(f"Package requires {key}")
    if not package["selection_reason"].strip():
        raise StoreError("Package selection_reason must explain the material selection")
    # Resolve source refs even on replay: a deleted or altered source is explicit.
    selected = []
    seen = set()
    for item in package["items"]:
        if not isinstance(item, dict) or item.get("importance") not in {"required", "reference"}:
            raise StoreError("Package item requires required/reference importance")
        if not isinstance(item.get("purpose"), str) or not item["purpose"].strip():
            raise StoreError("Package item must explain its purpose")
        if not isinstance(item.get("limitations"), str):
            raise StoreError("Package item requires limitations (empty text if none)")
        ref = store.record_ref(item.get("ref"))
        if ref["id"] in seen:
            raise StoreError("Duplicate material reference in one package")
        seen.add(ref["id"])
        payload = store.public_read(ref)
        artifacts = store.artifact_entries(ref)
        paths = item.get("artifact_paths")
        if paths is not None:
            if (not isinstance(paths, list) or any(not isinstance(p, str) for p in paths)
                    or not set(paths).issubset({a["path"] for a in artifacts})):
                raise StoreError("Selected artifact_paths must be authorized by the material record")
            artifacts = [a for a in artifacts if a["path"] in paths]
        else:
            artifacts = _default_artifacts(store, ref)
        selected.append((item, ref, payload, artifacts))
    return selected, seen


def _prepare_sources(store, package, selected, seen):
    progress = _progress_snapshot(store, package)
    if progress:
        for dependency in _dependency_refs(progress.get("bracket", {})):
            ref = store.record_ref(dependency)
            if ref["id"] not in seen:
                seen.add(ref["id"])
                selected.append(({"importance": "required", "purpose": "Evidence for the supplied Bracket scope",
                    "limitations": "Use only within the recorded reviewed scope"}, ref,
                    store.public_read(ref), _default_artifacts(store, ref)))
    # Include fixed locally referenced premises recursively. These are explicit
    # scientific dependencies, not every historical Result or sibling workspace.
    index = 0
    while index < len(selected):
        parent_item, parent_ref, payload, _ = selected[index]
        index += 1
        for dependency in _dependency_refs(payload):
            ref = store.record_ref(dependency)
            if ref["id"] in seen:
                continue
            seen.add(ref["id"])
            selected.append(({"importance": "required", "purpose": f"Local dependency of {parent_ref['id']}",
                              "limitations": "Preserves original evidence status"}, ref,
                             store.public_read(ref), _default_artifacts(store, ref)))
    authorized = {a["path"]: a for _, ref, _, _ in selected for a in store.artifact_entries(ref)}
    prepared_markdown = {}
    formatting = read_package_formatting(store)
    repairs = {}
    # Preserve relative Markdown dependencies, rather than flattening files and
    # leaving links back into the producer's directory. Only authorized material
    # dependencies are copied; a missing local dependency must be supplied.
    for _, _, _, artifacts in selected:
        present = {a["path"] for a in artifacts}
        index = 0
        while index < len(artifacts):
            artifact = artifacts[index]
            index += 1
            if Path(artifact["path"]).suffix.lower() not in {".md", ".markdown"}:
                continue
            raw = store.safe_path(artifact["path"], exists=True).read_bytes()
            body = raw.decode("utf-8-sig")
            repair = formatting.get(artifact["path"])
            if repair is not None:
                digest = hashlib.sha256(raw).hexdigest()
                if repair.get("source_sha256") != digest:
                    raise StoreError(f"Package formatting source hash mismatch: {artifact['path']}")
                try:
                    body, spans = apply_literal_spans(body, repair)
                except ValueError as exc:
                    raise StoreError(f"Invalid package formatting for {artifact['path']}: {exc}") from exc
                repairs[artifact["path"]] = {"source_sha256": digest,
                    "reason": repair["reason"], "literal_spans": spans}
            text, dependencies = resolve_markdown(store.root, artifact["path"], body, authorized)
            prepared_markdown[artifact["path"]] = text.encode("utf-8")
            if repair is not None:
                repairs[artifact["path"]]["output_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
            for relative in sorted(dependencies):
                if relative not in present:
                    artifacts.append(dict(authorized[relative]))
                    present.add(relative)
    return progress, prepared_markdown, repairs


def read_package_formatting(store):
    path = store.safe_path("runtime/package_formatting.json")
    if not path.exists():
        return {}
    value = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(value, dict) or value.get("schema_version") != 1 or not isinstance(value.get("artifacts"), dict):
        raise StoreError("Invalid package formatting manifest")
    if any(not isinstance(entry, dict) for entry in value["artifacts"].values()):
        raise StoreError("Invalid package formatting entry")
    return value["artifacts"]


def register_literal_formatting(store, ref, path, literal_text, reason, *, actor):
    """Quote one explicitly reviewed literal in future package copies only."""
    from colombo.shared.file_io import file_lock
    if store.record_kind(ref) not in {"result", "material"}:
        raise StoreError("Formatting requires a returned Result or fixed material")
    if path not in {a["path"] for a in store.artifact_entries(ref)}:
        raise StoreError("Formatting source is not authorized by this record")
    if Path(path).suffix.lower() not in {".md", ".markdown"}:
        raise StoreError("Formatting source must be Markdown")
    raw = store.safe_path(path, exists=True).read_bytes()
    body = raw.decode("utf-8-sig")
    if not isinstance(literal_text, str) or not literal_text or body.count(literal_text) != 1:
        raise StoreError("Supply a unique exact literal expression from the source")
    start = body.index(literal_text)
    span = {"start": start, "end": start + len(literal_text), "expected": literal_text}
    digest = hashlib.sha256(raw).hexdigest()
    with file_lock(store.safe_path("runtime/package_formatting.lock")):
        artifacts = read_package_formatting(store)
        prior = artifacts.get(path)
        if prior and prior.get("source_sha256") != digest:
            raise StoreError("Package formatting source hash mismatch")
        spans = [{**item, "reason": item.get("reason", prior["reason"])}
                 for item in prior.get("literal_spans", [])] if prior else []
        if not any(all(item.get(key) == value for key, value in span.items()) for item in spans):
            spans.append({**span, "reason": reason})
        spans.sort(key=lambda item: item["start"])
        entry = {"source_sha256": digest, "reason": reason, "literal_spans": spans,
                 "source_ref": store.record_ref(ref), "actor": actor}
        try:
            _, audit = apply_literal_spans(body, entry)
        except ValueError as exc:
            raise StoreError(str(exc)) from exc
        artifacts[path] = entry
        # The append-only event preserves who classified the literal and why.
        store.event("package_literal_formatting", source=path, source_sha256=digest,
                    source_ref=entry["source_ref"], literal_span=span, reason=reason, actor=actor)
        atomic_write(store.safe_path("runtime/package_formatting.json"),
                     json_bytes({"schema_version": 1, "artifacts": artifacts}))
    return {"source": path, "source_sha256": digest, "literal_spans": audit,
            "applies_to": "unpublished_package_copies", "original_unchanged": True}


def preflight_package(store, task_spec):
    """Read-only check using the same closure/formatting rules as publication."""
    package = task_spec.get("package")
    selected, seen = _select_sources(store, package)
    _prepare_sources(store, package, selected, seen)
    return {"source_count": len(selected), "artifact_count": sum(len(row[3]) for row in selected)}


def build_package(store: Store, task_id: str, task_spec: dict, destination: Path) -> dict:
    """Publish complete fixed inputs; replay never changes an existing package."""
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_.\-]{1,120}", task_id):
        raise StoreError("Invalid task id")
    package = task_spec.get("package")
    raw = Path(destination).absolute()
    if not raw.is_relative_to(store.root):
        raise StoreError("Package destination must be inside this run")
    destination = store.safe_path(raw.relative_to(store.root))
    request = {"task_id": task_id, "package": package}
    selected, seen = _select_sources(store, package)
    published = _verify_existing(destination, request) if destination.exists() else None
    if published:
        return published
    progress, prepared_markdown, repairs = _prepare_sources(store, package, selected, seen)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = destination.parent / (".p-" + uuid.uuid4().hex[:12])
    stage.mkdir()
    files, items = [], []

    def put(relative, data, source_ref=None):
        atomic_write(stage / relative, data)
        entry = {"path": relative, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}
        if source_ref is not None:
            entry["source_ref"] = source_ref
        files.append(entry)

    try:
        readme = [f"# Context package for {task_id}", "", package["background"], "",
                  "## Material selection", package["selection_reason"], "",
                  "These files are frozen inputs. Record bodies preserve original review status.",
                  "Original source paths are provenance only. Read the package copies; do not read other Task workspaces.",
                  "Brain's purpose/limitations are application guidance, not new certification.", ""]
        setting = store.root / "input/setting.json"
        if setting.is_file():
            put("setting.json", setting.read_bytes())
            readme.append("Fixed Setting Specification: setting.json")
        if progress:
            put("bracket_snapshot.json", json_bytes(progress))
            readme.append("GoalProgress snapshot at assignment: bracket_snapshot.json")
        if not selected:
            readme.append("No additional materials were selected. Use the task statement and supplied background.")
        for index, (item, ref, payload, artifacts) in enumerate(selected, 1):
            prefix = f"m/{index:03d}"
            record_path = prefix + "/record.json"
            # Export the selected fixed node, not a summary or a second record
            # store. Files in this package are delivery snapshots only.
            record_data = json_bytes(payload)
            put(record_path, record_data, ref)
            copies = []
            for number, artifact in enumerate(artifacts, 1):
                source = store.safe_path(artifact["path"], exists=True)
                original = source.read_bytes()
                data = prepared_markdown.get(artifact["path"], original)
                relative = prefix + "/f/" + Path(artifact["path"]).as_posix()
                put(relative, data, ref)
                copies.append({"source_path": artifact["path"], "package_path": relative,
                               "size": len(data), "source_sha256": hashlib.sha256(original).hexdigest(),
                               "local_links_rewritten": data != original})
                if artifact["path"] in repairs:
                    copies[-1]["formatting_repair"] = repairs[artifact["path"]]
            items.append({"source_ref": ref, "importance": item["importance"],
                          "purpose": item["purpose"], "limitations": item["limitations"],
                          "record_path": record_path, "artifacts": copies})
            readme.extend([f"## {index}. {item['importance']} — {ref['id']}",
                           f"Purpose: {item['purpose']}", f"Limitations: {item['limitations'] or 'None specified'}",
                           f"Original record: {record_path}",
                           *[f"- Material: {copy['package_path']}" for copy in copies], ""])
        put("README.md", "\n".join(readme).encode("utf-8"))
        manifest = {"schema_version": 2, "package_id": f"PKG-{task_id}",
                    "task_id": task_id, "request": request,
                    "background": package["background"], "selection_reason": package["selection_reason"],
                    "items": items, "files": files}
        atomic_write(stage / "manifest.json", json_bytes(manifest))
        # Destination is published only after all selected inputs are present.
        if destination.exists():
            existing = _verify_existing(destination, request)
            if json_bytes(existing) != json_bytes(manifest):
                raise StoreError("Frozen package manifest differs from its selected source materials")
            return existing
        stage.rename(destination)
        return manifest
    finally:
        if stage.exists() and stage.parent == destination.parent and stage.name.startswith(".p-"):
            shutil.rmtree(io_path(stage))


REMOTE_SCHEMES = {"http", "https", "mailto", "doi", "arxiv", "ftp", "ftps"}


def _local_target(root, source, href, authorized):
    decoded = unquote(href)
    if not decoded or decoded.startswith("#"):
        return None
    # A Windows drive is a local path, not a one-letter URL scheme.
    drive = re.match(r"^[A-Za-z]:", decoded)
    if drive:
        if len(decoded) < 3 or decoded[2] not in "/\\":
            raise StoreError("Drive-relative local links are ambiguous; use a frozen relative artifact path")
        path_text, _, fragment = decoded.partition("#")
        path_text, _, query = path_text.partition("?")
        absolute = True
    else:
        parsed = urlsplit(decoded.replace("\\", "/"))
        if parsed.scheme.lower() in REMOTE_SCHEMES:
            return None
        if parsed.scheme and parsed.scheme.lower() != "file":
            raise StoreError(f"Unsupported material link scheme: {parsed.scheme}")
        path_text, query, fragment = parsed.path, parsed.query, parsed.fragment
        if parsed.scheme.lower() == "file":
            if parsed.netloc and parsed.netloc.lower() != "localhost":
                path_text = "//" + parsed.netloc + path_text
            elif re.match(r"^/[A-Za-z]:/", path_text):
                path_text = path_text[1:]
            absolute = True
        elif parsed.netloc:
            # Protocol-relative notation is ambiguous with UNC paths. External
            # references must state their scheme; never treat UNC as a web URL.
            path_text = "//" + parsed.netloc + path_text
            absolute = True
        else:
            absolute = path_text.startswith("/") or bool(re.match(r"^[A-Za-z]:", path_text))
    path_text = path_text.replace("\\", "/")
    if "\x00" in path_text or not path_text:
        raise StoreError("Invalid local material link")
    if absolute:
        # Match only known paths, without probing arbitrary drives or network
        # shares. Authorization refers to the saved artifact, never live data.
        normalize = lambda value: os.path.normcase(posixpath.normpath(value)).replace("\\", "/")
        lookup = {normalize(str(root / key).replace("\\", "/")): key
                  for key in authorized}
        relative = lookup.get(normalize(path_text))
    else:
        relative = posixpath.normpath(posixpath.join(posixpath.dirname(source), path_text))
    if relative not in authorized:
        raise StoreError(f"Self-contained package is missing local dependency: {path_text}")
    target = quote(posixpath.relpath(relative, posixpath.dirname(source)), safe="/-._~")
    if query:
        target += "?" + quote(query, safe="=&-._~%")
    if fragment:
        target += "#" + quote(fragment, safe="-._~%")
    return relative, target, absolute or "\\" in decoded


class _HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and key.lower() in {"href", "src", "poster", "data"}:
                self.links.append(value)
            if value and key.lower() == "srcset":
                # An explicit failure is safer than declaring a closure check
                # complete without parsing the separate srcset grammar.
                raise StoreError("Material srcset needs an explicit self-contained attachment bundle")


def resolve_markdown(root, source, body, authorized):
    """Return (complete copied Markdown, required artifact paths).

    For relocatable absolute links the exact original destination is rewritten.
    Ambiguous source edits are rejected rather than altering mathematical text.
    """
    parser = create_markdown_parser()
    parser.validateLink = lambda value: True  # Discover file: links too; do not render them.
    captured = []
    helpers = SimpleNamespace(**vars(parser.helpers))
    parse_destination = helpers.parseLinkDestination
    normalized_body = body.replace("\r\n", "\n").replace("\r", "\n")

    def capture(text, start, maximum):
        result = parse_destination(text, start, maximum)
        if result.ok:
            context_offset = normalized_body.find(text)
            line = (normalized_body.count("\n", 0, context_offset) + text.count("\n", 0, start) + 1
                    if context_offset >= 0 and normalized_body.count(text) == 1 else None)
            captured.append((parser.normalizeLink(result.str), text[start:result.pos], line))
        return result

    helpers.parseLinkDestination = capture
    parser.helpers = helpers
    env = {}
    tokens = parser.parse(body, env)
    links, html = [], []

    def visit(rows):
        for token in rows:
            if token.type == "link_open":
                links.append(token.attrGet("href"))
            elif token.type == "image":
                links.append(token.attrGet("src"))
            elif token.type in {"html_inline", "html_block"}:
                html.append(token.content)
            if token.children:
                visit(token.children)

    visit(tokens)
    links.extend(ref["href"] for ref in env.get("references", {}).values())
    links.extend(ref["href"] for ref in env.get("duplicate_refs", []))
    dependencies, replacements = set(), {}
    for href in dict.fromkeys(links):
        try:
            resolved = _local_target(Path(root), source, href, authorized)
        except StoreError as exc:
            line = next((line for normalized, raw, line in captured if normalized == href and line), None)
            raise PackageDependencyError(source, href, line, str(exc)) from exc
        if resolved is None:
            continue
        relative, replacement, needs_rewrite = resolved
        dependencies.add(relative)
        if not needs_rewrite:
            continue  # Relative/encoded/angle paths remain valid in the mirrored tree.
        candidates = {raw for normalized, raw, line in captured if normalized == href and raw in body}
        # CommonMark autolinks use no parseLinkDestination call.
        for raw in ("<" + href + ">", "<" + unquote(href) + ">"):
            if raw in body:
                candidates.add(raw)
        # Angle forms contain their bare form. Prefer the complete parsed form.
        candidates = {raw for raw in candidates if not any(raw != other and raw in other for other in candidates)}
        if len(candidates) != 1:
            raise StoreError("Cannot unambiguously relocate local Markdown link; supply a relative frozen artifact link")
        raw = next(iter(candidates))
        if body.count(raw) != 1:
            raise StoreError("Repeated absolute material link requires explicit relative links before packaging")
        replacements[raw] = "<" + replacement + ">" if raw.startswith("<") else replacement
    for markup in html:
        collector = _HTMLLinks()
        collector.feed(markup)
        for href in collector.links:
            if _local_target(Path(root), source, href, authorized) is not None:
                raise StoreError("Local HTML links require explicit Markdown links or a self-contained HTML bundle")
    for before, after in replacements.items():
        body = body.replace(before, after, 1)
    return body, dependencies
