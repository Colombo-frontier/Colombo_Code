# Independent Proof Scope Review

Literature_grounded_discovery separates mathematical dependencies from surrounding profile context when considering a prior independent proof credential. A catalog verifies material identity and provenance; it does not establish mathematical validity.

| Review path | Required evidence | Current reviewer action |
| --- | --- | --- |
| Unchanged certified proof reuse | A controller-verified independent credential, unchanged proof and dependencies, and complete issue scope | Confirm eligibility, review current applications, and list verified reused references |
| Independent scope revalidation | A controller-listed stable proof and mathematical dependencies with changed surrounding context | Read the prior credential and actual changes, assess applicability and issues independently, and issue a current credential |
| Full affected proof review | Changed proof, source, dependency, or assumption; absent credential; undeclared dependence; or substantive counterexample | Verify the affected mathematics and necessary original sources in full |

## Read the controller catalog

Inspect `proof_scope_revalidation_candidates` in the current proof context. A candidate binds the prior independent review, current and previous proposals and profiles, scientific-material fingerprint, context digests, leaf-level `context_changes`, and relevant issue occurrences. Read complete pointed-to material whenever the summary is insufficient.

A review of a listed candidate may include:

```json
{
  "proof_scope_revalidations": [
    {
      "proof_ref": "ACTUAL_PROOF_REF",
      "candidate_id": "ACTUAL_CURRENT_CANDIDATE_ID",
      "changes_reviewed": true,
      "reason": "Describe the changed context, relevant issues, and applicability actually checked."
    }
  ]
}
```

Replace these explanatory placeholders with actual catalog values. Also supply a current `proof_approvals` credential for the same proof, complete issue scopes, and `proof_reuse_context_ref` bound to the current job's `proof_context_ref`. A revalidated proof does not belong in `reused_proof_refs`.

Declining a candidate does not waive scientific review, adopted-bound defect checks, or execution-check declarations. For a job with listed scope candidates, approval of an active bound supported by an affected proof requires complete current `proof_issue_scopes`, even if the reviewer chooses full review without optional reuse credentials.

## State complete mathematical assumptions

The `standalone_proposition_explicit_context` credential requires `/common_specification` and every necessary mathematical definition: parameter domains, variables, blocks, norms, quantifiers, oracle assumptions, and cost assumptions. Its dependency scope does not implicitly include the entire `/parameters` array.

The `standalone_proposition` scope remains conservative. Moving to explicit context requires inspecting the prior context and explaining why excluded fields are irrelevant. It cannot discard a real assumption or describe unknown dependencies as complete.

## Review issues and adoption

Assess copied issue occurrences against their actual lineage. Copying an unchanged record does not itself create new scientific evidence, while different meanings of an issue ID still require separate assessment. Examine new counterexamples and scope or resolve them correctly.

Direct source, proof, and result defects remain blocking for dependent claims. Changed mathematical dependencies require affected review. Narrowing a contextual scope cannot hide such defects.

The final reviewer approves active bounds and their current applications, joint-parameter checks, comparisons, and the frozen five-file bundle. Required oracle-simulation and branch checks use actual execution receipts. Keep software validation, real-paper scientific judgments, and Atlas ingestion receipts distinct.
