"""Small exact-arithmetic experiments. A passing experiment is not a proof."""
from __future__ import annotations

from fractions import Fraction
import json
import re

from ..core.contracts import ProtocolError
from ..core.store import digest, dumps

ENGINE_VERSION = "exact-rational-check"


def execute(program):
    if not isinstance(program, dict) or set(program) != {"steps", "assertions"}:
        raise ProtocolError("A program contains steps and assertions only.")
    if not isinstance(program["steps"], list) or len(program["steps"]) > 64 or not isinstance(program["assertions"], list) or not 1 <= len(program["assertions"]) <= 64:
        raise ProtocolError("Use at most 64 steps and 1 to 64 assertions.")
    if len(dumps(program)) > 32000:
        raise ProtocolError("The experiment exceeds 32000 characters.")
    env, nodes = {}, 0

    def number(value):
        if type(value) is not Fraction:
            raise ProtocolError("Arithmetic operands must be rational numbers, not booleans.")
        if max(value.numerator.bit_length(), value.denominator.bit_length()) > 4096:
            raise ProtocolError("The rational-number size limit was exceeded.")
        return value

    def expr(value, depth=0):
        nonlocal nodes
        nodes += 1
        if depth > 16 or nodes > 4000:
            raise ProtocolError("The experiment expression budget was exceeded.")
        if isinstance(value, bool): return value
        if isinstance(value, int) and abs(value).bit_length() <= 4096: return Fraction(value)
        if isinstance(value, str) and len(value) <= 1300 and re.fullmatch(r"-?\d+(?:/\d+|\.\d+)?", value):
            try: return number(Fraction(value))
            except (ValueError, ZeroDivisionError) as exc: raise ProtocolError("Invalid rational literal.") from exc
        if isinstance(value, dict) and set(value) == {"var"} and isinstance(value["var"], str) and value["var"] in env:
            return env[value["var"]]
        if not isinstance(value, list) or not value or not isinstance(value[0], str):
            raise ProtocolError("Use integer/rational literals, {var:name}, or [operator, operands...].")
        op, args = value[0], value[1:]
        if op == "if":
            if len(args) != 3: raise ProtocolError("if needs condition, true expression, false expression.")
            condition = expr(args[0], depth + 1)
            if type(condition) is not bool: raise ProtocolError("if condition must be boolean.")
            return expr(args[1 if condition else 2], depth + 1)
        arity = {"sub":2, "div":2, "pow":2, "abs":1, "eq":2, "ne":2, "lt":2, "le":2, "gt":2, "ge":2}
        if op not in arity and op not in {"add", "mul", "min", "max"}:
            raise ProtocolError("Unsupported exact-arithmetic operator.")
        if (op in arity and len(args) != arity[op]) or not 1 <= len(args) <= 64:
            raise ProtocolError("Wrong operator arity.")
        values = [number(expr(a, depth + 1)) for a in args]
        if op == "eq": return values[0] == values[1]
        if op == "ne": return values[0] != values[1]
        if op == "lt": return values[0] < values[1]
        if op == "le": return values[0] <= values[1]
        if op == "gt": return values[0] > values[1]
        if op == "ge": return values[0] >= values[1]
        try:
            if op == "add": result = sum(values, Fraction(0))
            elif op == "sub": result = values[0] - values[1]
            elif op == "mul":
                result = Fraction(1)
                for x in values: result = number(result * x)
            elif op == "div": result = values[0] / values[1]
            elif op == "abs": result = abs(values[0])
            elif op == "min": result = min(values)
            elif op == "max": result = max(values)
            else:
                power = values[1]
                if power.denominator != 1 or abs(power) > 16:
                    raise ProtocolError("Power must be an integer between -16 and 16.")
                result = values[0] ** int(power)
        except ZeroDivisionError as exc:
            raise ProtocolError("Division by zero in the executed branch.") from exc
        return number(result)

    def encode(value): return value if type(value) is bool else str(value)
    for step in program["steps"]:
        if not isinstance(step, dict) or set(step) != {"name", "expr"} or not isinstance(step["name"], str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]{0,63}", step["name"]) or step["name"] in env:
            raise ProtocolError("Each step needs a unique identifier name and expr.")
        env[step["name"]] = expr(step["expr"])
    results, ids = [], set()
    for assertion in program["assertions"]:
        if not isinstance(assertion, dict) or set(assertion) != {"id", "left", "relation", "right"} or not isinstance(assertion["id"], str) or not 1 <= len(assertion["id"]) <= 160 or assertion["id"] in ids:
            raise ProtocolError("Each assertion needs a unique id, left, relation, and right.")
        relation = assertion["relation"]
        if relation not in {"eq", "ne", "le", "lt", "ge", "gt"}: raise ProtocolError("Unsupported assertion relation.")
        left, right = number(expr(assertion["left"])), number(expr(assertion["right"]))
        passed = {"eq":left == right, "ne":left != right, "le":left <= right,
                  "lt":left < right, "ge":left >= right, "gt":left > right}[relation]
        results.append({"id":assertion["id"], "left":encode(left), "relation":relation, "right":encode(right), "passed":passed})
        ids.add(assertion["id"])
    return {"values":{k:encode(v) for k,v in env.items()}, "assertions":results,
            "all_passed":all(row["passed"] for row in results)}


def run_check(host, label, program_text, evidence_refs, call_id):
    if not isinstance(label, str) or not 1 <= len(label) <= 200 or not isinstance(program_text, str) or len(program_text) > 32000:
        raise ProtocolError("Use a short label and a program of at most 32000 characters.")
    if not isinstance(evidence_refs, list) or not 1 <= len(evidence_refs) <= 16 or len(set(evidence_refs)) != len(evidence_refs):
        raise ProtocolError("Bind 1 to 16 distinct authorized proof/source references.")
    for ref in evidence_refs:
        if host._allowed(ref)["kind"] not in {"proof", "source", "result"}:
            raise ProtocolError("Experiment evidence must be a formal proof, original source, or result.")
    program = json.loads(program_text)
    result = execute(program)
    record = {"tool":"exact_check", "engine_version":ENGINE_VERSION, "label":label,
              "program":program, "program_digest":digest(program), "evidence_refs":evidence_refs,
              "job_id":host.job["id"], "result":result,
              "limit":"Finite arithmetic experiments can refute a proposed identity or check a specified example; passing does not prove a theorem or establish source fidelity."}
    ref = host.artifacts.put("external_result", record, host.job["id"], evidence_refs)
    host.ws.event(host.job["id"], "exact_check_executed", {"ref":ref, "call_id":call_id, "program_digest":digest(program), "engine_version":ENGINE_VERSION})
    host.grants.add(ref)
    return {"check_ref":ref, "all_passed":result["all_passed"], "assertion_count":len(result["assertions"]),
            "failed_assertion_ids":[a["id"] for a in result["assertions"] if not a["passed"]],
            "notice":record["limit"]}


def validate_execution_check(check, proof_ref, artifacts, *, subject_ref):
    """Validate execution provenance only, never classify a mathematical proof."""
    if not isinstance(check, dict) or set(check) != {"required", "reason", "check_refs"} or type(check["required"]) is not bool or not isinstance(check["reason"], str) or not check["reason"].strip() or not isinstance(check["check_refs"], list):
        return ["Declare execution_check.required, a scientific reason, and check_refs."]
    refs = check["check_refs"]
    if len(refs) > 16 or any(not isinstance(ref, str) for ref in refs) or len(set(refs)) != len(refs) or (check["required"] and not refs):
        return ["A required execution check needs 1 to 16 distinct executed receipts."]
    errors = []
    for ref in refs:
        try:
            item = artifacts.get(ref); body = item["data"]
            if item["kind"] != "external_result" or body.get("tool") != "exact_check" or body.get("engine_version") != ENGINE_VERSION:
                raise ProtocolError("Not a supported exact_check receipt.")
            if proof_ref not in body["evidence_refs"] or body["job_id"] != item["producer"]:
                raise ProtocolError("The experiment is not bound to this proof and producer.")
            result = execute(body["program"])
            if body["program_digest"] != digest(body["program"]) or body["result"] != result or result["all_passed"] is not True:
                raise ProtocolError("The executed experiment failed or its transcript is inconsistent.")
            ws = artifacts.workspace
            matching = [json.loads(row["payload"]) for row in ws.query("SELECT payload FROM events WHERE job=? AND event='exact_check_executed'", (item["producer"],))]
            if not any(e.get("ref") == ref and e.get("program_digest") == body["program_digest"] and e.get("engine_version") == ENGINE_VERSION for e in matching):
                raise ProtocolError("No actual tool execution event supports this receipt.")
            job = ws.job(item["producer"])
            if job["role"] != "profile_reviewer":
                raise ProtocolError("Independent proof credentials require a reviewer's executed experiment.")
            if job["inputs"].get("subject_ref") != subject_ref:
                found = False
                if job["status"] == "complete":
                    for event in ws.query("SELECT payload FROM events WHERE job=? AND event='validated_handoff'", (job["id"],)):
                        handoff = json.loads(event["payload"])
                        if handoff.get("status") != "complete": continue
                        for review_ref in handoff.get("refs", []):
                            prior = artifacts.get(review_ref)
                            if prior["kind"] != "review" or prior["data"].get("subject_ref") != job["inputs"].get("subject_ref"): continue
                            found |= any(a.get("proof_ref") == proof_ref and ref in a.get("execution_check", {}).get("check_refs", []) for a in prior["data"].get("proof_approvals", []))
                if not found: raise ProtocolError("Historical experiments need a completed independent proof credential; current scope must still be reviewed.")
        except (ProtocolError, KeyError, TypeError, ValueError) as exc:
            errors.append(str(exc))
    return errors
