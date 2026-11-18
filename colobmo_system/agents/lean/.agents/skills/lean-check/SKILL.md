---
name: lean-check
description: Independently formalize a frozen ProofDraft in Lean 4, use compiler feedback to repair it, and review statement correspondence before handing a passed package to Writing Agent.
---

# Independent Lean Check

Read `input.json` and the supplied output schema. The package contains the ProofDraft, fixed Setting, exact required Claim IDs, proof hash, and selected materials. Work only in the current stage. Return final JSON; the runner writes it and manages the compiler loop. There are no Brain, Cell, or MCP submission tools.

## Formalization mode: `lean-check`

Translate every required Claim, including the designated main Claim, into a named Lean theorem. The mapping associates `claim_id`, fully qualified `declaration`, and `correspondence` explaining its exact location and meaning in the source ProofDraft. Preserve definitions, quantifier order, domains, assumptions, Oracle, Algorithm Class, Guarantee, Resource, parameter dependencies and regimes. Preserve endpoints, strictness, rounding, uniform constants, and probability versus expectation. A finite example cannot replace a parameterized Bound.

Supporting Lemmas may use different Proof steps. Do not weaken a conclusion, assume the desired result, introduce inconsistent premises or an empty domain, or substitute a trivial proposition. If faithful formalization reveals a mathematical gap, report it as a limitation. Do not change the frozen ProofDraft or create a research Task.

The runner provides a provisioned pinned Lean project and compiles each returned source. Search installed mathlib with `rg` when useful; verify declaration types, namespaces and hypotheses. Prefer applicable library Lemmas. Use the supplied `previous_feedback` to distinguish parser/elaboration errors, missing instances or imports, coercions, and unresolved mathematical obligations. Suitable proof-producing tactics include `simp`, `rw`, `ring`, `linarith`, `nlinarith`, `omega`, and `norm_num`; choose them from the actual goal. Keep theorem signatures mathematically fixed during repair.

Submit one self-contained `Main.lean` as the JSON `source` string. Imports are limited to `Init`, `Lean`, and `Mathlib`; include local definitions in this file. Do not submit `#` commands, attributes, notation/macros/elaborators, custom commands, `native_decide`, `run_tac`, `run_meta`, `unsafe`, custom axioms, `sorry`, or `admit`. Only `maxRecDepth` and `maxHeartbeats` resource options are supported. The runner creates audit commands independently and checks transitive axioms. It requires theorem proofs; `def C : Prop := ...` is not a proof of C.

Return `status=candidate` only with full required Claim coverage, valid source, and no remaining limitations. Return `status=incomplete` with useful partial source, its exact mapping subset, and explicit remaining obligations when the allotted attempts or scope make completion infeasible. Always preserve the supplied `proof_sha256`. Model statements that compilation succeeded are not evidence.

## Correspondence-review mode: `lean-review`

This is a fresh model invocation after actual compiler success. Inspect the frozen mathematics, submitted source, mapping, printed theorem declarations, and compiler/axiom evidence. Do not accept the author's mapping assertions alone. Review every required Claim, including composition steps, and verify quantifiers, definitions, domain nonemptiness, assumptions, parameter dependence, regimes and conclusions. Reject stronger assumptions, weaker rates, tautologies, target-equivalent premises, or omitted dependencies. Do not repair source in this stage.

Return `verdict=pass` only with all required IDs in `checked_claim_ids` and no findings. Otherwise return `fail` with precise findings. This is model review of informal-to-formal correspondence, not a machine proof of that correspondence. The complete Lean Check passes only when both compiler/axiom checks and this review pass on the same source and ProofDraft.

The allowed axiom set is any subset of `propext`, `Classical.choice`, and `Quot.sound`. Imported gaps or compiler-trust axioms block pass even when the source has no visible placeholders. Missing toolchains/dependencies and timeouts remain explicit infrastructure or incomplete outcomes. Writing Agent receives only a fully passed package and must preserve its checked statements.

For official references and optional tooling, read [references/sources.md](references/sources.md). External services are optional; no installation is required by this Skill.
