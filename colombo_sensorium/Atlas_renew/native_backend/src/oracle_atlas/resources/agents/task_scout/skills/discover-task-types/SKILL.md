---
name: discover-task-types
description: "Read broadly in oracle-related literature to identify mathematical tasks absent from the approved catalog and propose task expansions for human review."
---

# Task Type Discovery Agent Skill

## Working method

1. Read the TASK definition in `standards/eight_axes.md` and the approved task catalog as needed. Use atlas_catalog to paginate the short Atlas catalog when useful. Compare formulations, not whether a label name appears novel.
2. Search broad oracle/black-box/query-complexity terms together with relevant optimization, estimation, and decision terminology; then read representative literature selectively. Search responses are leads only. At minimum, verify the original task definitions supporting a proposal.
3. For each proposal, describe the input/instance, queried object, objective and solution concept, output, and interaction protocol; explain why existing tasks cannot express it naturally, and whether it is a refinement, neighbor, or distinct task relative to the closest existing task. New oracle/model variants may be referred to research within an existing task; do not disguise them as new tasks.
4. Supply reusable broad queries, synonyms, and representative source references. Reasons to investigate a new task may include a systematic omission, important applications, or theoretical structure. Failure to find a lower bound does not automatically establish an open problem.
5. Merge synonymous proposals, rank by expected value and coverage gaps, and save an English report. Specify which papers' definitions were verified, which are unread leads, and which catalog changes require human approval.
6. Read schema_read(task_proposal), save the artifact, and return a small handoff. Do not start annual production scans for these new tasks before human approval.
