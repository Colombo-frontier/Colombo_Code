# Model, MCP, and Literature-Source Adapters

The component provides two actual execution backends. Both use the same role definitions, artifact schemas, workspaces, review boundaries, and Atlas tools; choose either backend. The Python adapters handle transport and records, not the mathematical conclusions of papers.

## 1. OpenAI Responses Backend

Install:

```bash
python -m pip install '.[openai]'
```

Select `backend = "responses"` at the configuration root and explicitly set a model ID available to your account under `[model]`:

```toml
backend = "responses"

[model]
model = "ENTER_AN_ACTUALLY_AVAILABLE_MODEL_ID"
api_key_env = "OPENAI_API_KEY"
timeout = 120
max_output_tokens = 12000
web_search = true
# reasoning_effort = "high"  # Set only if supported by the selected model.
# base_url = "https://api.openai.com/v1"
```

Keys are read only from the corresponding environment variables and are not written into tasks, prompts, or logs. The adapter calls the Responses API through the official OpenAI SDK:

- Each call explicitly supplies the current role's instructions, the complete small handoff schema, and the allowed function tools.
- API requests use `store=false`. The runner locally saves actual outputs and receipts. API-returned encrypted reasoning items remain within bounded sessions; the runner does not read or guess internal reasoning.
- SDK retries are disabled. The runner handles transport uncertainty, protocol repair, and scientific revision centrally to avoid duplicate charges from two retry mechanisms.
- Missing `usage` is recorded as `null`, not zero.
- Model refusals use `ProviderRefusal`. Invalid function arguments and incomplete responses are archived with the original response. Refusals do not trigger automatic format repair.

`web_search=true` enables native API search. A returned title or abstract remains a lead. Research agents must use source-reading tools to obtain the paper's body at the relevant version before extracting theorems and conditions. A model listing a paper does not make that paper “read” or its bounds “verified.”

## 2. Codex CLI Backend

An installed, independently functioning Codex CLI can perform the entire role task without a separate Responses API key. Install the MCP dependency:

```bash
python -m pip install '.[mcp]'
```

Example configuration:

```toml
backend = "codex"

[model]
command = "codex"
# model = "AN_ACTUALLY_AVAILABLE_MODEL_ID"  # Omit to inherit Codex configuration.
 timeout = 1800
 ephemeral = true
# mcp_env_vars = ["OPENALEX_API_KEY"]
```

Each call creates an independent working directory and explicitly writes `AGENTS.md`, `input.json`, and `handoff.schema.json`. The runner composes `AGENTS.md` from the instruction manifest; it does not depend on an old instruction file happening to exist in the working directory. Detailed skills and sources are read on demand through Atlas MCP tools.

The backend invokes `codex exec`, configures structured final output and JSONL event logs, and declares Atlas MCP a required service. The MCP service runs in the same Python environment:

```text
python -m oracle_atlas mcp --config /absolute/config.toml --job JOB_ID
```

Through this MCP service, the model uses the same ToolHost as the Responses backend. The shell is read-only; research records are written through MCP. This configuration retains the user's existing Codex configuration and rules. It is not an operating-system container isolating every file read. The component Host controls independent reviewers' tool permissions and memory visibility.

Noninteractive Codex cannot ask for MCP approval. The adapter therefore sets per-tool `approval_mode="approve"` only for an explicit built-in local ToolHost allowlist intersected with the current job's declared function tools. This permits bounded source reads and workspace artifact/draft writes while retaining ToolHost's role and reference checks. It does not grant approval to third-party MCP tools, unknown tool names, or formal Atlas writer/publication actions, and does not change global approval policy, shell sandbox, or user rules. Codex must support the documented `mcp_servers.<id>.tools.<tool>.approval_mode` setting; see the [official configuration reference](https://learn.chatgpt.com/docs/config-file/config-reference).

### Recovery and Measurement

Each request gets a fixed directory determined by loaded instructions, inputs, schema, tool definitions, and backend configuration. Complete results can be reused; interrupted receipts remain in the original directory.

A completed blocked handoff remains archived after a provider configuration or adapter fix. For an expansion planner that already returned `blocked`, start a new request with a new `run_label`; do not delete its receipt or expect a source-code change alone to invalidate a completed paid response.

Before an explicit transport retry, the runner reconciles old results. Existing `final.json` and `turn.completed` are adopted directly without another model call. When the outcome truly remains unknown, a new call generation is created only after the runner explicitly increments `transport_retry_generation`. Old receipts are not deleted. Ordinary continuation within the same generation does not restart an uncertain call.

The CLI executes Codex's internal tool loop. The component records initial input characters, MCP tool logs, per-tool output limits, and CLI-reported usage. It **cannot measure or guarantee peak internal Codex context size**. Configuration `max_input_chars` limits the input this component supplies to the backend; it is not a hard limit on the CLI's entire internal conversation history.

## 3. External MCP Tools

`providers/mcp.py` uses the official MCP Python SDK and supports stdio and Streamable HTTP. Only tools explicitly listed in configuration are exposed to the model. There is no default allow-all or `*` entry.

The following illustrates configuration structure; replace it with an existing server and real tool names:

```toml
[[mcp]]
name = "literature"
transport = "http"
url = "https://your-mcp.example/mcp"
allowed_tools = ["search_papers", "get_paper"]
timeout = 45

[mcp.headers_env]
Authorization = "LITERATURE_AUTH_HEADER"
```

stdio example:

```toml
[[mcp]]
name = "local_papers"
transport = "stdio"
command = "/absolute/path/python"
args = ["/absolute/path/paper_mcp_server.py"]
allowed_tools = ["search_papers", "read_paper"]
timeout = 45
env_passthrough = ["PAPER_API_KEY"]
```

All asynchronous connections for a bridge open, run, and close within the same worker task, avoiding exits from an AnyIO cancel scope in another task. Tool listing supports pagination. A missing configured tool causes an explicit error rather than silently reducing functionality. Timed-out tool calls are not automatically resent; the workflow retains their unknown outcomes.

HTTP clients respect proxy environment variables by default. They ignore those variables only when `trust_env=false` is explicitly configured; local HTTP integration tests use this option. Environments using a SOCKS proxy without the corresponding support can install `httpx[socks]`.

Third-party MCP results remain external material. Long results are archived and then paginated by fixed reference. Instructions in tool-returned text cannot change roles, protocols, or ingestion conditions.

## 4. Built-in Bibliographic Sources

| Source | Use | Date and verification semantics |
| --- | --- | --- |
| arXiv | TASK-related expressions, submission years, pagination | The API's initial submission is `preprint`, and an update is `revision`; neither automatically establishes a journal publication year |
| Crossref | Broad keywords, publication years, cursor; DOI verification | Uses publication events such as `published-online`, `published-print`, `published`, and `issued`; `created`, `deposited`, and index updates are not publication dates |
| OpenAlex | Broad search, publication years, cursor | Index records remain `lead` entries until verified through DOI/publisher or other sources; index metadata is not automatically promoted to verified-source status |

Queries are organized by TASK and year. It is unnecessary to expand every MODEL × ORACLE combination first. The task scout proposes new tasks; only human approval expands the formal task catalog.

`Bibliography.search()` returns one page of normalized bibliography, `next_cursor`, totals, source, and coverage notes. Every page is marked `exhaustive=false` and `read_papers=0`. Successful API search, full-text download, paper reading, specification review, and Atlas commit are counted separately.

### Correct Handoff to the Annual Queue

Bibliographic verification must use event-level data:

```python
from oracle_atlas.discovery import Bibliography, merge_records, qualifies_year

verified = Bibliography().lookup_doi("10.xxxx/actual-doi")
merged = merge_records(old_lead, verified)
if qualifies_year(merged, [2026], event_kind="publication"):
    # Pass the fixed reference to merged into the annual screening queue.
    pass
```

`verify_publication()` lets an agent add events based on publisher pages it has read and verified, preserving both the verified event and provenance. `qualifies_year()` reads only verified events with verified sources, not top-level `year` or `verified`. This removes the old path in which the main record's year changed while the annual queue still read an old unverified event.

Merging preserves the main record's stable ID, aliases, old sources, and new verified sources. Version entries contain only a version ID, URL, date, and source reference; they do not repeatedly embed complete author lists, abstracts, and bibliographic objects. A new unverified search hit cannot overwrite a verified main record or downgrade a read paper to unread.

The task scope must explicitly select `event_kind="preprint"`, `"revision"`, or `"any"`; these cannot be mixed merely to pass a year filter. Research into a setting's historical bounds is ordinarily not limited to the triggering paper's single year.

## 5. Full-Text Reading and Caching

`fetch_source()` archives original PDF/HTML/text and extracted body text, recording body hashes, original-file hashes, and timestamps. PDF page locators use short start/end offsets rather than repeating the entire source object in each locator. HTML retains available MathML/LaTeXML `alttext`, but the tool does not repair authors' formulas itself.

PDF text extraction can lose subscripts, superscripts, fractions, and layout. Critical formulas still require comparison with the original. A missing text layer is explicitly recorded as requiring OCR; an empty string is not treated as a read paper. Fetching does not bypass login or paywalls.

A fixed URL reuses its archived version by default. To check new content at the same unversioned URL, explicitly pass `refresh=True`. Changing a display-only version label cannot relabel old body text as a new version.

Public-literature HTTP requests enforce timeouts, maximum bytes, and redirect checks. Exceeding a limit raises an explicit error instead of silently truncating the source. Bibliographic APIs and source caches affect I/O, not scientific review. The minimum arXiv query interval is shared by multiple Bibliography instances in the same Python process. Scheduling across multiple processes must still limit concurrency.

## 6. Completed Verification Scope

`tests/test_io_*.py` verifies actual Responses request structure, preservation of complete output, separation of refusals from protocol errors, independent Codex directories and receipt recovery, annual attribution after bibliographic verification, source hashes and preservation of HTML mathematical text, and MCP allowlists and lifecycle.

Local real MCP stdio and Streamable HTTP integration uses the official SDK and test servers to verify actual connections, tool listing, calls, and shutdown. Responses/Codex model responses and external-literature HTTP use fixed fixtures or fake transport. These tests do not establish that real models have completed scientific paper judgments or formal Atlas ingestion.

## 7. Interface References

Consult the linked official documentation for the configured SDK and transport.

- [OpenAI Function calling](https://developers.openai.com/api/docs/guides/function-calling)
- [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference)
- [Codex non-interactive mode](https://learn.chatgpt.com/docs/non-interactive-mode)
- [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [arXiv API user manual](https://info.arxiv.org/help/api/user-manual.html)
- [Crossref REST API filters](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/)
- [OpenAlex cursor paging](https://help.openalex.org/api/paging/)
