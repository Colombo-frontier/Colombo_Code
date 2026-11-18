# Literature_grounded_discovery: Project Rules

This is a standalone component for paper discovery and Atlas maintenance. Its scientific standards come from setting-discovery practice. Colombo supplies only the architectural separation of roles, protocols, skills, tools, and memory.

## Responsibilities and execution entry points

- `agents/<role>/AGENTS.md`: the role's responsibilities, methods, and boundaries.
- `protocol.md` and each role's `protocol.md`: immutable references, outputs, decision scope, recovery, and collaboration.
- `agents/<role>/skills/*/SKILL.md` and `standards/`: detailed methods, loaded as needed.
- `src/oracle_atlas/runtime/instructions.py` explicitly loads responsibilities and protocols and records the actual file hashes. Do not infer the active instructions from Codex's current directory.
- Component skills are project resources, not skills that must be installed into a personal skill directory. Do not duplicate the complete scientific standards in Python strings.

## Implementation requirements

The LLM determines mathematical specifications, identity, applicability, proofs, and complexity brackets. Python handles fields, references, permissions, budgets, versions, queues, and transactions. Do not replace scientific judgment with keyword rules or predetermined test conclusions.

When changing an interface, update its schema, actual tool registration, Agent protocol, and an end-to-end path together. A raw model response is not a valid handoff. Record rejected outputs separately; do not repeatedly reuse the same invalid cached response.

Retain complete archives, but provide only references and short catalogs as stage inputs. Never automatically expand an entire dependency graph, annual bibliography, or the complete Atlas into a prompt. Reviews use independent sessions and share only frozen formal artifacts and sources.

Preserve stable setting/view IDs and aliases. Tags support initial retrieval only. Unknown information is not a conflict. A new setting requires model-based identity verification and an independent review. Document approval and the adoption scope of individual bounds are distinct.

Use professional English for current component documentation, skills, runtime explanations, and reader-facing setting profiles. Profiles must be self-contained and must not depend on historical audit snapshots. Preserve compatibility identifiers and immutable source evidence; translating prose must not change scientific meaning or operational behavior.

After changes, run `python -m pytest`, `python scripts/check_resources.py`, and the offline end-to-end demo. Report real-model, network, and actual Atlas-commit acceptance separately. Synthetic tests cannot substitute for scientific acceptance on real papers.
