# Lean Check references

This is a Colombo-specific skill written for a bounded post-Brain Check stage; no third-party skill or MCP server is installed by it.

## Primary documentation

- [Lean language reference: Axioms](https://lean-lang.org/doc/reference/latest/Axioms/): describes axiom tracking, `sorryAx`, and the additional trust introduced by native evaluation. Use the reference matching the pinned Lean version when behavior differs from the current manual.
- [Lean community: Did you prove it?](https://leanprover-community.github.io/did_you_prove_it.html): explains why successful compilation, checked build targets, a standard-axiom dependency set, and statement correspondence are separate requirements. This motivates separate compiler and correspondence evidence in Colombo.
- [Lean projects](https://leanprover-community.github.io/install/project.html) and [mathlib cache documentation](https://github.com/leanprover-community/mathlib4/blob/master/Cache/README.md): explain project dependency setup and cached builds. Colombo fixes the project revisions before checking; the ordinary upstream update instructions are not a repair step.
- [Mathematics in Lean: Using Theorems and Lemmas](https://leanprover-community.github.io/mathematics_in_lean/C02_Basics.html#using-theorems-and-lemmas): practical search by source, API documentation, Loogle, and `apply?`, followed by checking the actual declaration type.

## Original workflow references

- [Cameron Freer's lean4-skills](https://github.com/cameronfreer/lean4-skills/blob/main/plugins/lean4/skills/lean4/SKILL.md): useful patterns are library search, incremental feedback, preserving statement signatures during proving, and distinguishing a file check from a project build. Colombo uses those ideas in a short local instruction rather than importing its plugin, command suite, hooks, and workflow state.
- [lean-lsp-mcp](https://github.com/oOo0oOo/lean-lsp-mcp): optional interactive goal/diagnostic inspection and theorem search. It still requires a working Lean project. Neither MCP output nor external search replaces compilation of the submitted source snapshot.

## Minimal acceptance contract

1. Bind the accepted ProofDraft/review revision, source hash, required Claim IDs, and explicit required theorem names before a final check.
2. Record submitted source hashes, Lean version, pinned toolchain/dependency files, compiler command, exit status, diagnostics, and elapsed time. Rebuild changed local imports; never accept stale artifacts.
3. Generate the audit in Controller-owned code. Every required name must resolve to a proved proposition. Capture its elaborated type and transitive axiom set in a fresh process; require only the three allowed standard axioms. Missing output or an unrecognized output format is inconclusive.
4. Check complete required coverage and preserve the correspondence review status separately. Stronger assumptions, changed quantifiers, changed arithmetic domains, vacuous domains, or altered Oracle semantics need review even when the axiom audit is clean.
5. Distinguish verified, incomplete formalization, compilation failure, unavailable environment, and timeout. No missing-tool or partial-coverage result advances manuscript writing as a full Lean Check pass.

These are acceptance design requirements, not evidence that a particular run has passed. The host runtime owns the concrete submission schema and gate implementation.
