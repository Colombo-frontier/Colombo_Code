---
name: manuscript-writing
description: Integrate a fixed ProofDraft and supplied source materials into a complete English theory manuscript, preserving exact Claims, scope, citations, and Lean evidence provenance. Return structured Markdown, LaTeX, bibliography, Claim mapping, and editorial gaps.
---

# Manuscript Writing

Write a coherent research article from the local `input.json`. Use its `proof` as the authoritative mathematical text and its source materials for supporting explanations and prior-work context. Earlier drafts do not override the fixed proof. Read only this input for local research content; paths mentioned inside it are provenance, not additional files to explore. Available web tools may be used to verify literature.

## Establish what can be claimed

Read the full proof, supplied source materials, required Claim IDs, and `lean_result` before deciding the article's contribution. Preserve the provided `proof_sha256` without recomputing it under a different serialization. Identify contradictions, missing support, and incomplete evidence in `editorial_gaps`.

Keep assumptions, quantifiers, Oracle, Algorithm Class, Guarantee, Resource, parameter ranges, probability statements, regime boundaries, constants, and actual logarithmic factors intact. Preserve the distinction between exact and asymptotic results, worst-case and expected cost, and uniform and pointwise guarantees. Shortening a statement must not broaden its scope. Do not combine bounds under incompatible assumptions.

Lean evidence concerns the exact formal declarations and dependencies recorded in `lean_result`. Compilation alone does not establish correspondence to an informal statement. Report a correspondence review only if the input contains one, and retain its limitations. Do not infer whole-paper formalization from a checked auxiliary lemma. The newly written manuscript has only your editorial self-check; the supplied checks do not automatically certify rewritten text.

## Build the argument for the reader

Choose the central research question and state the precise contribution supported by the materials. Explain why that contribution matters within its actual scope. Avoid unsupported priority or superiority claims, including "first", "optimal", and "state of the art". If the materials establish a useful partial result, explain that result and its remaining gap directly.

A theory article often benefits from an abstract, introduction, related work, Setting and notation, main results, proof ideas, technical development, limitations, and complete proof appendices. Adapt the structure to the argument; do not force an empirical section or an empty section. Produce complete prose, not an outline or concatenated drafts.

- Define the problem and the essential objects before stating results. Use one notation for each concept, and resolve notation collisions without changing meanings. Introduce any renaming clearly enough to compare the article with the source proof.
- State each theorem with its full assumptions and quantifiers. Explain the main obstacle, the proof's key idea, and the dependency between lemmas. Distinguish an intuitive proof sketch from the complete proof.
- Include the complete supporting argument in the article or its appendix. Internal file paths and source IDs are provenance, not replacements for definitions or proof steps. Preserve all necessary cases, boundary conditions, and dependencies when moving material.
- Compare results only under matched models, scopes, and success criteria. If a comparison table helps, expose differences and cite the exact source of each entry. Do not suppress a varying parameter or logarithmic factor to suggest a stronger improvement.
- Reuse sound explanations from supplied drafts, remove duplication, and make each paragraph advance the argument. Prefer explicit connections between statements over narration of how the research was conducted.
- Keep empirical motivation and conjectures separate from established mathematical results. Use only supplied experimental facts with their actual settings and uncertainty. Do not invent experiments to make the article look complete.
- Record new deductions, stronger statements, repaired gaps, or changed proof obligations as issues requiring mathematical verification. Do not adopt them during editorial revision.
- Write the abstract and conclusion after the body. Reconcile their claims with the theorems and limitations; a known unresolved case must remain visible.

## Ground the citations

Reuse checked source material in the input. When additional verification is needed and web tools are available, read the primary source supporting the specific attribution, comparison, or borrowed theorem. A search snippet or another paper's bibliography does not establish support. Confirm bibliographic metadata against the paper, publisher, or official repository, and retain a precise theorem/section/page locator when essential.

Create consistent BibTeX keys for real, checked references. Do not invent authors, titles, dates, identifiers, URLs, missing results, or source quotations. Omit optional unsupported claims; if missing support is essential, explain the limitation and list it in `editorial_gaps`. A self-contained result may have an empty bibliography. New external mathematical dependencies require verification before they can become part of the fixed proof.

## Return the manuscript

Return one final JSON object matching the supplied output schema:

- `proof_sha256`: the unchanged input digest.
- `manuscript_md`: the complete English article with full proofs or appendices and readable references.
- `manuscript_tex`: the same article as a complete LaTeX document, including preamble and document body. Use a portable article layout and standard mathematical packages. Define any custom macros locally; do not reference unavailable figures or other unpublished files.
- `bibliography_bib`: verified BibTeX entries cited by the article, or an empty string. When used, link the LaTeX bibliography to `references`. Every citation key must resolve, and both article versions must cite the same works.
- `claim_map`: exactly one `{claim_id, location}` entry for every supplied `required_claim_ids` entry, including the designated main Claim. Copy IDs exactly. Describe the concrete Markdown heading/theorem label and corresponding LaTeX label in `location`; verify both locations contain the required statement and supporting proof. Do not invent Claim IDs or add fields.
- `editorial_gaps`: concise unresolved issues, including essential unverified citations, conflicting source material, or proposed mathematical changes. An empty list means this writing pass identified no such gaps; it does not establish independent validation.

The host exports the standalone manuscript sources, `references.bib`, and Claim map. Keep internal IDs and runtime logs out of reader-facing prose unless their scientific role needs explaining. Do not invent author identities, funding, acknowledgments, acceptance dates, or publication metadata.

This workflow produces a manuscript draft with **uncompiled LaTeX**. It does not execute a LaTeX compiler or render a PDF. Formatting success has not been checked, and manuscript fidelity is `writer_self_check_only`. Do not describe the output as compiled, independently reviewed, or guaranteed ready for submission.

Before returning JSON, compare the abstract, result statements, tables, proof summaries, and conclusion with the fixed proof. Check full Claim coverage, notation consistency, citation resolution, and equivalence of the Markdown and LaTeX versions. Preserve limitations rather than improving them away. Return the complete requested contents directly; do not call a research submission tool or create follow-up research tasks.
