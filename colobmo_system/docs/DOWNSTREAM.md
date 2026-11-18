# Independent downstream Agents

Brain and Cells finish their normal workflow and export their existing report. They contain no Lean/writing phases, tools, configuration or records. `run.py` remains their unchanged entrypoint. The optional external `run_pipeline.py` performs a one-way file handoff:

```text
completed Brain exports -> handoff.json -> Lean Agent -> passed result -> Writing Agent
```

The launcher reads existing `research.json`, `proof_draft.json` and `output/final.md`, checks that the same complete adopted ProofDraft passed final review, and freezes a self-contained handoff.json. It never opens the Brain database or changes a Brain record. Explicit `--material` files may supply selected drafts/source text. Each Agent has its own instructions, runtime, workspace, process records and outputs. Neither imports Brain or Cell code, calls their tools, dispatches Tasks or sends work upstream.

## Usage

Use existing completed Brain output:

```powershell
python run_pipeline.py --brain-run runs/example --output-dir downstream_runs/example
```

Start Brain through its existing CLI, then hand off when it completes:

```powershell
python run_pipeline.py --brain-run runs/example --output-dir downstream_runs/example -- run path/to/goal.md
```

The launcher adds the matching `--run-dir`. Use `-- resume` similarly. Incomplete or failed Brain work stops the chain. Downstream output must be separate from the Brain run. `python run.py` directly still performs Brain research alone.

Each Agent can also run separately:

```powershell
python run_pipeline.py --stage lean --input handoff.json --output-dir downstream_runs/lean_only
python run_pipeline.py --stage writing --input handoff.json --lean-result downstream_runs/lean_only/lean/result.json --output-dir downstream_runs/writing_only
```

Writing validates the passed compiler/correspondence evidence and exact proof binding. Stage selection does not bypass feature switches. Downstream failure saves its own results and stops; no automatic upstream research/repair occurs.

## Configuration and execution

Only the launcher reads `downstream.toml`. Brain's `config.toml` has no downstream settings. `enabled=false` bypasses downstream work; `writing_enabled=false` stops after Lean. Writing instructions and config have no venue names or venue-selection fields.

Native model processes use read-only sandbox, no application plugins and no Colombo MCP server. Empty model/login settings use the existing native CLI settings. Instructions restrict research context to the supplied files. This removes service/write access to Brain and Cells; it is not a per-directory filesystem read jail. Scientific Memory and its independent writer are not wired into either Agent.

Provision Lean/lake and a pinned project once, and set `[lean].lean_project` to its absolute path. The reused compiler is `src/colombo/lean_agent/compiler.py`; accepted project/source formats and axiom policy are described in the Lean Skill. Dependencies are not silently installed. Missing environment returns `blocked` and suppresses Writing.

Default implementation allowances: Lean 1800 seconds, up to 3 candidate attempts, at most 120 seconds per compiler check; Writing 1800 seconds independently. Each Agent preserves its own input binding, deadline and receipts across replay. Changed inputs/config need a new output directory. Unsettled calls/stale locks require inspection rather than duplicate launch. Brain's integration clock remains unchanged.

## Ownership and outputs

- `agents/lean/`, `src/colombo/lean_agent/`: formalization, compiler-feedback repair, and internal fresh correspondence review. It does not call Brain Verifier. Pass requires full Claim coverage, proved declarations and permitted axiom dependencies. `lean/result.json` records the outcome; its `attempts/` contains sources, diagnostics and review evidence.
- `agents/writing/`, `src/colombo/writing_agent/`: organize checked research around question, contribution, Setting, assumptions, main results, Proof ideas, complete Proofs, notation, citations and limitations. It preserves Claim scope. Outputs: `writing/manuscript.md`, `manuscript.tex`, `references.bib`, `claim-map.json`, `result.json`.
- `src/colombo/downstream/`: file adapter, independent native process wrapper, sequential launcher. `pipeline.json` reports downstream status separately from Brain completion.

The Writing stage performs writer self-check only; it does not perform independent final mathematical review, LaTeX compilation, or PDF rendering. The default configuration requires a separately provisioned Lean project. Existing research may satisfy the Brain completion gate while failing the independent downstream handoff or formalization requirements; downstream failure preserves its own evidence and does not rewrite the research run.
