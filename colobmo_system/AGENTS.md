# Workspace instructions

- Active source: Colombo System. See README.md and SOURCE_LAYOUT.md for entry points and source responsibilities.
- Preserve instruction/workflow/storage identities and exact scientific record/review hashes unless the requested change requires a reviewed migration.
- Keep long_term_memory/ and .long_term_memory_state/ together. Brain/proof Cells have read-only scientific_memory; Experiment/Verifier/Recovery have no live Memory reader.
- The independent nested colombo_memory_agent defaults to this system's Store. Its publication workflow remains separate from the proof scheduler.
- Brain/Cells export their normal results and finish. Independent Lean/Writing Agents consume files through run_pipeline.py; downstream stages/tools/records do not belong in Brain.
- Writing instructions contain academic writing principles; venue-specific requirements come from the current task.
- Do not commit credentials, workstation configuration, generated run directories, model transcripts, or local validation output.
