---
name: coordinate-scan
description: "Organize paper scanning within approved tasks, years, sources, and budgets, using persistent state to arrange continuation or exception handling."
---

# Coordinator Agent Skill

## Working method

1. Verify this run's user objective first: whether the year means formal publication or preprint year, the approved TASK scope, and any specified journals/conferences or paper limit. When information is incomplete, use defaults supplied by the invocation context and state them in notes; do not invent an approved catalog that was not provided.
2. Form broad search directions from task formulations, conventional names, and synonyms. Select complementary bibliographic sources, official publication catalogs, and available search capabilities. Give each task a finite query budget and preserve gaps that remain after cross-source deduplication. New tasks produce proposals only; do not expand the approved scope of this run.
3. Read short persistent-queue summaries, distinguishing verified bibliography, read papers, pending extraction, pending materials, reviewed records, and committed records. Reuse completed artifacts during recovery; do not rescan/re-extract every paper because of one exception.
4. Reconsider routing only for exceptions authorized in this invocation: unknown native specification -> targeted materials/specification revision; an uncertain individual bound -> quarantine that result and continue independent evidence; protocol error -> repair with the schema and diagnostics; actual scientific-version conflict -> recheck affected comparisons. Repeated invocations without new materials do not replace research progress.
5. Read plan with schema_read, save it, and return a small handoff. On budget exhaustion, describe completed responsibilities and remaining gaps. An ended run is not necessarily a completed objective; never claim that Atlas was updated without an intake receipt.

## References on demand

`standards/identity.md`: identity routing or critical unknowns; `standards/evidence.md`: exception/review scope; `standards/profile.md`: completion and intake counts. Delegate other scientific details to the relevant role rather than loading every standard.
