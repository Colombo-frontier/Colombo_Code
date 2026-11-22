#!/usr/bin/env python3
"""Build the local, offline Complexity Atlas from authoritative profile JSON.

No data is fetched by the generated pages. MathJax and its components are
copied from visualization/assets/mathjax by the parent build workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import pathlib
import re
import shutil
from collections import Counter, defaultdict
from urllib.parse import quote

ROOT = pathlib.Path(__file__).resolve().parents[2]

# Display-only aliases/appendices. Canonical hashes above are checked before
# passing an independent display copy to the legacy renderer.
import sys
sys.path.insert(0, str(ROOT / "data/tools"))
from public_render_adapter import normalise_display_profile, maintenance_html
from public_display_rules import html_title_errors
from public_navigation_bridge import load_bridge, project
SRC = pathlib.Path(__file__).resolve().parent
TOPICS = {
    "single_objective": "Single-objective optimization",
    "bilevel": "Bilevel optimization", "minimax": "Minimax optimization",
    "saddle_point": "Saddle-point problems",
    "variational_inequality": "Variational inequalities",
    "matrix_computation": "Matrix computation", "online_bandit": "Online learning and bandits",
}
AXES = [("task", "Task"), ("model", "Admissible model"),
        ("oracle", "Oracle interface"), ("output", "Output"),
        ("metric", "Loss or accuracy criterion"), ("resource", "Resource accounting")]
STATUS = {
    "optimal": "Optimal", "fully_optimal": "Fully optimal",
    "logarithmic_gap": "Logarithmic gap", "polynomial_gap": "Polynomial gap",
    "other_quantified_gap": "Other quantified gap", "bounds_missing": "Bounds missing",
    "missing_upper": "Upper bound missing", "missing_lower": "Lower bound missing",
    "missing_both": "Both bounds missing", "joint_budget_unclosed": "Joint budget unresolved",
    "infinite_complexity": "Infinite complexity", "infeasible_task": "Infeasible task",
}
MATH = re.compile(r"(\$\$[\s\S]*?\$\$|\$(?:\\.|[^$])*?\$)")
# Explicitly reviewed source fields, rather than a formula-detection heuristic.
# The original source renders this definition in math mode.
DISPLAY_FORMATS = {"CV_S_EXACT_RESOLVENT": {"/symbols/14/definition": "math"}}
LITERAL_SIGNATURES = {
    '(sample_id,x,y)', 'F(x,y;sample_id)', 'G(x,y;sample_id)',
    '(G_f,x,G_f,y,G_g,x,G_g,y)', 'G_f(x,y)=(G_f,x,G_f,y)', 'G_g(x,y)=(G_g,x,G_g,y)',
}


def esc(value):
    return html.escape(str(value if value is not None else ""), quote=True)


def display_terms(value):
    value = re.sub(r'information interface', 'Oracle interface', str(value), flags=re.IGNORECASE)
    return re.sub(r'\bcoverage\b', lambda m: 'Applicability' if m.group(0)[0].isupper() else 'applicability', value, flags=re.IGNORECASE)


def plain(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "; ".join(plain(v) for v in value if v is not None)
    if isinstance(value, dict):
        return "; ".join(f"{k.replace('_', ' ')}: {plain(v)}" for k, v in value.items())
    return str(value)


def paragraphs(value):
    if not value:
        return []
    return value if isinstance(value, list) else [value]


def normalize_math_text(source):
    """Unwrap redundant nested \\text using balanced TeX groups.

    This browser-only normalization leaves every text character and every
    surrounding mathematical token in place. Escaped braces and control
    symbols are read as tokens; braces are never matched with a regex.
    """
    def group_end(text, start):
        depth = 1
        i = start + 1
        while i < len(text):
            if text[i] == '\\':
                i += 1
                if i < len(text) and not text[i].isalpha():
                    i += 1  # escaped braces, \\, \$, etc.
                else:
                    while i < len(text) and text[i].isalpha():
                        i += 1
                continue
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        return None

    def walk(text, within_text=False):
        out = []
        i = 0
        inline_math = False
        while i < len(text):
            char = text[i]
            if char == '\\':
                j = i + 1
                while j < len(text) and text[j].isalpha():
                    j += 1
                if j == i + 1:
                    token = text[i:i + 2]
                    if within_text and token in ('\\(', '\\)'):
                        inline_math = token == '\\('
                    out.append(token)
                    i += len(token)
                    continue
                command = text[i + 1:j]
                k = j
                while k < len(text) and text[k].isspace():
                    k += 1
                if command in ('text', 'ensuremath') and k < len(text) and text[k] == '{':
                    end = group_end(text, k)
                    if end is not None:
                        body = walk(text[k + 1:end], command == 'text')
                        if command == 'text' and within_text and not inline_math:
                            out.append(body)
                        else:
                            out.append(text[i:k + 1] + body + '}')
                        i = end + 1
                        continue
                out.append(text[i:j])
                i = j
                continue
            if char == '{':
                end = group_end(text, i)
                if end is not None:
                    out.append('{' + walk(text[i + 1:end], within_text and not inline_math) + '}')
                    i = end + 1
                    continue
            if within_text and char == '$':
                inline_math = not inline_math
            out.append(char)
            i += 1
        return ''.join(out)
    return walk(str(source))


def source_pointers_containing(value, needle, pointer=''):
    if isinstance(value, dict):
        return [p for key, child in value.items() for p in source_pointers_containing(child, needle, pointer + '/' + key.replace('~', '~0').replace('/', '~1'))]
    if isinstance(value, list):
        return [p for i, child in enumerate(value) for p in source_pointers_containing(child, needle, pointer + '/' + str(i))]
    return [pointer] if isinstance(value, str) and needle in value else []


class ProfileRenderer:
    def __init__(self, profile, classification=None, explanations=None, colombo=None):
        self.p = profile
        self.classification = classification or {}
        self.explanations = explanations or {}
        self.colombo = colombo or {}
        self.math_normalizations = {}
        self.literal_signature_normalizations = {}
        self.refs = {r["id"]: r for r in profile.get("references", [])}
        self.ref_numbers = {str(i): r for i, r in enumerate(profile.get("references", []), 1)}
        self.views = {v["view_id"]: v for v in profile["views"]}
        self.bounds = {b["id"]: b for b in profile["bounds"]}
        self.blabels = {b["id"]: f"B{i}" for i, b in enumerate(profile["bounds"], 1)}
        self.qlabels = {q["id"]: f"Q{i}" for i, q in enumerate(profile["quantities"], 1)}
        self.projections = {r["resource_projection_id"]: r for r in profile["resource_projections"]}

    def view_label(self, view_id):
        return self.views[view_id]["label"] if len(self.views) > 1 else ""

    def tex(self, value):
        normalized = normalize_math_text(value)
        if normalized != value:
            self.math_normalizations[value] = normalized
        return normalized

    def rich(self, value):
        """Escape prose while leaving original TeX tokens intact for MathJax."""
        out = []
        for token in MATH.split(plain(value)):
            if not token:
                continue
            if token.startswith("$$") and token.endswith("$$"):
                out.append('<span class="display-math">' + esc(self.tex(token)) + '</span>')
            elif token.startswith("$") and token.endswith("$"):
                out.append(esc(self.tex(token)))
            else:
                text = esc(display_terms(token))
                text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
                text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
                def citation(match):
                    r = self.ref_numbers.get(match.group(1))
                    return (f'<a class="citation" href="{esc(r["url"])}" target="_blank" rel="noopener" title="{esc(r["title"])}">[{match.group(1)}]</a>'
                            if r and r.get("url") else match.group(0))
                text = re.sub(r"\[(\d+)\]", citation, text)
                out.append(text)
        return "".join(out)

    def para(self, value, cls=""):
        if not value:
            return ""
        return f'<p{(" class=" + chr(34) + cls + chr(34)) if cls else ""}>{self.rich(value)}</p>'

    def ps(self, values):
        return "".join(self.para(v) for v in paragraphs(values))

    def math(self, value):
        if not value:
            return ""
        value = str(value).strip()
        if "$" in value:
            return '<div class="formula">' + self.rich(value) + '</div>'
        return '<div class="formula">\\[' + esc(self.tex(value)) + '\\]</div>'

    def signature_math(self, value, source_pointer=None):
        if value in LITERAL_SIGNATURES:
            # These source signatures use literal identifier punctuation, not
            # LaTeX subscripts. Preserve their characters instead of guessing
            # which commas or suffixes belong inside a mathematical index.
            rendered = r'\texttt{' + value.replace('_', r'\_') + '}'
            entry = self.literal_signature_normalizations.setdefault(value, {'after': rendered, 'source_pointers': []})
            if source_pointer and source_pointer not in entry['source_pointers']:
                entry['source_pointers'].append(source_pointer)
            return self.math(rendered)
        return self.math(value)

    def field(self, label, value):
        return f'<div class="field"><span class="field-label">{esc(label)}</span><div>{self.rich(value)}</div></div>' if value else ""

    def source_links(self, bound):
        ids = list(bound.get("source_refs", []))
        ev = {e["id"]: e for e in self.p.get("evidence", [])}
        for eid in bound.get("evidence_refs", []):
            e = ev.get(eid, {})
            ids.extend(e.get("source_refs", []))
            if e.get("source_ref"):
                ids.append(e["source_ref"])
        links = []
        for rid in dict.fromkeys(ids):
            r = self.refs.get(rid)
            if r:
                links.append(f'<a class="paper-link" href="{esc(r.get("url", "#"))}" target="_blank" rel="noopener">{self.rich(r.get("title", rid))}<span aria-hidden="true"> ↗</span></a>')
        if bound.get("proof_refs") or any(ev.get(eid, {}).get("kind") == "local_argument" for eid in bound.get("evidence_refs", [])):
            links.append('<a class="local-proof" href="#downloads">Local argument in this profile · see complete PDF / LaTeX ↗</a>')
        return '<div class="bound-sources">' + "".join(links) + '</div>' if links else ""

    def oracle_operations(self):
        if self.p['primary_domain'] != 'bilevel':
            return ''
        bindings = self.classification.get('operation_bindings', [])
        if not bindings:
            return ''
        registry = self.p.get('registry', {})
        objects = {o['id']: o for o in registry.get('objects', [])}
        blocks = {v['id']: v for v in registry.get('variable_blocks', [])}
        resource = self.p['common_specification'].get('resource', {})
        rules = {rule['id']: rule for rule in resource.get('cost_rules', []) if isinstance(rule, dict) and rule.get('id')}
        components = {component['code']: component for component in resource.get('components', [])}
        roles = {'upper_objective': 'Upper objective', 'lower_objective': 'Lower objective',
                 'reduced_objective': 'Reduced objective', 'declared_auxiliary_object': 'Auxiliary object'}
        out = [f'<details class="oracle-operations"><summary>Queries and responses <span>{len(bindings)} operations</span></summary>']
        for i, binding in enumerate(bindings, 1):
            applies = [self.view_label(v) for v in binding.get('view_ids', []) if v in self.views and self.view_label(v)]
            if binding.get('state') != 'structured':
                out.append(f'<article class="oracle-operation"><h4>{i:02d} · Declared operation</h4>')
                if applies:
                    out.append(self.field('Applies to', '; '.join(applies)))
                out.append(self.para(binding.get('raw')))
                out.append('</article>')
                continue
            source = binding['source_fields']
            out.append(f'<article class="oracle-operation"><h4>{i:02d} · {esc(source.get("operation_code", "Declared operation").replace("_", " ").capitalize())}</h4>')
            if applies:
                out.append(self.field('Applies to', '; '.join(applies)))
            target_ids = [source.get('target_object')] + source.get('target_objects', [])
            target_records = {obj['id']: obj for obj in binding.get('target_object_registry', [])}
            for oid in target_ids:
                if oid in objects:
                    target_records[oid] = objects[oid]
            for obj in target_records.values():
                out.append(self.field(roles.get(obj.get('role_code'), 'Target object'), obj.get('definition')))
            derivative_ids = list(dict.fromkeys([source.get('derivative_reference_object')] + source.get('derivative_reference_objects', [])))
            for oid in derivative_ids:
                if oid and oid not in target_records and oid in objects:
                    out.append(self.field('Derivative reference', objects[oid].get('definition')))
            out.append('<div class="operation-signatures">')
            for key, label in [('query_signature', 'Query'), ('response_signature', 'Response')]:
                if source.get(key):
                    out.append(f'<div><span class="minor-eyebrow">{label}</span>{self.signature_math(source[key], binding["source_pointer"] + "/" + key)}</div>')
            out.append('</div>')
            order = source.get('derivative_order')
            if isinstance(order, (str, int)):
                out.append(self.field('Derivative order', str(order).replace('_', ' ')))
            block_roles = [blocks[bid].get('role') for bid in source.get('variable_blocks', []) if bid in blocks and blocks[bid].get('role')]
            if block_roles:
                out.append(self.field('Variable blocks', '; '.join(dict.fromkeys(block_roles))))
            quality = source.get('feedback_quality', {})
            if isinstance(quality, dict):
                out.append(self.field('Feedback', quality.get('description') or quality.get('code')))
            elif quality:
                out.append(self.field('Feedback', quality))
            for key, label in [('coupling', 'Sample coupling and reuse'), ('index_control', 'Selection permissions'), ('access_schedule', 'Access schedule'), ('order_convention', 'Order convention')]:
                out.append(self.field(label, source.get(key)))
            rule = rules.get(source.get('cost_rule_ref'))
            if rule and isinstance(rule.get('cost'), dict):
                for coordinate, amount in rule['cost'].items():
                    component = components.get(coordinate, {})
                    description = component.get('description')
                    unit = component.get('unit', 'units in the declared resource coordinate')
                    if amount == 1 and unit == 'oracle responses':
                        unit = 'oracle response'
                    out.append(self.field('Unit charge', f'{amount} {unit}' + (f' — {description}' if description else '')))
            elif rule:
                for key in ['description', 'meaning']:
                    out.append(self.field('Unit charge', rule.get(key)))
            out.append('</article>')
        out.append('</details>')
        return ''.join(out)

    def specification(self):
        out = ['<section class="document-section" id="specification"><div class="section-heading"><span>01</span><h2>Setting specification</h2></div>']
        for axis, label in AXES:
            obj = (self.p.get("display_specification") or self.p["common_specification"]).get(axis, {})
            out.append(f'<div class="spec-axis"><h3>{label}</h3>')
            note = self.explanations.get(axis, {})
            explanation = ''.join(self.para(paragraph, 'spec-explanation') for paragraph in note.get('paragraphs', []))
            replacement = int(note['replace_pointer'].rsplit('/', 1)[1]) if note.get('action') == 'replace' else None
            if replacement is None:
                out.append(explanation)
            if obj.get("description_paragraphs"):
                out.extend(explanation if i == replacement else self.para(paragraph)
                           for i, paragraph in enumerate(paragraphs(obj["description_paragraphs"])))
            elif axis in ("task", "metric"):
                out.append(self.math(obj.get("formulation") or obj.get("base_expression") or obj.get("formula_latex")))
            else:
                for key, value in obj.items():
                    if isinstance(value, str) and not key.endswith(("_ref", "_id")) and key not in ("id", "code"):
                        out.append(self.field(key.replace("_", " ").capitalize(), value))
            if axis == 'oracle':
                out.append(self.oracle_operations())
            out.append('</div>')
        out.append('<div class="spec-axis algorithms-axis"><h3>Algorithm views and success guarantees</h3>')
        for view in self.p["views"]:
            out.append(f'<div class="algorithm-view" id="view-{esc(view["view_id"])}">')
            if self.view_label(view['view_id']):
                out.append(f'<h4>{esc(self.view_label(view["view_id"]))}</h4>')
            a = view["algorithms"]
            out.append(self.ps(a.get("description_paragraphs")))
            if not a.get("description_paragraphs"):
                for key in ["randomization", "adaptivity", "restrictions", "internal_computation"]:
                    out.append(self.field(key.replace("_", " ").capitalize(), plain(a.get(key))))
            for g in view["guarantees"]:
                out.append(self.ps(g.get("description_paragraphs")))
                if not g.get("description_paragraphs"):
                    out.append(self.math(g.get("complete_expression") or g.get("formula_latex")))
                    out.append(self.field("Guarantee", plain(g.get("aggregation_order"))))
            out.extend(self.para(q) for q in view.get("display_qualifications", []))
            out.append(self.field("Budget convention", plain(view.get("budget", {}).get("budget_semantics"))))
            out.append('</div>')
        out.append('</div></section>')
        return "".join(out)

    def notation(self):
        out = ['<section class="document-section" id="notation"><div class="section-heading"><span>02</span><h2>Notation and parameters</h2></div><dl class="notation-list">']
        seen = set()
        for i, s in enumerate(self.p.get("symbols", [])):
            sig = tuple(str(s.get(k)) for k in ["symbol_latex", "meaning", "domain", "definition"])
            if sig in seen:
                continue
            seen.add(sig)
            out.append('<div class="notation-row"><dt>' + self.rich('$' + s.get('symbol_latex', '') + '$') + '</dt><dd>')
            out.append(self.para(s.get("meaning")))
            out.append(self.field("Domain", s.get("domain")))
            if s.get("definition") and str(s["definition"]) not in str(s.get("meaning", "")):
                format = DISPLAY_FORMATS.get(self.p['setting_id'], {}).get(f'/symbols/{i}/definition')
                out.append(self.math(s["definition"]) if format == 'math' else self.para(s["definition"]))
            out.append('</dd></div>')
        out.append('</dl></section>')
        return "".join(out)

    def bound_conditions(self, b):
        ap = b.get("applicability", {})
        out = []
        if not isinstance(ap, dict):
            return self.field("Applicability", plain(ap))
        for key, label in [("conditions", "Conditions"), ("dimension_conditions", "Dimension conditions")]:
            out.append(self.field(label, plain(ap.get(key))))
        scope = b.get("algorithm_class_scope")
        out.append(self.field("Algorithm scope", plain(scope)))
        extras = []
        for key, label in [("oracle_mapping", "Oracle correspondence"), ("guarantee_mapping", "Guarantee conversion"), ("output_mapping", "Output rule"), ("resource_mapping", "Resource conversion")]:
            extras.append(self.field(label, plain(ap.get(key))))
        extras.append(self.field("Constants", b.get("hidden_constants")))
        extras.append(self.field("Logarithmic factors", plain(b.get("hidden_logs"))))
        extras.append(self.field("Derivation", b.get("derivation")))
        extras.append(self.field("Scope qualification", b.get("witness_type_note") or b.get("lower_scope_type_note")))
        extras = [x for x in extras if x]
        if extras:
            out.append('<details class="technical-details"><summary>Correspondence, constants and qualifications</summary>' + "".join(extras) + '</details>')
        return "".join(out)

    def bracket(self):
        out = ['<section class="document-section" id="bracket"><div class="section-heading"><span>03</span><h2>Complexity bracket</h2></div>',
               '<p class="section-note">Each bracket applies to the stated view, success guarantee, resource and parameter region. Status summarizes the documented comparisons.</p>',
               '<details class="quantity-definitions" open><summary>Compared quantities and resource definitions</summary>']
        for q in self.p["quantities"]:
            out.append(f'<article class="quantity-definition" id="quantity-{esc(q["id"])}"><h4>{esc(self.qlabels[q["id"]])} · {esc(q.get("kind", "quantity").replace("_", " "))}</h4>')
            out.append(self.field("View", self.view_label(q["view_id"])))
            out.append(self.math(q.get("expression_latex") or q.get("expression")))
            for key, label in [("label", "Definition"), ("analysis_scope", "Scope"), ("optimization_direction", "Optimization direction")]:
                out.append(self.field(label, q.get(key)))
            out.append(self.ps(q.get("display_notation_note")))
            out.append(self.ps(q.get("definition_note")))
            for key, label in [("metric_contract", "Metric contract"), ("resource_contract", "Resource contract")]:
                out.append(self.field(label, plain(q.get(key))))
            out.append(self.para(q.get("interpretation")))
            out.append('</article>')
        out.append('</details>')
        comps = {c["comparison_id"]: c for c in self.p["comparisons"]}
        for i, row in enumerate(self.p["bracket_rows"], 1):
            cs = [comps[cid] for cid in row["comparison_ids"]]
            c = cs[0]
            br = c["bracket"]
            code = c["status"]["code"]
            credited = [cid for cid in row['comparison_ids'] if cid in self.colombo.get('comparison_ids', [])]
            provenance_badge = colombo_badge(self.colombo) if credited else ''
            credit_attribute = f' data-colombo-comparisons="{esc(",".join(credited))}"' if credited else ''
            out.append(f'<article class="regime-card{" is-colombo" if credited else ""}" id="regime-{i}" data-comparison-ids="{esc(",".join(row["comparison_ids"]))}"{credit_attribute}><div class="regime-top"><span class="regime-index">R{i}</span>{provenance_badge}{badge(code, STATUS.get(code, code))}</div><h3>{esc(c.get("label", "Parameter regime"))}</h3>')
            out.append(self.field("Parameter region", c.get("predicate_text")))
            if credited:
                credited_views = list(dict.fromkeys(comps[cid]['view_id'] for cid in credited))
                out.append(self.field('Colombo contribution views', '; '.join(self.view_label(vid) or vid for vid in credited_views)))
            out.append(self.field("Views", "; ".join(self.view_label(vid) for vid in dict.fromkeys(row["view_ids"]) if self.view_label(vid))))
            guarantees = []
            seen_guarantees = set()
            for comparison in cs:
                signature = (comparison['view_id'], comparison['guarantee_id'])
                if signature in seen_guarantees:
                    continue
                seen_guarantees.add(signature)
                view = self.views[comparison['view_id']]
                guarantee = next(g for g in view['guarantees'] if g['guarantee_id'] == comparison['guarantee_id'])
                if self.view_label(comparison['view_id']):
                    guarantees.append(self.para(self.view_label(comparison['view_id'])))
                expression = guarantee.get('complete_expression') or guarantee.get('formula_latex')
                guarantees.append(self.math(expression) if expression else self.ps(guarantee.get('description_paragraphs')))
            out.append('<details class="guarantee-details"><summary>Success guarantee</summary>' + "".join(guarantees) + '</details>')
            out.append(self.field("Quantity", "; ".join(dict.fromkeys(self.qlabels.get(x["quantity_id"], x["quantity_id"]) for x in cs))))
            rp = self.projections[c["resource_projection_id"]]
            out.append(self.field("Resource", rp.get("description") or rp.get("expression") or "Joint resource budget"))
            joint = bool(br.get("achievable_refs") or br.get("necessary_refs") or code == "joint_budget_unclosed")
            sides = [("achievable_refs", "Achievable budgets"), ("necessary_refs", "Necessary constraints")] if joint else [("lower", "Lower bound"), ("upper", "Upper bound")]
            out.append('<div class="bound-pair">')
            for side, label in sides:
                refs = list(dict.fromkeys(bid for cc in cs for bid in cc["bracket"].get(side if joint else side + "_refs", [])))
                out.append(f'<div class="bound-box {side}"><div class="minor-eyebrow">{label}</div>')
                env = br.get("envelopes", {}).get(side)
                if env:
                    out.append(self.math(env.get("expression_latex") or env.get("expression")))
                    if not refs:
                        out.append(self.para("Nonnegativity of the compared quantity" if env.get("basis") == "nonnegativity" else "Admitted envelope"))
                elif not refs:
                    out.append(self.para("No admitted bound for this comparison" if code not in ("infinite_complexity", "infeasible_task") else STATUS[code], "missing-bound"))
                for bid in refs:
                    b = self.bounds[bid]
                    out.append(f'<div class="bound-claim" data-bound-id="{esc(bid)}"><span class="bound-id">{esc(self.blabels[bid])}</span>')
                    if not env or joint:
                        out.append(self.math(b.get("formula_latex")))
                    out.append(self.field('Meaning of the inequality', b.get('direction_explanation')))
                    for quantity, formula in b.get('formula_by_quantity', {}).items():
                        out.append(self.field('Quantity', quantity.replace('_', ' ')))
                        out.append(self.math(formula))
                    out.append(self.para(b.get("method") or b.get("algorithm_or_hard_family"), "bound-method"))
                    out.append(self.source_links(b))
                    out.append(self.bound_conditions(b))
                    guards = []
                    for comparison in cs:
                        for guard in comparison['bracket'].get('claim_guards', {}).get(bid, []):
                            condition = guard.get('predicate_text')
                            if condition and condition not in guards:
                                guards.append(condition)
                    for condition in guards:
                        if condition != c.get('predicate_text'):
                            out.append(self.field('Branch condition', condition))
                    if joint and b.get("resource_costs"):
                        out.append(self.field("Simultaneous resource costs", plain(b["resource_costs"])))
                    out.append('</div>')
                out.append('</div>')
            out.append('</div>')
            out.append(self.field("Gap or comparison", br.get("ratio_or_gap")))
            out.append(self.field("Comparison argument", br.get("envelope_certificate")))
            out.append('</article>')
        out.append('</section>')
        return "".join(out)

    def evidence(self):
        out = ['<section class="document-section" id="evidence"><div class="section-heading"><span>04</span><h2>Evidence</h2></div><ol class="paper-list">']
        for r in self.p.get("references", []):
            out.append(f'<li><a href="{esc(r.get("url", "#"))}" target="_blank" rel="noopener">{self.rich(r.get("title", r["id"]))}<span aria-hidden="true"> ↗</span></a></li>')
        out.append('</ol></section>')
        return "".join(out)


def badge(code, label):
    cls = "closed" if code in ("optimal", "fully_optimal") else "missing" if code.startswith("missing") or code == "bounds_missing" else "gap"
    return f'<span class="status-badge {cls}" data-status="{esc(code)}"><i aria-hidden="true"></i>{esc(label)}</span>'


def toolkit_filter_axes(dictionary, human_tags):
    """Project Toolkit presentation records into the existing browse controls."""
    common_axes = []
    exact_axes = []
    group_labels = dictionary['group_labels']
    current_detail_counts = Counter(identity for tags in human_tags.values() for identity in {item['machine_concept_id'] for item in tags['details']})
    navigation_counts = Counter(
        concept_id for tags in human_tags.values()
        for concept_id in {concept_id for view in tags['views'] for concept_id in view['facet_ids']}
    )
    supplemented = {
        facet['concept_id'] for tags in human_tags.values() for facet in tags['facets']
        if facet.get('local_navigation_evidence')
    }
    navigation_labels = {
        'family': 'Task family', 'objective_convexity': 'Objective convexity',
        'structure': 'Problem structure', 'monotonicity': 'Operator monotonicity',
        'access': 'Oracle access', 'quality': 'Primitive feedback quality',
        'randomization': 'Randomization', 'object': 'Returned object',
        'goal': 'Target metric', 'error_mode': 'Error guarantee', 'measure': 'Resource measure',
    }
    for axis in dictionary['axes']:
        common_groups = defaultdict(list)
        for option in dictionary['concepts']:
            if option['axis'] != axis['id']:
                continue
            description = display_terms(option.get('description', ''))
            if option['id'] in supplemented:
                description += ' Profile tag tooltips identify explicit feasible domains used to add this label.'
            common_groups[option['group']].append({
                'id': option['id'], 'axis': axis['id'], 'group': option['group'],
                'value': option['value'], 'label': display_terms(option['label']),
                'aliases': [display_terms(alias) for alias in option.get('aliases', [])],
                'description': description.strip(),
                'count_settings': navigation_counts[option['id']],
            })
        common_axes.append({'id': axis['id'], 'label': axis['label'], 'groups': [
            {'id': f'{axis["id"]}:{key}', 'key': key,
             'label': navigation_labels.get(key, group_labels.get(key, key.replace('_', ' ').capitalize())),
             'options': values}
            for key, values in common_groups.items()
        ]})
        exact_groups = defaultdict(list)
        for detail in dictionary['detail_concepts']:
            if detail['axis'] != axis['id']:
                continue
            tag_id = detail['machine_concept_id']
            exact_groups[detail['group']].append({
                'tag_id': tag_id, 'value': tag_id.split(':', 2)[-1],
                'label': display_terms(detail['label']),
                'count_settings': current_detail_counts[tag_id],
            })
        exact_axes.append({'id': axis['id'], 'label': axis['label'], 'groups': [
            {'id': key, 'label': group_labels.get(key, key.replace('_', ' ').capitalize()), 'values': values}
            for key, values in exact_groups.items()
        ]})
    return common_axes, exact_axes


def card_tags_html(human_tags):
    # Shared tags describe the card without joining assertions from distinct views.
    shared_ids = set.intersection(*(set(view['facet_ids']) for view in human_tags['views']))
    tags = [tag for tag in human_tags['facets'] if tag['concept_id'] in shared_ids]
    out = []
    groups = {
        'TASK': ('family',), 'MODEL': ('objective_convexity', 'structure', 'smoothness', 'geometry'),
        'ORACLE': ('access', 'quality'), 'METRIC': ('goal',),
    }
    for axis, preferred_groups in groups.items():
        for group in preferred_groups:
            candidates = [tag for tag in tags if tag['axis'] == axis and tag['group'] == group]
            if not candidates:
                continue
            tag = next((tag for tag in candidates if tag['value'] == 'strongly_convex'), candidates[0])
            out.append(f'<span class="tag" data-axis="{axis}" data-tag-id="{esc(tag["concept_id"])}">{axis}: {esc(display_terms(tag["label"]))}</span>')
            break
    return ''.join(out)


def profile_tags_html(human_tags, dictionary):
    views = {view['view_id']: view['label'] for view in human_tags['views']}
    group_labels = dictionary['group_labels']

    def sections(tags):
        out = []
        for axis in dictionary['axes']:
            groups = defaultdict(list)
            for tag in tags:
                if tag['axis'] != axis['id']:
                    continue
                scopes = [views[view_id] for view_id in tag['view_ids'] if view_id in views]
                scope = ' · Applies to: ' + ', '.join(scopes) if scopes and len(scopes) != len(views) else ''
                title = group_labels.get(tag['group'], tag['group'].replace('_', ' ').capitalize()) + scope
                local_evidence = tag.get('local_navigation_evidence', [])
                if local_evidence:
                    local_views = {item['view_id'] for item in local_evidence}
                    local_scope = ' in ' + ', '.join(label for view_id, label in views.items() if view_id in local_views) if len(local_views) < len(views) else ''
                    source_pointers = dict.fromkeys(assertion['source_pointer'] for item in local_evidence for assertion in item['assertions'])
                    title += f' · Explicit feasible domain{local_scope} ({", ".join(source_pointers)})'
                tag_id = tag.get('machine_concept_id', tag['concept_id'])
                groups[tag['group']].append(f'<span class="tag" data-tag-id="{esc(tag_id)}" title="{esc(title)}">{esc(display_terms(tag["label"]))}</span>')
            if groups:
                out.append(f'<div class="classification-axis" data-axis="{axis["id"]}"><h4>{esc(axis["label"])}</h4><div>')
                for group, values in groups.items():
                    label = group_labels.get(group, group.replace('_', ' ').capitalize())
                    out.append(f'<div class="classification-group"><span>{esc(label)}</span><div>{"".join(values)}</div></div>')
                out.append('</div></div>')
        return ''.join(out)

    out = ['<details class="profile-classification"><summary>Specification tags <span>Toolkit navigation</span></summary>',
           '<div class="classification-grid">', sections(human_tags['facets']), '</div>']
    native_notes = defaultdict(set)
    for note in human_tags.get('interface_notes', []):
        if note['kind'] == 'native_response':
            native_notes[note['text']].update(note['view_ids'])
    if native_notes:
        out.append('<div class="profile-native-notes"><h4>Native oracle response</h4>')
        for note, note_views in native_notes.items():
            labels = [label for view_id, label in views.items() if view_id in note_views]
            prefix = f'{", ".join(labels)}. ' if len(labels) < len(views) else ''
            out.append(f'<p>{esc(prefix + display_terms(note))}</p>')
        out.append('</div>')
    out.extend(['<details class="profile-source-tags"><summary>Exact source tags</summary><div class="classification-grid">',
                sections(human_tags['details']), '</div></details></details>'])
    return ''.join(out)


def search_text(profile, human_tags):
    strings = []
    def visit(value):
        if isinstance(value, str):
            strings.append(value)
        elif isinstance(value, list):
            for item in value:
                visit(item)
        elif isinstance(value, dict):
            for item in value.values():
                visit(item)
    visit(profile)
    strings.extend(tag['label'] for tag in human_tags['facets'] + human_tags['details'])
    strings.extend(note['text'] for note in human_tags.get('interface_notes', []))
    return display_terms(' '.join(dict.fromkeys(strings))).lower()


def head(title, prefix="", math=False):
    math_config = r"""<script>window.MathJax={loader:{load:[]},tex:{inlineMath:[['$','$'],['\\(','\\)']],displayMath:[['$$','$$'],['\\[','\\]']],processEscapes:true,macros:{polylog:'\\operatorname{polylog}',dist:'\\operatorname{dist}',diam:'\\operatorname{diam}',rank:'\\operatorname{rank}',tr:'\\operatorname{tr}',diag:'\\operatorname{diag}',prox:'\\operatorname{prox}',KL:'\\operatorname{KL}',Var:'\\operatorname{Var}',eps:'\\varepsilon',R:'\\mathbb{R}',E:'\\mathbb{E}',mathbbm:['\\mathbf{#1}',1],mathds:['\\mathbf{#1}',1],llbracket:'[\\![',rrbracket:']\\!]'}},svg:{fontCache:'local'},options:{enableMenu:false,enableAssistiveMml:false,skipHtmlTags:['script','noscript','style','textarea','pre','code'],renderActions:{addMenu:[]}},startup:{ready:()=>{MathJax.startup.defaultReady();MathJax.startup.promise.then(()=>{document.documentElement.dataset.mathReady='true';});}}};</script>"""
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><title>{esc(title)} · Complexity Atlas</title><link rel="stylesheet" href="{prefix}assets/atlas.css">' + (math_config + f'<script defer src="{prefix}assets/mathjax/tex-svg.js"></script>' if math else '') + '</head>'


def brand(prefix=""):
    return f'<a class="brand" href="{prefix}index.html"><span class="brand-mark" aria-hidden="true">∿</span><span>Complexity Atlas<small>ORACLE OPTIMIZATION</small></span></a>'


def colombo_badge(info):
    if not info:
        return ''
    return (f'<span class="colombo-badge" data-colombo-state="{esc(info["state"])}" '
            f'title="{esc(info["scope_note"])}">{esc(info["label"])}</span>')


def colombo_legend():
    return ('<div class="colombo-legend" aria-label="Colombo result highlights">'
            '<span class="colombo-badge" data-colombo-state="adopted">★ Colombo</span>'
            '<p>Near-optimal regions</p></div>')


def build_profile(p, index, total, previous, following, classification, human_tags, dictionary, normalization_report=None, explanations=None, colombo=None):
    r = ProfileRenderer(p, classification, explanations, colombo)
    ss = p["summary_status"]
    badges = "".join(badge(x["code"], x["label"]) for x in ss.get("badges", []) + ss.get("special_statuses", []))
    sid = p["setting_id"]
    graph_setting = quote(sid, safe="")
    out = [head(p["title"], "../", True), '<body class="profile-page"><header class="topbar">', brand("../"), f'<a class="back-link" href="../index.html">← All settings <span>{index:02d} / {total:02d}</span></a></header><div class="profile-layout"><aside class="document-nav"><div class="minor-eyebrow">In this profile</div><a href="#specification"><span>01</span> Setting specification</a><a href="#notation"><span>02</span> Notation and parameters</a><a href="#bracket"><span>03</span> Complexity bracket</a><a href="#evidence"><span>04</span> Evidence</a><a href="#downloads"><span>↓</span> Complete profile</a><a href="../graph.html?setting={graph_setting}"><span>↗</span> Related settings</a><div class="nav-note">{len(p["views"])} algorithm {"view" if len(p["views"]) == 1 else "views"}<br>{len(p["comparisons"])} scoped comparisons</div></aside><main class="profile-main" data-setting-id="{esc(sid)}"><div class="profile-intro"><div class="eyebrow">{esc(TOPICS.get(p["primary_domain"], p["primary_domain"]))} <span>·</span> SETTING {index:02d}</div><h1>{esc(p["title"])}</h1><div class="setting-id">{esc(sid)}</div>', r.para(p.get("summary"), "profile-summary"), '<div class="status-line">' + badges + '</div>', profile_tags_html(human_tags, dictionary), '<p class="status-scope">Status applies to the documented comparisons and their explicit parameter regions.</p></div>', r.specification(), r.notation(), r.bracket(), r.evidence(), f'<section class="downloads-section" id="downloads"><div><div class="minor-eyebrow">Complete profile</div><h2>Keep the full argument.</h2><p>Complete bounds, applicability reviews, local arguments and references.</p></div><div class="download-buttons"><a class="button primary" href="../downloads/{esc(sid)}/profile.pdf" download>Download PDF <span>↓</span></a><a class="button secondary" href="../downloads/{esc(sid)}/profile.tex" download>LaTeX source <span>↓</span></a></div></section><nav class="profile-pagination" aria-label="Adjacent settings">']
    # Attribution is presentation metadata, separate from mathematical tags.
    if colombo:
        heading = '<h1>' + esc(p['title']) + '</h1>'
        out = [part.replace(heading, '<div class="profile-heading">' + heading
                            + colombo_badge(colombo) + '</div>', 1) for part in out]
    out.append(f'<a href="{esc(previous["setting_id"])}.html">← Previous setting</a>' if previous else '<span></span>')
    out.append(f'<a href="{esc(following["setting_id"])}.html">Next setting →</a>' if following else '<a href="../index.html">All settings →</a>')
    out.append(f'</nav></main></div><footer class="footer">Complexity Atlas <span>{total} profiles</span><a href="#">Back to top ↑</a></footer></body></html>')
    if normalization_report is not None and (r.math_normalizations or r.literal_signature_normalizations):
        normalizations = [
            {'rule': 'unwrap_redundant_nested_text', 'before': before, 'after': after,
             'source_pointers': source_pointers_containing(p, before)}
            for before, after in r.math_normalizations.items()]
        normalizations += [
            {'rule': 'preserve_literal_signature_identifiers', 'before': before, 'after': entry['after'],
             'source_pointers': entry['source_pointers']}
            for before, entry in r.literal_signature_normalizations.items()]
        normalization_report.append({'setting_id': sid, 'normalizations': normalizations})
    return "".join(out)


def build_index(profiles, catalog, human_tags, dictionary, overview, nebula, colombo_registry=None):
    from nebula_data import nebula_markup
    from overview_data import overview_markup

    count = len(profiles)
    colombo_registry = colombo_registry or {'settings': {}, 'papers': []}
    colombo_marks = colombo_registry['settings']
    catalog_entries = {entry.get('id') or entry.get('setting_id'): entry for entry in catalog['profiles']}
    common_axes, exact_axes = toolkit_filter_axes(dictionary, human_tags)
    statuses = {}
    status_counts = Counter()
    for p in profiles:
        entry = catalog_entries[p['setting_id']]
        for code, label in zip(entry['statusCodes'], entry['statusLabels']):
            statuses.setdefault(code, label)
            status_counts[code] += 1

    def primary_group(axis, group):
        key = group.get('key', group['id'].split(':')[-1])
        return ((axis['id'] == 'TASK' and key in ['family', 'task_family']) or
                (axis['id'] == 'MODEL' and key in ['convexity', 'objective_convexity']) or
                (axis['id'] == 'ORACLE' and key in ['order', 'access_order', 'access', 'quality', 'feedback_quality']))

    def group_controls(axis, group):
        key = f'common|{axis["id"]}|{group.get("key", group["id"].split(":")[-1])}'
        out = [f'<fieldset class="common-fieldset" data-facet-group="{esc(key)}"><legend>{esc(group["label"])}</legend>']
        for option in group['options']:
            n = option.get('count_settings', 0)
            disabled = ' disabled' if not n else ''
            label = f'{group["label"]}: {option["label"]}'
            description = option.get('description', '')
            out.append(f'<label class="filter-option common-option" title="{esc(description)}"><input type="checkbox" name="common" value="{esc(option["id"])}" data-group-key="{esc(key)}" data-filter-label="{esc(label)}"{disabled}><span>{esc(option["label"])}</span><small class="facet-count">{n} {"setting" if n == 1 else "settings"}</small></label>')
        out.append('</fieldset>')
        return ''.join(out)

    out = [head('Research atlas').replace('</head>', '<link rel="stylesheet" href="assets/overview.css"><link rel="stylesheet" href="assets/nebula.css"></head>'), '<body class="index-page"><header class="topbar">', brand(),
           '<nav class="atlas-links" aria-label="Atlas views"><a href="graph.html">Relationship graph <span aria-hidden="true">↗</span></a><span class="edition-label"><i></i> LOCAL RESEARCH LIBRARY</span></nav></header>',
           '<main class="atlas-main"><section class="atlas-heading"><div><div class="eyebrow">A STRUCTURED VIEW OF ORACLE COMPLEXITY</div>',
           '<h1>Known bounds.<br><em>Precisely scoped.</em></h1></div>',
           f'<div class="batch-panel"><span class="batch-number">{count}</span><div>Settings in this atlas</div><span class="batch-rule"></span><p>Full profiles available<br>as PDF and LaTeX.</p></div></section>',
           colombo_legend(), nebula_markup(nebula, overview), overview_markup(overview),
           '<section class="library" id="setting-library" aria-label="Settings library"><div class="library-toolbar"><h2>Explore the atlas</h2>',
           '<label class="search-box"><svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"></circle><path d="m15.5 15.5 4.5 4.5"></path></svg><input id="search" type="search" placeholder="Search concepts, a setting ID, or text…" aria-label="Search concepts or profile text"><kbd>/</kbd></label></div>',
           '<div class="library-layout"><div class="filter-shell" id="filter-shell"><button class="filter-toggle" id="toggle-filters" type="button" aria-expanded="false" aria-controls="filter-panel"><span>Filters <span class="filter-toggle-count" id="filter-toggle-count"></span></span><span class="filter-toggle-action">Common filters <b aria-hidden="true">+</b></span></button>',
           '<aside class="filter-panel simple-filter-panel" id="filter-panel"><div class="filter-heading"><h3>Common filters</h3><button id="reset-filters" type="button">Reset</button></div>',
           '<p class="browse-filter-help">A setting appears when one algorithm view matches at least one choice in every group you use.</p><p class="facet-count-help">Each count shows how many settings match that option with your other groups. Greyed-out options have no matches.</p>']
    for axis in common_axes:
        for group in axis['groups']:
            if primary_group(axis, group):
                out.append(group_controls(axis, group))
    model_axis = next(axis for axis in common_axes if axis['id'] == 'MODEL')
    model_groups = [group for group in model_axis['groups'] if not primary_group(model_axis, group)]
    if model_groups:
        out.append('<details class="more-filters" id="model-details"><summary>Model details <span>Smoothness, geometry, structure and monotonicity</span></summary>')
        out.extend(group_controls(model_axis, group) for group in model_groups)
        out.append('</details>')
    more_axes = [axis for axis in common_axes if axis['id'] != 'MODEL' and any(not primary_group(axis, group) for group in axis['groups'])]
    more_labels = [axis['label'] for axis in more_axes]
    more_hint = ', '.join(more_labels) + ' and research status' if more_labels else 'Research status'
    out.append(f'<details class="more-filters" id="more-filters"><summary>More filters <span>{esc(more_hint)}</span></summary>')
    for axis in more_axes:
        remaining = [group for group in axis['groups'] if not primary_group(axis, group)]
        if remaining:
            out.append(f'<div class="more-filter-axis"><h4>{esc(axis["label"])}</h4>')
            out.extend(group_controls(axis, group) for group in remaining)
            out.append('</div>')
    out.append('<fieldset class="common-fieldset research-status" data-facet-group="status"><legend>Research status</legend><p class="status-filter-note">“Optimal” may apply to one regime; “Fully optimal” summarizes all documented comparisons. Status is checked in the same view as the other filters.</p>')
    for code, label in statuses.items():
        n = status_counts[code]
        out.append(f'<label class="filter-option"><input type="checkbox" name="status" value="{esc(code)}" data-group-key="status"><span>{esc(label)}</span><small class="facet-count">{n} settings</small></label>')
    out.append('</fieldset></details><details class="advanced-filters" id="advanced-filters"><summary>Advanced source tags <span>Exact recorded terminology</span></summary><p class="advanced-filter-note">These preserve the source vocabulary. Use common filters for inherited concepts and synonyms. Advanced groups also match alternatives within one group and require one compatible view.</p><label class="tag-search-box"><input id="tag-search" type="search" placeholder="Find an exact source tag…" aria-label="Find an exact source tag"></label><p class="tag-search-empty" id="tag-search-empty" hidden>No matching source tags.</p>')
    precise_tags = []
    common_options = [option for axis in common_axes for group in axis['groups'] for option in group['options']]
    common_ids = {option['id'] for option in common_options}
    hidden_advanced_ids = []
    def redundant_advanced(axis, group, value):
        # Presentation deduplication only: raw mathematical facts stay in the
        # precise index and in every profile's complete classification.
        if value['tag_id'] in common_ids:
            return True
        if axis['id'] == 'ORACLE' and group['id'] == 'access_order' and value['value'] in ['zero', 'zeroth', 'first', 'higher']:
            return any(option['axis'] == 'ORACLE' and option['group'] in ['access', 'order', 'access_order'] for option in common_options)
        if axis['id'] == 'ORACLE' and group['id'] == 'feedback_quality' and value['value'] in ['exact', 'inexact', 'stochastic', 'sample']:
            return any(option['axis'] == 'ORACLE' and option['group'] == 'quality' for option in common_options)
        if axis['id'] == 'MODEL' and group['id'] == 'convexity' and value['value'] in ['convex', 'strongly_convex', 'weakly_convex', 'nonconvex', 'not_assumed']:
            return any(option['axis'] == 'MODEL' and 'convexity' in option['group'] for option in common_options)
        return False
    for axis in exact_axes:
        axis_output = []
        for group in axis['groups']:
            if not group['values']:
                continue
            key = f'advanced|{axis["id"]}|{group["id"]}'
            group_output = []
            for value in group['values']:
                tag_id = value['tag_id']
                precise_tags.append({'id': tag_id, 'axis': axis['id'], 'group': group['id'], 'groupLabel': group['label'], 'value': value['value'], 'label': value['label']})
                if redundant_advanced(axis, group, value):
                    hidden_advanced_ids.append(tag_id)
                    continue
                n = value['count_settings']
                label = f'{axis["label"]} / {group["label"]}: {value["label"]}'
                disabled = ' disabled' if not n else ''
                group_output.append(f'<label class="filter-option"><input type="checkbox" name="tag" value="{esc(tag_id)}" data-group-key="{esc(key)}" data-filter-label="{esc(label)}"{disabled}><span>{esc(value["label"])}</span><small class="facet-count">{n} settings</small></label>')
            if group_output:
                axis_output.append(f'<div class="taxonomy-subgroup" data-group="{esc(group["id"])}" data-facet-group="{esc(key)}"><h4>{esc(group["label"])}</h4>{"".join(group_output)}</div>')
        if axis_output:
            out.append(f'<details class="facet-group taxonomy-axis" data-axis="{esc(axis["id"])}"><summary><span class="taxonomy-axis-label">{esc(axis["label"])}</span></summary>{"".join(axis_output)}</details>')
    out.append('</details></aside></div>')
    out.append(f'<div class="setting-results"><div class="results-caption"><span id="results-label" role="status">{count} settings</span></div><div id="active-filters" class="active-filters" aria-live="polite"></div><div id="setting-list">')
    records = []
    for i, p in enumerate(profiles, 1):
        sid = p['setting_id']
        ss = p['summary_status']
        entry = catalog_entries[sid]
        tags = human_tags[sid]
        colombo = colombo_marks.get(sid)
        common_views = {view['view_id']: view['facet_ids'] for view in tags['views']}
        precise_views = {view_id: set() for view_id in common_views}
        for detail in tags['details']:
            for view_id in detail['view_ids']:
                precise_views[view_id].add(detail['machine_concept_id'])
        summary_badges = ss.get('badges', []) + ss.get('special_statuses', [])
        mark_class = ' is-colombo' if colombo else ''
        out.append(f'<article class="setting-row{mark_class}" data-setting="{esc(sid)}" data-setting-id="{esc(sid)}"><div class="setting-order">{i:02d}</div><div class="setting-body"><div class="row-meta">{esc(TOPICS.get(p["primary_domain"], p["primary_domain"]))}<span>·</span><code>{esc(sid)}</code></div><h3><a href="settings/{esc(sid)}.html">{esc(p["title"])}</a></h3>{colombo_badge(colombo)}<div class="tags">{card_tags_html(tags)}</div><p class="matching-views" hidden></p><div class="row-bottom"><div class="status-line">')
        out.extend(badge(s['code'], s['label']) for s in summary_badges)
        out.append(f'</div><span class="row-counts">{len(p["views"])} {"view" if len(p["views"]) == 1 else "views"}<span>·</span>{len(p["comparisons"])} {"comparison" if len(p["comparisons"]) == 1 else "comparisons"}</span></div></div><a class="row-arrow" href="settings/{esc(sid)}.html" aria-label="Open {esc(p["title"])}">↗</a></article>')
        if set(common_views) != set(entry['viewStatusCodes']):
            raise ValueError(f'Browse view index differs from the profile view index: {sid}')
        records.append({'id': sid, 'title': p['title'], 'statuses': entry['statusCodes'],
                        'viewTagSets': {view_id: sorted(ids) for view_id, ids in precise_views.items()},
                        'viewLabels': {view['view_id']: view['label'] for view in tags['views']},
                        'viewStatusCodes': entry['viewStatusCodes'],
                        'commonViewFacets': common_views, 'search': search_text(p, tags) + (' colombo ' + colombo['label'].lower() + ' ' + ' '.join(colombo['paper_ids']) if colombo else '')})
    metadata = {'commonAxes': common_axes, 'preciseTags': precise_tags,
                'toolkitVocabularyVersion': dictionary['version'],
                'statuses': [{'id': code, 'label': label} for code, label in statuses.items()],
                'presentationPolicy': {'coarseAdvancedChoicesHidden': hidden_advanced_ids,
                                       'sourceFactsDeleted': False,
                                       'reason': 'Equivalent common concepts have one UI entry; finer source distinctions remain available under Advanced source tags.'}}
    data = json.dumps(records, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    meta = json.dumps(metadata, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    out.append('</div><div id="empty-state" class="empty-state" hidden><span>∅</span><h3>No matches for these conditions</h3><p id="conflict-explanation">This combination has no documented match in the current atlas.</p><p class="empty-state-qualification">A filter conflict does not establish that a setting is absent from the literature.</p><div id="relaxation-options" class="relaxation-options"></div><button id="clear-empty" class="button secondary" type="button">Clear all conditions</button></div></div></div></section></main>')
    out.append(f'<footer class="footer">Complexity Atlas <span>{count} profiles · Research statements preserved from the source</span><a href="#">Back to top ↑</a></footer>')
    out.append(f'<script id="atlas-search-data" type="application/json">{data}</script><script id="atlas-browse-meta" type="application/json">{meta}</script><script src="assets/nebula_bundles.js"></script><script src="assets/nebula.js"></script><script src="assets/overview.js"></script><script src="assets/browse-engine.js"></script><script src="assets/atlas.js"></script></body></html>')
    return ''.join(out)


def append_native_records(page, canonical):
    # No native mutation: the complete appendix uses the original source value.
    if canonical.get("joint_analysis") is None:
        return page
    marker = '<section class="downloads-section"'
    if page.count(marker) != 1:
        raise ValueError("Ambiguous native-record appendix insertion point")
    return page.replace(marker, maintenance_html(canonical) + marker, 1)


def public_root(requested):
    from public_build_root import checked_root
    return checked_root(requested, ROOT)


def complete_catalog(root):
    catalog = json.loads((root / "data/derived/catalog.json").read_text("utf-8"))
    rows = catalog.get("profiles")
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Missing complete catalog row array")
    ids = [row.get("id") for row in rows]
    native_ids = {path.parent.name for path in (root / "data/settings").glob("*/profile.json")}
    if (any(not isinstance(sid, str) for sid in ids) or len(ids) != len(set(ids))
            or set(ids) != native_ids or catalog.get("profile_count") != len(native_ids)):
        raise ValueError("Catalog/native IDs and profile_count must agree exactly before building")


def main():
    from catalog_order import load_ordered_catalog
    from navigation_additions import apply_navigation_additions, load_navigation_additions
    from nebula_data import build_nebula
    from overview_data import build_overview
    from specification_explanations import bind_explanations, load_explanations
    from colombo_results import load_colombo_results, display_registry

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=pathlib.Path, default=ROOT)
    args = parser.parse_args()
    root = public_root(args.root)
    complete_catalog(root)
    canonical_profiles = {}
    bridge_rules, bridge_registry = load_bridge(root)
    navigation_projection = {}
    catalog = load_ordered_catalog(root / "data/derived/catalog.json")
    dictionary = json.loads((root / 'data/vocabulary/human_tags.json').read_text())
    navigation_additions = load_navigation_additions(root)
    explanations = load_explanations(root)
    bound_explanations = {}
    common_ids = {option['id'] for option in dictionary['concepts']}
    exact_ids = {detail['machine_concept_id'] for detail in dictionary['detail_concepts']}
    expected_axes = ['TASK', 'MODEL', 'ORACLE', 'ALGORITHMS', 'OUTPUT', 'METRIC', 'GUARANTEE', 'RESOURCE']
    if [axis['id'] for axis in dictionary['axes']] != expected_axes:
        raise ValueError('The Toolkit vocabulary must define the eight specification axes in order')
    profiles = []
    classifications = {}
    human_tags = {}
    for entry in catalog["profiles"]:
        sid = entry.get("id") or entry.get("setting_id")
        profile_path = root / 'data/settings' / sid / 'profile.json'
        profile_bytes = profile_path.read_bytes()
        profile = json.loads(profile_bytes)
        if entry['domain'] != profile['primary_domain']:
            raise ValueError(f'Catalog task differs from the profile primary domain: {sid}')
        profile_sha256 = hashlib.sha256(profile_bytes).hexdigest()
        bound_explanations[sid] = bind_explanations(profile, profile_sha256, explanations)
        classification_bytes = (profile_path.parent / 'classification.json').read_bytes()
        classification = json.loads(classification_bytes)
        if classification['profile_sha256'] != profile_sha256:
            raise ValueError(f'Classification is stale relative to its profile: {sid}')
        tags = json.loads((profile_path.parent / 'human_tags.json').read_text())
        canonical = json.dumps(profile, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        if tags['setting_id'] != sid or tags['profile_sha256'] != hashlib.sha256(canonical).hexdigest():
            raise ValueError(f'Toolkit tags are stale relative to the profile: {sid}')
        if tags['vocabulary_version'] != dictionary['version']:
            raise ValueError(f'Toolkit tags use a different vocabulary version: {sid}')
        tags, projection = project(profile, classification, tags, dictionary, root, bridge_rules, bridge_registry)
        if projection is not None:
            navigation_projection[sid] = projection
        tags = apply_navigation_additions(tags, navigation_additions)
        view_ids = {view['view_id'] for view in profile['views']}
        if {view['view_id'] for view in tags['views']} != view_ids:
            raise ValueError(f'Toolkit tags use different view IDs: {sid}')
        if any(set(view['facet_ids']) - common_ids for view in tags['views']):
            raise ValueError(f'Toolkit tags use an unregistered navigation concept: {sid}')
        if any(detail['machine_concept_id'] not in exact_ids or set(detail['view_ids']) - view_ids for detail in tags['details']):
            raise ValueError(f'Toolkit details use an unregistered concept or view: {sid}')
        canonical_profiles[sid] = profile
        profiles.append(normalise_display_profile(profile))
        classifications[sid] = classification
        human_tags[sid] = tags
    colombo_registry = display_registry(load_colombo_results(root, canonical_profiles))
    colombo_marks = colombo_registry['settings']
    dist = root / "visualization/dist"
    (dist / "settings").mkdir(parents=True, exist_ok=True)
    (dist / "assets").mkdir(exist_ok=True)
    for filename in ["atlas.css", "atlas.js", "browse-engine.js", "overview.css", "overview.js", "nebula.css", "nebula.js", "nebula_bundles.js"]:
        shutil.copy2(SRC / filename, dist / "assets" / filename)
    math_src = root / "visualization/assets/mathjax"
    if math_src.exists():
        shutil.copytree(math_src, dist / "assets/mathjax", dirs_exist_ok=True)
    (dist / "navigation-projection.json").write_text(json.dumps({"settings": navigation_projection}, ensure_ascii=False, indent=2))
    overview = build_overview(profiles, human_tags, dictionary, root, colombo_marks)
    nebula = build_nebula(overview, root)
    (dist / "index.html").write_text(build_index(profiles, catalog, human_tags, dictionary, overview, nebula, colombo_registry))
    normalization_report = []
    for i, p in enumerate(profiles):
        sid = p['setting_id']
        page = build_profile(p, i + 1, len(profiles), profiles[i - 1] if i else None, profiles[i + 1] if i + 1 < len(profiles) else None, classifications[sid], human_tags[sid], dictionary, normalization_report, bound_explanations[sid], colombo_marks.get(sid))
        page = append_native_records(page, canonical_profiles[sid])
        if html_title_errors(page):
            raise ValueError(f"Forbidden display label remains in {p['setting_id']}")
        (dist / "settings" / f"{p['setting_id']}.html").write_text(page)
    from build_graph_public import build_graph

    build_graph(root=root)
    print(json.dumps({"pages": len(profiles) + 2, "profiles": len(profiles),
                      "entry": str(dist / "index.html"), "graph": str(dist / "graph.html")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
