# Colombo: A Frontier-to-Frontier Autoresearch System for Oracle-Based Optimization

**Formulate problems, investigate complexity gaps, verify findings, and preserve knowledge for further discovery.**

[Paper](https://arxiv.org/abs/2611.23080) · [Quickstart](#quickstart) · [API keys](#authentication-and-api-keys) · [Configuration](#configuration) · [Atlas](#sensorium-and-complexity-atlas) · [Citation](#citation)

Colombo is a self-organizing AI research system for **oracle-based optimization**. It studies how efficiently a problem class can be solved through a prescribed information interface, and which costs every admissible algorithm must incur. Algorithms establish achievable **upper bounds**; hard-instance constructions establish unavoidable **lower bounds**. The gap between them defines a concrete research frontier.

Two mechanisms drive the system: **Self-Organization** adapts research programmes as evidence accumulates, while **Adversarial Co-Ascent** develops algorithms and hard families through reciprocal challenge. Independent review, Lean-based formal certification, and scientific memory support the transition from individual investigations to subsequent research programmes.

The [accompanying paper](https://arxiv.org/abs/2611.23080) reports optimal or near-optimal rates for more than fifty settings and describes 56 research works. This repository provides the system source, scientific memory, Sensorium tools, and Complexity Atlas data. Local research runs and model transcripts are excluded from the source distribution.

## Contents

- [How Colombo works](#how-colombo-works)
- [Research highlights](#research-highlights)
- [Repository layout](#repository-layout)
- [Installation](#installation)
- [Authentication and API keys](#authentication-and-api-keys)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Run your own research problem](#run-your-own-research-problem)
- [Monitor, resume, and understand results](#monitor-resume-and-understand-results)
- [Standalone Cells and experiments](#standalone-cells-and-experiments)
- [Lean certification and paper composition](#lean-certification-and-paper-composition)
- [Scientific Memory](#scientific-memory)
- [Sensorium and Complexity Atlas](#sensorium-and-complexity-atlas)
- [Troubleshooting](#troubleshooting)
- [Further documentation](#further-documentation)
- [Citation](#citation)

## How Colombo works

### Frontier-to-frontier research

The **Complexity Atlas** records mathematically specified settings, their relationships, and the current state of knowledge. For a selected setting, the **Setting Profile** fixes the task, instance class, oracle, admissible algorithms, resource measure, success criterion, and known bounds. Its **Complexity Bracket** expresses the remaining question:

$$
L_s(\varepsilon,\delta;\theta)
\;\leq\;
N_s^*(\varepsilon,\delta;\theta)
\;\leq\;
U_s(\varepsilon,\delta;\theta).
$$

Here, $N_s^*$ is the optimal complexity under the declared model; $\varepsilon$, $\delta$, and $\theta$ specify accuracy, failure probability, and problem parameters. Improving an algorithm can lower $U_s$; a stronger hardness argument can raise $L_s$. Both sides must refer to the same assumptions and parameter regime.

![Colombo architecture: Sensorium, Brain, specialized Cells, verification, formal certification, paper composition, and Long-Term Memory](https://arxiv.org/html/2611.23080v1/figures/colombo-architecture.png)

*The paper's system architecture: frontier sensing supplies a Setting Profile; supported findings inform subsequent investigations.*

| Component | Role |
| --- | --- |
| **Sensorium** | Maps settings and complexity gaps; prepares Setting Profiles through literature discovery, structural exploration, and Atlas maintenance. |
| **Brain** | Plans research programmes, dispatches Tasks, integrates reviewed results, maintains the Live Complexity Bracket, and replans around the remaining gap. |
| **Research Cells** | Investigate upper bounds, lower bounds, general proofs, and experiments. |
| **Independent Verifiers** | Review Cell results and the exact final adopted proof, with decisions bound to the relevant claims and evidence. |
| **Formal Certification** | Uses Lean compilation, axiom checks, and claim-correspondence review to assess formalized results. |
| **Paper Composer** | Organizes accepted downstream material into a manuscript with proofs, references, and claim mappings. |
| **Scientific Memory** | Preserves sources, theorems, algorithm families, hard families, and reusable research knowledge. |

**Released execution paths.** `run.py` starts Brain/Cell research and independent natural-language review. Lean and Writing are separate downstream Agents launched through `run_pipeline.py`. Sensorium tools and the Memory Agent have their own entry points. An ordinary Brain run does not automatically launch Atlas maintenance or publish Memory records. The figure describes the overall research architecture; the commands below specify the actual execution boundaries.

### Self-Organization

![Self-Organization across field, programme, and problem levels](https://arxiv.org/html/2611.23080v1/figures/self-organization-frontier-compact.png)

Self-Organization connects three levels of inquiry:

- **Field level:** the Sensorium identifies settings, maps bounds, and locates unresolved gaps.
- **Programme level:** the Brain forms candidate rates and technical routes, assigns subproblems, and revises its plan using reviewed evidence.
- **Problem level:** Cells investigate concrete claims, constructions, counterexamples, and experiments.

Partial progress and failed approaches can change the next assignment as well as a successful proof. Accepted discoveries can refine existing settings or motivate new ones, connecting progress within a programme to renewal of the research frontier.

### Adversarial Co-Ascent

![Adversarial Co-Ascent: algorithms and hard families improve through reciprocal challenge](https://arxiv.org/html/2611.23080v1/figures/adversarial-co-ascent-evolution.png)

Adversarial Co-Ascent makes **algorithm design** and **hardness construction** inform one another. Algorithms probe candidate hard families for exploitable structure; hard instances expose limitations in how candidate methods obtain and use information. These challenges guide stronger constructions, sharper conjectures, and new questions.

An experiment can reveal a useful pattern or failure mode. Establishing a complexity bound still requires a proof over the declared model class and parameter regime. Empirical evidence, independent natural-language review, and formal certification have distinct roles.

## Research highlights

The paper's [Research Outcomes](https://arxiv.org/html/2611.23080v1#S3) section describes the following programmes. Its statements and appendix specify the oracle models, assumptions, parameter regimes, and remaining gaps.

| Area | Selected focus |
| --- | --- |
| **Zeroth-order optimization** | Lower bounds and matching characterizations under specified value-oracle and query-domain assumptions. |
| **Randomized first-order optimization** | Accuracy exponents for smooth nonconvex optimization under fixed finite-order smoothness. |
| **Variational inequalities** | Higher-order algorithms and lower bounds, including stochastic weak-Minty sample-complexity limits. |
| **Stochastic bilevel optimization** | Accuracy limits and smoothness-dependent complexity under fresh, globally unbiased first-order samples. |
| **Nonconvex minimax optimization** | Complexity across stochastic, finite-sum, and full-Hessian information models. |
| **Geometry and matrix computation** | Hyperbolic optimization, simplex-based matrix games, and low-rank approximation. |

These are reported research outcomes, rather than a guarantee that a new run will reproduce them or solve an arbitrary submitted problem. The bundled Atlas provides setting-level records, sources, and exports.

## Repository layout

```text
Colombo/
├── README.md
├── colobmo_system/                 # Brain/Cell research system
│   ├── run.py                     # New run, configuration preview, status, resume
│   ├── run_cell.py                # Standalone Cell
│   ├── run_pipeline.py            # Optional independent Lean → Writing pipeline
│   ├── config.toml                # Brain/Cell parameters and resource profiles
│   ├── downstream.toml            # Separate Lean/Writing parameters
│   ├── requirements.txt
│   ├── agents/                    # Role instructions, protocols, and skills
│   ├── src/colombo/               # Implementation
│   ├── long_term_memory/          # Scientific libraries
│   ├── .long_term_memory_state/   # Paired indexes and pinned scientific state
│   ├── colombo_memory_agent/      # Independent extraction, review, publication
│   ├── docs/
│   └── tests/
└── colombo_sensorium/
    ├── Complexity_altas/           # Atlas records, browser, and exports
    ├── Literature_grounded_discovery/
    ├── Structural_exploration/
    └── Atlas_renew/
```

Use the existing directory spellings **`colobmo_system`** and **`Complexity_altas`** in commands. Unless otherwise stated, the working directory below is **`Colombo/colobmo_system/`**.

## Installation

### Prerequisites

| Requirement | Used for |
| --- | --- |
| **Python 3.11+** and `pip` | System runtime and dependencies. |
| **Git** | Downloading the repository. |
| **Codex CLI** with working model access | Native agent processes. |
| **Node.js/npm**, if using the installation below | Installing Codex CLI. |
| **Service credentials**, as applicable | Literature retrieval and hosted experiments. |
| **Lean/lake and a pinned Lean project**, optional | Downstream formal certification; not required for ordinary Brain/Cell research. |

Install Codex CLI if needed:

```sh
npm install -g @openai/codex
codex --version
codex login
```

See the [Codex CLI documentation](https://developers.openai.com/codex/cli) for platform-specific installation and authentication. Confirm that your selected model is available to your account or provider.

### macOS / Linux

```sh
git clone https://github.com/WU-Wendao/Colombo.git
cd Colombo/colobmo_system
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install -r colombo_memory_agent/requirements.txt
```

### Windows PowerShell

```powershell
git clone https://github.com/WU-Wendao/Colombo.git
Set-Location Colombo/colobmo_system
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pip install -r colombo_memory_agent/requirements.txt
```

Check that `py -3` selects Python 3.11 or newer. If shell policy prevents activation, use `.\.venv\Scripts\python.exe` in place of `python` in subsequent commands; activation is only a convenience.

On Windows, the launcher needs the **native `codex.exe`**. If discovery selects an npm `.cmd` wrapper, configure `[runtime].codex_bin` with the actual executable path; see [runtime paths](#runtime-paths).

## Authentication and API keys

Model access, literature retrieval, and hosted experiments are separate services. **Codex login does not supply Serper, Jina, or hosted Experiment API keys.**

| Component | Credential | When needed |
| --- | --- | --- |
| **Brain / Cells / Verifiers** | Existing Codex authentication, or `OPENAI_API_KEY` with a compatible native CLI setup | Every live research run. Current preflight checks for file-backed `auth.json` or `OPENAI_API_KEY`. |
| **Serper search** | `SERPER_API_KEY` | Default Brain/Cell literature lookup: `search_provider = "serper"`. |
| **Jina reader** | `JINA_API_KEY` | Default Brain/Cell source reader: `reader_provider = "jina"`. |
| **Hosted Experiment** | `OPENAI_API_KEY` | OpenAI Responses API / Code Interpreter execution, separate from native CLI login and usage. |
| **Lean / Writing / Memory Agents** | Native Codex authentication | When these optional agents run. Lean also needs its compiler/project configuration. |
| **Static Atlas browser** | None | Browsing the bundled data locally. |

Obtain keys from your [OpenAI API account](https://platform.openai.com/api-keys), [Serper account](https://serper.dev/), or [Jina account](https://jina.ai/), depending on the services you enable.

### Set credentials in the launching shell

Set only the variables for services you use. Replace these placeholders with your own keys.

**macOS / Linux:**

```sh
export OPENAI_API_KEY='YOUR_OPENAI_API_KEY'
export SERPER_API_KEY='YOUR_SERPER_API_KEY'
export JINA_API_KEY='YOUR_JINA_API_KEY'
```

**Windows PowerShell:**

```powershell
$env:OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'
$env:SERPER_API_KEY = 'YOUR_SERPER_API_KEY'
$env:JINA_API_KEY = 'YOUR_JINA_API_KEY'
```

These set variables for the current shell and its child processes. Launch Colombo from that shell. The system does **not** automatically load a general `.env` file. Keep real credentials out of goals, reference materials, TOML configuration, and commits.

Brain resolves its authentication directory from `[runtime].auth_home`, then `CODEX_HOME`, then the user's `.codex` directory. `auth_home` points to the directory containing the existing login/configuration, not to an API key string.

### Minimal service configuration

The Quickstart uses a smaller configuration that needs only working native Codex model access. In a **copy of the complete configuration**, change these existing entries:

```toml
profile = "standard"

[cell.settings.network]
search_provider = "arxiv"
reader_provider = "direct"
api_key_file = ""
theorem_search_url = ""

[cell.settings.experiment]
enabled = false
```

This is an **edit guide, not a complete configuration**. Preserve the other fields and edit existing tables instead of appending duplicate tables. Retain the Experiment `model` and other fields even when experiments are disabled.

The arXiv/direct combination requires no Serper/Jina keys, with different coverage from general web search and Jina. Retrieved text and metadata are not verified theorems. Brain literature lookup uses these providers and is controlled by `[brain].search_enabled`; native Brain web search is disabled. Native Cell web search follows the Cell search settings and CLI backend.

### Custom model providers

Native agents can inherit provider settings from your existing Codex configuration. Current research preflight still expects file-backed login or `OPENAI_API_KEY`; an arbitrary provider-specific environment variable alone does not satisfy that check.

Hosted Experiment uses **`https://api.openai.com/v1`**. A custom Codex `base_url` does not redirect it. Supply an OpenAI API key and an available Experiment model, or disable hosted experiments.

## Quickstart

This example asks Colombo to recover a small, known result in deterministic query complexity. It demonstrates the workflow rather than reproducing the paper's research portfolio. A live run consumes model usage and has no fixed completion-time guarantee.

### 1. Make a local configuration

From `colobmo_system/`:

```sh
# macOS / Linux
cp config.toml config.local.toml
```

```powershell
# Windows PowerShell
Copy-Item -LiteralPath config.toml -Destination config.local.toml
```

Edit `config.local.toml` using the [minimal service configuration](#minimal-service-configuration): select `standard`, use `arxiv`/`direct`, and disable hosted Experiment. Leave Brain/Verifier/Audit model fields empty to use existing native defaults, or select models supported by your backend. Keep Cell `reasoning_effort` nonempty; the standard value is `medium`.

### 2. Create `goal.md`

Save this Markdown as `goal.md` in `colobmo_system/`:

```markdown
# Exact deterministic query complexity of ordered search

## Setting
Let n >= 2 be known. An unknown integer theta belongs to {1, ..., n}.

## Oracle
One query chooses q in {1, ..., n - 1} and returns the bit [theta <= q].
Queries may be chosen adaptively. Algorithms are deterministic.

## Goal
Determine the exact minimum worst-case number of oracle queries needed
to identify theta correctly for every possible value of theta.

## Required output
- State an algorithm and prove its worst-case upper bound.
- Prove a matching lower bound for every admissible deterministic algorithm.
- Handle non-power-of-two values of n explicitly.
- Give a self-contained proof with the exact integer rounding.

## Scope
Count only oracle queries. Do not introduce noise, randomized error,
average-case cost, or additional information about theta.
```

### 3. Inspect the effective configuration

```sh
python run.py config --config config.local.toml
```

The JSON output should identify `mode: "preview_only"`, `creates_run: false`, and `profile: "standard"`. Check the resolved model, search, experiment, and allocation settings. This command neither starts a model nor creates a run; it does not test API-key validity or connectivity.

### 4. Prepare, then start

```sh
python run.py run goal.md --config config.local.toml --run-dir runs/ordered-search --prepare-only
python run.py resume --run-dir runs/ordered-search
```

`--prepare-only` creates the run and freezes its inputs without starting research. **Use `resume` to start that prepared run.** Do not issue another `run` command with the same nonempty directory.

Alternatively, start a fresh run directly:

```sh
python run.py run goal.md --config config.local.toml --run-dir runs/ordered-search-direct
```

### 5. Inspect progress and outputs

From another terminal in the same system directory and Python environment:

```sh
python run.py status --run-dir runs/ordered-search
```

Once produced, open `runs/ordered-search/output/final.md` for the report, `proof/current.md` for the adopted proof, and `research.json` for progress and reviews. A newly prepared run does not yet have a finished proof.

Only a run whose current goal passes the final acceptance gate is `completed`. Interrupted, partial, and failed attempts retain their evidence for inspection and possible continuation.

## Configuration

### Files, profiles, and precedence

| File | Controls |
| --- | --- |
| [`colobmo_system/config.toml`](colobmo_system/config.toml) | Brain, Cells, Verifiers, research allocations, literature access, and experiments. |
| Complete alternative selected with `--config` | Replaces the Brain configuration file; it is not a partial overlay. |
| [`colobmo_system/downstream.toml`](colobmo_system/downstream.toml) | Independent Lean and Writing Agents only. |
| Your existing Codex configuration | Native authentication/provider settings and inherited model defaults. |

The shipped selection is **`profile = "hard"`**. `standard` uses the base tables. `hard` applies `[profiles.hard.*]` differences on top of them.

**With `hard` selected, editing only a base field may have no effect if the hard profile overrides it.** Switch to `standard` or edit the corresponding `[profiles.hard.*]` entry, then preview the resolved configuration.

`--config` belongs after the `run` or `config` subcommand:

```sh
python run.py config --config config.local.toml
python run.py run goal.md --config config.local.toml --run-dir runs/my-research
```

`status` and `resume` do not accept `--config`. Resume uses the run's recorded configuration source. Standalone `run_cell.py` also has no `--config` option; it reads the system's `config.toml`.

### Research allocations

These values describe the shipped configuration, not a promise of runtime or API cost.

| Parameter | Standard | Hard | Meaning |
| --- | ---: | ---: | --- |
| `limits.max_rounds` | 3 | 8 | Maximum research Waves. |
| `limits.max_dispatches_per_wave` | 3 | 6 | Cell dispatches per Wave, including supplementary dispatches. |
| `limits.max_parallel_cells` | 2 | 4 | Concurrent outer Cells, separate from Subcell concurrency. |
| `cell.settings.agents.prover_max_rounds` | 3 | 15 | Cell-local Prover starts. |
| `cell.settings.agents.verifier_max_rounds` | 3 | 20 | Cell-local Verifier starts. |
| `cell.settings.agents.report_check_max_attempts` | 2 | 4 | Checker attempts per report version. |
| `cell.settings.parallel.max_subcells` | 4 | 8 | Subcell concurrency per parent. |
| `cell.settings.parallel.max_depth` | 1 | 2 | Subcell nesting depth. |
| `cell.settings.experiment.max_runs` | 6 | 12 | Hosted experiment allowance in its owning task. |
| `integration.timeout_seconds` | 7200 | 7200 | Shared time for final integration and review in one integration stage. |

Research has **no run-wide deadline or global model-call cap**. Waves and dispatches bound outer allocation; Cells, reviews, Subcells, and experiments have additional local limits. The nominal outer dispatch ceiling is Waves × dispatches per Wave, not a bound on all model calls or total cost. Resume preserves cumulative usage. Final integration/review does not consume a Wave dispatch.

To customize the smaller profile, edit the existing entries:

```toml
profile = "standard"

[limits]
max_rounds = 3
max_dispatches_per_wave = 3
max_parallel_cells = 2
```

All TOML blocks here are fragments to edit within the complete file. Preserve its other fields.

### Models and reasoning effort

| Role | Base configuration | Behavior |
| --- | --- | --- |
| Brain | `[brain]`: `model`, `reasoning_effort` | Empty standard values inherit native CLI defaults. |
| Result/final Verifier | `[verifier]`: `model`, `reasoning_effort` | Empty values inherit Brain settings. |
| Audit | `[audit]`: `model`, `reasoning_effort` | Empty values inherit Brain settings. |
| Cell | `[cell.settings.model]`: `name`, `reasoning_effort` | Empty name can inherit the native model; effort must be nonempty. |
| Hosted Experiment | `[cell.settings.experiment]`: `model`, `reasoning_effort` | Independent API model/effort; does not inherit the native CLI model. |

The shipped hard profile selects `gpt-6-astra` with `ultra` effort for Brain, Verifier, Audit, and Cells. Hosted Experiment uses `gpt-6-astra` with `medium` effort under standard and `max` under hard. These are repository settings: choose combinations actually supported by your backend. They need not match the model used in the paper's investigations.

For example, with `standard` selected, edit the existing tables:

```toml
[brain]
model = "YOUR_AVAILABLE_NATIVE_MODEL"
reasoning_effort = "YOUR_SUPPORTED_EFFORT"
search_enabled = true

[cell.settings.model]
name = "YOUR_AVAILABLE_NATIVE_MODEL"
reasoning_effort = "YOUR_SUPPORTED_EFFORT"
```

Replace the placeholders before running. With `hard`, edit `[profiles.hard.brain]`, `[profiles.hard.verifier]`, `[profiles.hard.audit]`, and `[profiles.hard.cell.settings.model]` instead.

### Runtime paths

Usually the system discovers Python, native Codex, and existing authentication. If necessary, edit:

```toml
[runtime]
python = ""
codex_bin = "C:/path/to/codex.exe"
auth_home = "C:/path/to/your/codex-home"
```

Use real absolute paths for your machine; leave an override empty for normal discovery. On macOS/Linux, select the installed native executable. On Windows, do not select `codex.cmd` or `codex.bat`. `auth_home` should contain the existing configuration and file-backed login.

Standalone Cells have their own discovery. If overrides are needed, set `CELL_CODEX_BIN` and `CELL_AUTH_HOME` in their launching environment; Brain's `[runtime]` overrides are not the standalone interface.

### Search and experiments

| Setting | Purpose |
| --- | --- |
| `[brain].search_enabled` | Enables Brain literature lookup through the configured search/reader providers. |
| `[cell.settings.network].search_provider` | `serper` for the default service, or `arxiv` for key-free arXiv retrieval. |
| `[cell.settings.network].reader_provider` | `jina` for the default service, or `direct` for direct retrieval. |
| `[cell.settings.network].prover_search_enabled` | Cell Prover search. |
| `[cell.settings.network].subcell_search_enabled` | Subcell search: false under standard, true under hard. |
| `[cell.settings.experiment].enabled` | Allows new hosted experiments. |
| `[cell.settings.experiment].max_runs` | Hosted run allowance. |
| `[cell.settings.experiment].max_tool_calls` | Tool-call allowance per hosted request. |
| `[cell.settings.experiment].memory_limit` | Hosted container memory selection. |

For Serper/Jina, supply both keys in the environment. The shipped `api_key_file` is empty; an explicitly configured key file is an alternative, not a required repository file.

To enable hosted experiments after Quickstart, set `enabled = true`, provide `OPENAI_API_KEY`, and select an API model supporting the requested tools. See the [Experiment Cell guide](colobmo_system/agents/experiment_cell/README.md) for the native researcher and hosted execution workflow.

## Run your own research problem

### Write a precise goal

| Include | Questions to answer |
| --- | --- |
| **Task and instance class** | What must be computed or proved? Which functions, operators, or instances are admissible? |
| **Oracle / feedback** | What can an algorithm query? What does it learn? Is feedback exact, noisy, stochastic, or stateful? |
| **Geometry and regularity** | What are the domain, dimension, smoothness, convexity, and other assumptions? |
| **Algorithm model** | Are adaptivity, randomization, memory, or communication restricted? |
| **Resource measure** | Queries, samples, rounds, memory, or another cost? Worst-case or expected cost? |
| **Success criterion** | What accuracy and failure probability are required, over which parameter regimes? |
| **Known results and target** | Which bounds are established? What gap remains? What counts as progress or completion? |

Brain can complete a Setting Specification from the materials, but must preserve your mathematical problem. State assumptions and requirements that must not change.

### Attach reference materials and requirements

```sh
python run.py run goals/my-problem.md --config config.local.toml --run-dir runs/my-problem --material references/background.md --material references/prior-proof.tex --criterion "Track all parameters and state every assumption in the final theorem."
```

Replace the example paths with existing files. Repeat `--material` or `--criterion` for additional inputs. Prefer readable Markdown, plain text, or LaTeX for mathematical source material; consult component guides for other formats.

Inputs are copied into the run. Include the supporting files needed to understand references: a local link to an unprovided file is not a complete research package. Task assignments and packages are fixed for each attempt. A changed goal or new assignment material should become a new run/Task rather than silently replace the evidence behind an existing one.

The default workflow permits near-optimal results with logarithmic/polylogarithmic gaps under its stated conventions. If you require exact constants, exact integer complexity, or a fully matching rate, state that explicitly in the goal and criteria.

## Monitor, resume, and understand results

### Status and recovery

```sh
python run.py status --run-dir runs/my-problem
python run.py resume --run-dir runs/my-problem
```

`status` reports current state and rebuilds exported views from the authoritative store; it is not strictly read-only. `resume` continues or reconciles the existing run, retaining Tasks, attempts, evidence, and cumulative usage. It does not award a fresh allocation.

**Ctrl+C** interrupts the controller and preserves committed work. It is **not a guaranteed stop of all active computation**: durable Cell processes may continue after the controller detaches. Inspect status before resuming and do not start two controllers for one run. The CLI has no general `pause`/`stop` command or pause-marker workflow.

Keep the selected configuration file available. Changes may be adopted at a safe resume boundary; pending calls, audits, tool jobs, or active Cells can prevent adoption. Resolve those executions first rather than deleting state or blindly resubmitting requests whose outcome is unknown.

### Important outputs

Paths are relative to your `--run-dir`:

| Path | Contents |
| --- | --- |
| `input/goal.md`, `input/materials/` | Supplied goal and copied references. |
| `input/setting.json` | Fixed Setting Specification, once established. |
| `research.json` | GoalProgress, Tasks, Waves, bounds, reviews, and audits. |
| `proof_draft.json` | Adopted proof versions and final review. |
| `working_notes.json` | Optional research notes. |
| `proof/current.md` | Current adopted proof. |
| `output/final.md` | Final report and completion/certification status. |
| `state.sqlite` | Authoritative internal records; use system tools rather than editing it. |

Exports appear as the corresponding stages produce them. A process ending, a partial claim being accepted, or a draft existing does not establish full completion. Check status and the final review tied to the adopted proof. Natural-language acceptance remains distinct from a passed Lean downstream result.

### Reconcile an already-reviewed final result

For an **ended run affected by stale completion metadata**:

```sh
python run.py reconcile-final-review --run-dir runs/my-problem
```

This checks existing final-proof/review bindings and, when eligible, appends corrective progress/conclusion records without model calls. It preserves the proof, reviews, open questions, and usage. It is idempotent, not a proof-repair command or a way to bypass unresolved work. See the [system guide](colobmo_system/README.md).

## Standalone Cells and experiments

Use a standalone Cell for a focused problem that does not need Brain-level coordination:

```sh
python run_cell.py goal.md --run-dir runs/my-cell --research-mode oracle_complexity --specialization general
python run_cell.py --run-dir runs/my-cell --check
python run_cell.py --run-dir runs/my-cell --resume
```

Standalone Cells read **`colobmo_system/config.toml`**, not the `config.local.toml` selected for a Brain run. Apply your model, search, and Experiment settings there before starting one. The default standalone mode is `generic`; specify `--research-mode oracle_complexity` for this example. Consult `--help` and the [Cell guide](colobmo_system/agents/cell/README.md) for other supported options.

The Experiment Cell performs empirical investigation with its own records and review. Hosted execution requires the separate API key described above. Experiments can guide conjectures or expose failure modes, but their reports do not by themselves certify a mathematical bound or near-optimality claim.

## Lean certification and paper composition

The optional downstream workflow is:

```text
completed Brain exports → frozen handoff → Lean Agent → passed result → Writing Agent
```

It is a separate launcher, not an implicit stage of `run.py`. It consumes exported files without modifying Brain/Cell records. Incomplete research stops the chain; downstream acceptance has its own checks.

### Configure the Lean environment

Provision Lean/lake and a project with pinned compiler/dependency versions. Edit the existing `[lean]` section of [`downstream.toml`](colobmo_system/downstream.toml):

```toml
[lean]
lean_project = "/absolute/path/to/your/lean-project"
lake_bin = "lake"
max_compile_attempts = 3
compile_timeout_seconds = 120
timeout_seconds = 1800
```

On Windows, use an absolute path such as `C:/research/my-lean-project`. Dependencies are not silently installed. A missing environment produces a blocked downstream result and prevents Writing. Set the separate `[model]` section if these Agents need different native CLI settings.

The top-level `enabled` switch controls downstream work; `writing_enabled = false` stops after Lean. These settings belong in `downstream.toml`, not Brain's `config.toml`.

### Start downstream work

For an existing completed Brain run:

```sh
python run_pipeline.py --brain-run runs/my-problem --output-dir downstream_runs/my-problem
```

Or start a fresh Brain run and hand off after completion:

```sh
python run_pipeline.py --brain-run runs/new-problem --output-dir downstream_runs/new-problem -- run goal.md --config config.local.toml
```

The launcher supplies the matching Brain `--run-dir`. Arguments after `--` are Brain arguments; a launcher-level `--config` selects the separate downstream configuration. Keep downstream outputs separate from the Brain run.

| Downstream output | Contents |
| --- | --- |
| `handoff.json` | Frozen input package and proof binding. |
| `lean/result.json`, `lean/attempts/` | Formalization outcome, sources, compiler diagnostics, and review evidence. |
| `writing/manuscript.md`, `writing/manuscript.tex` | Manuscript drafts. |
| `writing/references.bib` | Bibliography. |
| `writing/claim-map.json` | Mapping between manuscript claims and checked material. |
| `pipeline.json` | Downstream status, separate from Brain completion. |

Writing performs its own self-check; it does not add an independent mathematical review, compile LaTeX, or render a PDF. Downstream failure retains its evidence and does not automatically send a repair task to Brain. See [requirements and standalone stages](colobmo_system/docs/DOWNSTREAM.md).

## Scientific Memory

The release includes four scientific libraries: **sources, theorems, algorithm families, and hard families**. Brain and proof Cells read them through `scientific_memory`. The bundled dataset contains **388 published records and 43 leads** at this release; record status and supporting provenance remain important when reusing a result.

Keep **`long_term_memory/` and `.long_term_memory_state/` together**. The hidden directory contains required indexes, pinned scientific objects, and review/publication state. Verifier, Recovery, and Experiment have no live Memory reader.

The independent [`colombo_memory_agent/`](colobmo_system/colombo_memory_agent/README.md) performs extraction, curation, independent review, and publication against the parent system's Store. It is not launched by the proof scheduler. Its `stage_only` jobs can extract and review without publishing; publication is an explicit operation governed by the component's review and authorization checks.

See [Memory usage](colobmo_system/docs/MEMORY.md) for reading behavior and [review identity and privacy](colobmo_system/docs/MEMORY_PRIVACY_PUBLICATION.md) for the bundled publication projection.

## Sensorium and Complexity Atlas

The Sensorium package includes native records for **425 settings**, static browsing pages, and PDF/TeX/Markdown exports at this release.

### Browse without running agents

From the **repository root** (`Colombo/`):

```sh
python -m http.server 8000 --bind 127.0.0.1 --directory colombo_sensorium/Complexity_altas
```

Open [http://localhost:8000/](http://localhost:8000/). This local static server needs no model credentials. Press Ctrl+C to stop the server.

### Discovery and maintenance tools

| Component | Purpose | Guide |
| --- | --- | --- |
| **Complexity Atlas** | Browse setting records, scientific history, and exports. | [Atlas guide](colombo_sensorium/Complexity_altas/README.md) |
| **Literature-grounded discovery** | Find papers, extract settings, review bounds independently, and maintain the Atlas. | [Discovery guide](colombo_sensorium/Literature_grounded_discovery/README.md) |
| **Structural exploration** | Explore neighborhoods of existing settings and propose related complexity questions. | [Exploration guide](colombo_sensorium/Structural_exploration/README.md) |
| **Atlas renewal** | Maintain existing profiles through bounded research, joint bracket analysis, independent review, and native adoption. | [Renewal guide](colombo_sensorium/Atlas_renew/README.md) |

These components have their own environments, configuration, entry points, and publication gates. Follow their guides rather than applying Brain's `config.toml`. Proposals and Atlas adoption are separate operations; begin maintenance with an Atlas copy as directed by the relevant guide.

## Troubleshooting

| Symptom | What to check |
| --- | --- |
| `colombo_system` directory not found | The released name is **`colobmo_system`**. |
| Missing Python modules | Activate the intended environment and install both requirements files from Installation. |
| Codex cannot be found, or Windows selects a wrapper | Set `[runtime].codex_bin` to the native executable; standalone Cells use `CELL_CODEX_BIN` for an override. |
| `No file login or OPENAI_API_KEY` | Point `auth_home` to the existing file-backed login, or configure API authentication in the launching environment. |
| Literature search/reading fails | Check `SERPER_API_KEY` / `JINA_API_KEY`, or select `arxiv` / `direct`. Variables must reach the launching process. |
| Hosted Experiment reports a missing key | It needs `OPENAI_API_KEY` independently of Codex login. Supply it or disable new hosted experiments. |
| Model or effort unavailable | Choose a supported combination; inspect hard-profile overrides and the separate Experiment model. |
| A model or limit edit appears ignored | A `[profiles.hard.*]` value may override the base table. Inspect the resolved configuration. |
| `--config` rejected | Supported by `run.py config` and `run.py run`, not `resume`, `status`, or `run_cell.py`. |
| Run directory already nonempty | Resume it or choose a new directory. This includes directories created by `--prepare-only`. |
| Resume refuses changed configuration | Finish/reconcile active and pending work before adopting new settings. Preserve state and counters. |
| Run ended without a completed proof | Inspect status and the exact final review. Exhausted allocation or a partial result does not imply full completion. |
| Completed Brain run fails downstream handoff | The current adapter also requires a single exported conclusion and no open questions in the adopted ProofDraft. Retained open questions or reconciliation history can prevent handoff; inspect the diagnostics and preserve the original records. |
| Lean blocked or Writing did not start | Provision the pinned Lean environment and inspect `lean/result.json`; Writing needs passed Lean evidence and a valid handoff. |
| Figures do not load | Images are linked from versioned arXiv HTML. Open the [paper PDF](https://arxiv.org/pdf/2611.23080) if the image host is unavailable. |

For syntax, use `python run.py --help`, `python run.py run --help`, `python run_cell.py --help`, and `python run_pipeline.py --help` from the system directory.

## Further documentation

- [System setup and workflow](colobmo_system/README.md)
- [Source layout](colobmo_system/SOURCE_LAYOUT.md)
- [Cell workflow](colobmo_system/agents/cell/README.md)
- [Experiment Cell](colobmo_system/agents/experiment_cell/README.md)
- [Scientific Memory](colobmo_system/docs/MEMORY.md)
- [Independent Memory Agent](colobmo_system/colombo_memory_agent/README.md)
- [Lean and Writing Agents](colobmo_system/docs/DOWNSTREAM.md)
- [Sensorium package](colombo_sensorium/README.md)

## Citation

If Colombo informs your research, please cite the [paper](https://arxiv.org/abs/2611.23080):

```bibtex
@misc{zhang2026colombo,
  title         = {Colombo: A Frontier-to-Frontier Autoresearch System for Oracle-Based Optimization},
  author        = {Haihan Zhang and Wendao Wu and Chenheng Zhang and
                   Chunyuan Zheng and Yanyi Li and Cong Fang and
                   Haoxuan Li and Zhouchen Lin},
  year          = {2026},
  eprint        = {2611.23080},
  archivePrefix = {arXiv},
  primaryClass  = {cs.AI},
  url           = {https://arxiv.org/abs/2611.23080}
}
```
