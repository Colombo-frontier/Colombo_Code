---
name: check-report
description: Independently assess an exact mathematical review against its frozen problem, draft, evidence and record mappings before any feedback or acceptance is released.
---

# Check-report: Confirming Review Findings

## 1. Objective

In a new independent process, assess whether the fixed first-stage report is supported by mathematical facts. This skill corresponds to `stage=report_check`; independently verify the report rather than substituting agreement with the preceding reviewer for verification.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| `review_request.json` | Confirm this stage, the frozen-input identity, and `review_id` and `report_revision`. |
| Requested `input_manifest_file` | Check inputs against the actual manifest in the workspace root; a historical source catalog is not the set of files delivered for this review. |
| `first_report.json` | Read the version specified by the request and all actual checks and findings it contains. |
| Requested `input/` material | Identify the objective from the original problem, then read the draft proof and necessary evidence. Material paths are relative to `input/`. |
| Frozen record mappings | When making record-level judgments, read the actual versions in `input/cell_record_evidence.json`. |
| `confirmation_notes.json` and same-stage handoff reports (when resuming) | Read completed mathematical assessments, evidence, and unresolved issues. |

Read these files using the current workspace's file-access method; keep the request, frozen material, and first report unchanged.

## 3. Procedure: How to Confirm the Report

### 3.1 Verify the Original Problem and Substantive Criticisms

First clarify the objective from the original problem, then read the draft proof and necessary evidence. For every substantive criticism in the first report, locate the original derivation and actually check its conditions, calculations, dependencies, and consequences. Assess whether an omission can be filled routinely and whether an unnecessary condition or writing preference has been treated as an error. Check the evidential limits of uncertain findings as well; uncertainty cannot be directly upgraded into an error.

The original `problem.md` retains all task responsibilities; the draft must independently state its mathematical scope because the final manuscript does not append the original task's operational instructions. Read the necessary evidence from the actual frozen manifest; do not treat undelivered files listed in historical source catalogs as already verified.

### 3.2 Independently Verify Decisive Steps and Coverage

Even if the first report is `pass`, independently verify the decisive steps supporting the final conclusion and the coverage of the objective; checking report format alone is insufficient. Recheck every check actually recorded in the original report, verify whether its `coverage` includes the original objective, all necessary assertions and transitions, and independently look for omissions; reviewing all existing IDs is not proof that none were omitted. A duplicate checklist is unnecessary. For external theorems, check source locations, original statements, assumptions, and application to the current problem; storing every external theorem's proof is not required. Use `lookup_sources` to read necessary sources.

### 3.3 Verify Record Mappings

Check every record mapping: whether the `record` object is indeed the version in the frozen evidence, whether the identified error belongs to the record itself, and whether the property scope is accurate. When a correct proposition has merely been misapplied, require the scope to be changed to `application`; do not invalidate the proposition's original local audit.

Locate current material using the request's `review_id` and `report_revision` and each record's `kind,id,revision`; directly compare relevant contents when necessary. Follow the material-identity rules in AGENTS, explaining versions, locations, and actual comparison results in `record_mapping` reasons or working notes, without calculating or attaching additional content digests or fingerprints.

### 3.4 Save Unfinished Work

Save progress with `save_confirmation_notes(summary, pending, evidence)`, where `evidence` is a list of objects containing locations and mathematical assessments. Near the budget deadline, save these grounds before handing off to the next verifier through the handoff skill. Incompletion means neither a pass nor a proof error.

## 4. Constraints: Requirements During Confirmation

- The first report, draft proof, and frozen material are read-only; return issues through confirmation findings for revision in the first stage.
- Uncertain findings cannot be directly upgraded into errors; save progress and hand off unfinished work rather than submitting confirmation with partial coverage.
- When a correct record is misapplied, require correction of the application scope rather than invalidating the record's original local audit.
- Newly discovered issues must first be returned to the first stage for revision; unconfirmed feedback remains within the verifier and is not sent to the prover.

## 5. Outputs: What to Submit and When to End

When complete, use `write_confirmation`:

- `assessment` contains five items: `target_alignment`, `coverage`, `reasoning`, `sources`, and `record_mapping`, each with `{status, reason}`. Status is `supported`, `disputed`, or `unresolved`; the reason must describe what was actually checked.
- `covered_check_ids` lists exactly all actual check IDs in the original report, with no omissions, duplicates, or IDs absent from that report. These are not the numbers in a general checklist. If unfinished, save progress and hand off rather than submitting confirmation with partial coverage.
- `findings` contains exactly one `{finding_id, status, reason}` entry for each original report finding, including nonblocking notes. Use an empty list when there are no findings.
- `decisive_steps` records independently verified key steps as `{location, status, reason}`, with at least one entry. `supported` means support for the first report's assessment of that step: independently confirming that a derivation is indeed wrong supports the report's `revise` judgment; it does not mean that the original derivation is correct. For a `pass` report, explain in particular why the complete argument holds.
- `new_findings` records issues omitted by the original report as `{location, explanation, repair}`. Even if a new issue appears clear, it must first be returned to the first stage for report revision.
- Set `verdict` to `confirmed` only when all the above assessments are `supported` and there are no new findings; any dispute, unresolved issue, or new finding requires `needs_correction`. Summarize the mathematical grounds in `summary`.

`confirmed` affirms the original report as a whole, including its `pass`, `revise`, or `inconclusive` conclusion. `needs_correction` triggers only internal verifier revision, after which a new independent process checks the revised report; unconfirmed feedback is not sent to the prover. Return the tool's short JSON receipt unchanged as the final response.

## 6. Relevant Record Objects

| Object or File | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Review request and frozen material | Read the original problem, draft, evidence, and version identities without modification, and form an independent assessment. | `review_request.json` and its specified `input/` paths. |
| First-stage report | Read each check, finding, source, and coverage explanation in the original report; keep the file unchanged. | `first_report.json`, with its version specified by the request's `review_id` and `report_revision`. |
| Frozen Cell records | Verify the versions referenced by `affected_refs`, the attribution of errors, and the property scope. | `input/cell_record_evidence.json`. |
| Confirmation working notes | Save summary, pending items, and evidence with `save_confirmation_notes`; these indicate progress only. | Tool-generated `confirmation_notes.json`. |
| Independent confirmation result | Submit an assessment of the entire first-stage report with `write_confirmation`. | Tool-generated `confirmation.json` and a short JSON receipt. |
| Same-stage handoff reports | Read or save completed grounds, unresolved matters, and resumption points; these do not certify the report. | Reports in `handoffs/` or the tool-returned `handoff_path`. |

## 7. MCP Tools Used

| Tool | When to Call | What It Reads or Produces |
|---|---|---|
| `lookup_sources` | When independently checking external originals and their applications. | Source text or search results, still requiring mathematical verification. |
| `save_confirmation_notes` | When saving incomplete confirmation work, especially before a handoff. | `confirmation_notes.json`; it does not confirm the report. |
| `write_confirmation` | After verifying all actual check IDs, original report findings, and decisive steps. | Complete confirmation results and a short JSON receipt. |
| `budget_status` | When assessing remaining time and the closing window. | The current process's actual budget status. |
| `finish_handoff` | When unfinished, after saving the grounds. | A handoff receipt for the next verifier in the same stage. |

Use tools as actually needed. This stage reads the original report; it does not use `record_check`, `record_source`, or `write_report` to rewrite the first-stage review.
