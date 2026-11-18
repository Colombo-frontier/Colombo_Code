---
name: extract-setting
description: "Extract recoverable eight-axis setting specifications, views, and shared facts for both labeling systems from one paper, saving candidates with source locations."
---

# Setting Extraction Agent Skill

## Extraction steps

1. Read `standards/eight_axes.md` and `standards/labels.md`, then the paper's fixed source references. Locate task definitions/information models/guarantees/costs before tracing required theorem appendices. Search by equation number or term as needed rather than putting all papers into context at once.
2. List the common contracts actually studied in the paper, placing differences such as algorithmic randomness in views where possible. Do not merge different native oracles, tasks, models, or metrics because they have the same rate. Initially assign initialization and step-size conditions to the witness; place them in the common specification only when they define common information or protocol.
3. Write recoverable statements for every axis: objects, variable blocks, norms, domains, views, operations, and sources. Expand both layers of a two-level oracle separately. Do not omit online timing, sample reuse, oracle-choice permissions, costs, or aggregation order. Identify exactly which condition is unknown rather than writing generic "standard assumptions."
4. Generate scoped tag_facts from the specification. Use vocabulary_lookup for existing concept definitions/parents; preserve proposed new concepts and raw statements. Check task parent classes, the object to which Exact applies, and every native operation, avoiding seven unclassified axes or precision assembled across different operations.
5. Distinguish extraction omissions, source ambiguities, and theorem-proof/cost-accounting issues. Faithfully recorded literature uncertainties may proceed with the candidate to extraction review. If a core interface is unknown, record an explicit identity blocker rather than inventing a known interface.
6. For each candidate, write a draft in chunks, verify JSON Pointers/references, and freeze it before submitting extraction references. Use draft_patch for large fields; do not put entire sources or the subsequent identity stage's full-library index into a candidate.
7. A revision task repairs only the specified candidate. Preserve superseding relationships and the basis for partial resolution of old issues, along with existing progress for unselected candidates from the same paper. Await an independent extraction_reviewer; do not approve your own work.
