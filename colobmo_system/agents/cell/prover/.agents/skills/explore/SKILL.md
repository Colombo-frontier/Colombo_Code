---
name: explore
description: Cells and subcells independently use existing knowledge and original sources as needed to understand the background, broaden their ideas, discover proof techniques, compare routes, or check theorem applicability.
---

# Explore: Expanding Ideas and Material for the Current Task

## 1. Objective

Cells and subcells independently use explore according to the current Task to understand the background, discover related problems and proof techniques, compare routes, or verify external results.

Determine the direction of exploration, depth of reading, and when to return based on available material and budget. Follow promising leads further; when information is sufficient or further reading offers limited benefit, save useful insights and sources and resume the current work.

## 2. Inputs: What to Read Before Starting

| Material | Reading Requirements |
|---|---|
| `problem.md` and, when present, `TASK.md` | Confirm the current problem or the subcell's local research scope. |
| Current objective and relevant `proof_state` and Attempts | Understand existing routes, insights, query directions, and unresolved questions. |
| Existing Sources, Claims, and Arguments | Verify source versions, reading coverage, and existing applicability assessments to avoid redundant searches. |

Start searching from topics, intuitions, or questions relevant to the Task, and refine queries and direction as you read. Explore background, related problems, methods from other fields, and transferable constructions, or seek justification for a proof gap. Before adopting a result, verify its definitions, assumptions, quantifiers, and scope of applicability.

Reuse relevant records already read, select directions worth extending, and retrieve additional material selectively when needed. See the workspace [protocol.md](../../../protocol.md#records-and-audits) for records and audits.

## 3. Procedure: Finding and Applying Material

### 3.1 Follow Leads to Original Sources

Search the current Memory through the builtin `scientific_memory(mode="search", arguments_json=...)`. Use only kinds and facets exposed by the current schema; explicitly set include_leads=true to discover leads. First examine scope, match checks, evidence, and use_hint, then use read with the full ref to retrieve the content, or expand to follow authorized links. A search hit does not establish applicability. See `.agents/skills/scientific-memory/GUIDE.md` for specific parameters; a full Memory ref cannot be used as a retrieve/archive record ref.

When external material is needed, use `lookup` to search papers, original author sources, or standard references, or to read a known URL. If search is disabled for the current task and external material is necessary, enable it with `configure` under the protocol. Scientific Memory is local read-only retrieval and does not depend on the external search switch.

By default, `lookup(query=...)` uses Serper to return titles, URLs, and snippets; first select sources worth reading, then use `lookup(url=...)` to obtain their text through Jina Reader. When both are provided, URL takes precedence; `limit` controls only the number of search results. The outer configuration selects the provider, and the existing arXiv search and direct URL reader remain configurable options. The service manages credentials; do not read API keys or write separate API requests. Inspect the actual provider, read coverage, and warnings returned; retain the limitation if reading fails, and do not treat a snippet as the full text.

Save useful references as Sources, retaining the title, authors, URL or bibliographic identifier, version, theorem or section/page locations, associated objectives, and intended use that were actually verified. State whether the material actually read was the full text, a specific section, an abstract, or a search snippet; preserve any limitation caused by inaccessible text or an unpublished proof.

Before applying a theorem, read its complete statement and relevant definitions. The original proof of an external theorem need not be stored or reproved; read the necessary proof sections when transferring its method or investigating a specific concern. Search summaries cannot replace verification against the original text; save the precise statement, applicability conditions, and a locatable source so that the verifier can return to the original.

### 3.2 Check How the Material Applies to This Problem

New insights, questions, route comparisons, and Source references may remain in the Attempt. Before using an external result in a proof, complete the following applicability check and records.

Match the objects, definitions, assumptions, and quantifiers in the source to those of the current problem, and explain which conditions are satisfied and which still need proof. For direct applications, derive the target from the source result; for partial transfers, identify the role of additional assumptions, the steps that cannot be transferred, and the components that remain reusable.

Place the complete extracted statement in the fixed `proposition` of a Claim, using `citation` under the protocol to reference its Source and original location. Having a citation does not mean verification is complete, nor does registering a citation require reproving the original theorem. Store the application or transfer argument in an Argument, with `conclusions` referencing the proposition actually established for this problem and `dependencies` referencing the theorem used and necessary sources; store reusable constructions in Examples. Create a new Claim for a conclusion under additional assumptions rather than marking the original objective proved. Background or inspiration does not constitute a proof of the current problem; submit the final source locations with the manuscript under the protocol.

## 4. Constraints: Limits on Permissible Conclusions

- Search snippets, abstracts, URLs, or source registration do not establish verification of a complete theorem; retain the actual reading coverage and accessibility limitations.
- Background inspiration and results under additional assumptions cannot directly certify the original objective; audit the actual application Argument and Example properties under the protocol.
- Use `retrieve` to check `current_trust` before reusing evidence; do not infer current usability from historical passing labels.
- A subcell reads only local records and authorized `context/` snapshots; obtain new sources through tools rather than searching ancestor or sibling directories for material.

## 5. Outputs: Findings That Remain Useful

Save useful Source references and concise insights, distinguishing directly applicable material, material requiring additional assumptions, inspiration only, and unverified material; retain questions worth further thought.

When further queries no longer advance the work, the Attempt records the directions actually covered, the scope of unproductive queries, and specific obstacles, such as inaccessible originals, inconsistent definitions, missing key assumptions, methods that cannot be transferred, or an audit that did not confirm the result. Record budget exhaustion and tool failures separately as execution causes. Failure to find a result does not imply that it does not exist, and a theorem's inapplicability does not imply that the target is false.

Save this use of `skill`, `decision_reason`, and output references in the Attempt. The main agent updates `proof_state` for changes to the overall route; when a handoff is needed, preserve unread sources and conditions awaiting verification using `$handoff`.

## 6. Relevant Record Objects

Locate local objects through `retrieve` and fixed references; save only material or arguments actually obtained.

| Object (Collection) | Use and Read/Write Behavior at This Stage | Entry Point |
|---|---|---|
| Source `sources` | Store bibliographic identifiers, versions, original locations, actual reading coverage, and intended use. | Actual sources returned by `lookup`, existing Source references, or `retrieve`. |
| Claim `claims` | Store the complete fixed statement of an external theorem and associate its Source through `citation`; do not assign proved status yourself. | `archive` / `archive_result` receipts and current target references. |
| Argument `arguments` | Store the application or transfer derivation for this problem, conclusion relations, and dependencies used; audit when complete. | Fixed record references. |
| Example `examples` | Store reusable constructions and properties when available, and audit the claims under the protocol. | Sources of constructions actually read and archiving receipts. |
| Attempt `attempts` | Store query directions, skill selection, reading limitations, failure scope, and next steps. | Current `proof_state` references or `retrieve`. |
| `proof_state` | Read current routes and gaps, and return findings relevant to the route. | `retrieve(kinds=["proof_state"])`. |
| `reviews` | Read audit results for application arguments or properties; maintained by the service. | `audit` receipts or relevant record references. |

## 7. MCP Tools Used

Invoke tools as actually needed; tool parameters and rules for sources and audits are governed by the workspace `protocol.md`.

| Tool | When to Call | What It Reads or Produces |
|---|---|---|
| `retrieve` | When beginning retrieval or reusing local sources or evidence. | Existing records, fixed-version contents, and `current_trust`. |
| `lookup` | When external literature searches or reading a known URL are needed. | Search results or original text; state the actual accessible scope when saving. |
| `scientific_memory` | When consulting knowledge exposed in this mode in shared Long-Term Memory. | Candidates, fixed content, and authorized dependencies; it neither creates task records nor upgrades evidence status. |
| `configure` | When checking search status, or when search is disabled and external material is necessary. | This task's configuration and an explanation of its effects; state the reason for enabling search. |
| `archive` | When saving or revising an individual Source, Claim, application argument, or Attempt. | A fixed-version receipt. |
| `archive_result` | Optionally, when multiple related outputs need to be saved together. | A batch of records and mapping to official references. |
| `audit` | When a complete application Argument or Example property needs to serve as audited evidence. | Local audit results; registering a citation does not itself require reproving the external theorem. |
| `budget_status` | When assessing remaining time for reading and saving. | The current time allowance; switch to `$handoff` when concluding. |
