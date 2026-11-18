"""Thin native Codex CLI agent adapter: each job/request has a separate working directory, and the same Host exposes tools through MCP."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import threading

from .base import ProviderError, Reply
from ..discovery.http import atomic_write


# Only these local ToolHost operations may receive noninteractive permission.
# Actual availability is further restricted to the current job's definitions.
# Third-party MCP names and formal Atlas publication are deliberately absent.
LOCAL_JOB_TOOLS = frozenset({
    "work_list", "vocabulary_lookup", "resource_read", "schema_read", "target_schema_read",
    "artifact_get", "artifact_put", "draft_create", "draft_read", "draft_patch",
    "draft_validate", "draft_freeze", "memory_save", "memory_search", "source_read",
    "source_search", "bibliography_search", "source_fetch", "paper_verify", "atlas_catalog",
    "atlas_search", "atlas_read", "draft_clone", "read_batch",
})


def _local_approval_overrides(tools: list) -> dict:
    names = {tool.get("name") for tool in tools
             if isinstance(tool, dict) and tool.get("type") == "function"
             and isinstance(tool.get("name"), str)
             and re.fullmatch(r"[a-z][a-z0-9_]*", tool["name"])
             and tool["name"] in LOCAL_JOB_TOOLS}
    return {f"mcp_servers.oracle_atlas.tools.{name}.approval_mode": "approve"
            for name in sorted(names)}


class CodexUncertain(ProviderError):
    """The process was interrupted or returned abnormally; tool side effects may already exist, so do not rerun automatically."""


class CodexBackend:
    def __init__(self, config: dict, *, popen=None):
        self.config = dict(config)
        self._local = threading.local()
        self._popen = popen or subprocess.Popen

    def bind_job(self, job: dict, config: dict):
        if not job.get("id") or not config.get("config_path") or not config.get("workspace"):
            raise ProviderError("CodexBackend requires bound job.id, config_path, and workspace.")
        if not Path(config["config_path"]).is_file():
            raise ProviderError("The configuration file does not exist; Atlas MCP cannot start.")
        generation = (job.get("state") or {}).get("transport_retry_generation", 0)
        if not isinstance(generation, int) or isinstance(generation, bool) or generation < 0:
            raise ProviderError("transport_retry_generation must be a nonnegative integer.")
        self._local.job, self._local.runtime = dict(job), dict(config)
        self._local.generation = generation

    def complete(self, instructions: str, input_items: list, tools: list, output_schema: dict) -> Reply:
        job = getattr(self._local, "job", None)
        if job is None:
            raise ProviderError("bind_job must be called before CodexBackend.complete.")
        cfg = self._local.runtime
        payload = {"job_id": job["id"], "instructions": instructions, "input": input_items,
                   "tools": tools, "schema": output_schema, "backend": self.config}
        key = hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
        # Do not place the job ID directly in file paths; the request key pins the loaded rules and input and prevents uncontrolled paths.
        job_key = hashlib.sha256(str(job["id"]).encode()).hexdigest()[:20]
        group = Path(cfg["workspace"]).resolve() / "transport" / "codex" / job_key / key
        generation = self._local.generation
        # Reconcile prior paid results before an explicit retry; generation creates a new receipt only for a genuinely uncertain call.
        for prior_attempt in sorted(group.glob("g*"), reverse=True):
            if self._reconcile(prior_attempt):
                return self._reply(prior_attempt / "final.json", prior_attempt)
        attempt = group / f"g{generation:04d}"
        attempt.mkdir(parents=True, exist_ok=True)
        receipt = attempt / "receipt.json"
        final = attempt / "final.json"
        if receipt.exists():
            prior = json.loads(receipt.read_text("utf-8"))
            if prior.get("status") == "completed" and final.exists():
                return self._reply(final, attempt)
            if prior.get("status") != "not_started":
                raise CodexUncertain(f"An unconfirmed Codex call already exists; inspect {receipt}. Do not automatically issue another paid call.")
        atomic_write(attempt / "AGENTS.md", instructions.encode())
        atomic_write(attempt / "input.json", json.dumps(input_items, ensure_ascii=False, indent=2).encode())
        atomic_write(attempt / "handoff.schema.json", json.dumps(output_schema, ensure_ascii=False).encode())
        atomic_write(attempt / "transport-metadata.json", json.dumps({
            "initial_input_characters": len(instructions) + len(json.dumps(input_items, ensure_ascii=False)),
            "measurement_scope": "Initial instructions and input files only; the peak internal Codex context is not observable.",
            "model": self.config.get("model"), "user_config_loaded": True,
            "request_hash": key, "job_id": job["id"], "transport_retry_generation": generation}, ensure_ascii=False).encode())
        command = [self.config.get("command", "codex"), "exec", "--cd", str(attempt),
                   "--skip-git-repo-check", "--sandbox", "read-only", "--json",
                   "--output-schema", str(attempt / "handoff.schema.json"),
                   "--output-last-message", str(final)]
        if self.config.get("model"):
            command += ["--model", self.config["model"]]
        if self.config.get("ephemeral", True):
            command += ["--ephemeral"]
        mcp_args = ["-m", "oracle_atlas", "mcp", "--config", str(Path(cfg["config_path"]).resolve()), "--job", str(job["id"])]
        overrides = {"mcp_servers.oracle_atlas.command": sys.executable,
                     "mcp_servers.oracle_atlas.args": mcp_args,
                     "mcp_servers.oracle_atlas.enabled": True,
                     "mcp_servers.oracle_atlas.required": True,
                     "mcp_servers.oracle_atlas.env_vars": self.config.get("mcp_env_vars", []),
                     "mcp_servers.oracle_atlas.env.PYTHONPATH": str(Path(__file__).resolve().parents[2])}
        # exec cannot ask for MCP approval. Authorize only the known local tools
        # exposed for this job; ToolHost still validates role, grants and inputs.
        overrides.update(_local_approval_overrides(tools))
        for name, value in overrides.items():
            command += ["-c", name + "=" + json.dumps(value, ensure_ascii=False)]
        command.append("-")
        prompt = ("Read AGENTS.md and input.json in this directory. Complete the assigned role; use oracle_atlas MCP to read sources, "
                  "Atlas, skills, and memory as needed and save artifacts. Modify research records only through MCP, never Atlas or internal databases directly. "
                  "Finally, output exactly the small handoff object specified by handoff.schema.json.")
        atomic_write(receipt, json.dumps({"status": "started", "request_hash": key}).encode())
        try:
            with (attempt / "events.jsonl").open("wb") as stdout, (attempt / "stderr.log").open("wb") as stderr:
                process = self._popen(command, stdin=subprocess.PIPE, stdout=stdout, stderr=stderr,
                                      cwd=str(attempt), start_new_session=os.name != "nt")
                try:
                    process.communicate(input=prompt.encode(), timeout=float(self.config.get("codex_timeout", self.config.get("timeout", 1800))))
                except subprocess.TimeoutExpired:
                    if os.name != "nt":
                        os.killpg(process.pid, signal.SIGTERM)
                    else:
                        process.terminate()
                    try:
                        process.communicate(timeout=5)
                    except subprocess.TimeoutExpired:
                        if os.name != "nt":
                            os.killpg(process.pid, signal.SIGKILL)
                        else:
                            process.kill()
                        process.communicate()
                    raise CodexUncertain("Codex timed out and the result may be incomplete; preserve the receipt and do not rerun automatically.")
            if process.returncode != 0 or not final.is_file():
                raise CodexUncertain(f"Codex did not return a complete result (exit={process.returncode}); inspect {attempt}.")
        except FileNotFoundError as exc:
            atomic_write(receipt, json.dumps({"status": "not_started", "reason": "executable_missing"}).encode())
            raise ProviderError("Codex CLI was not found; install/configure it, then explicitly resume this request.") from exc
        except BaseException:
            atomic_write(receipt, json.dumps({"status": "uncertain", "request_hash": key}).encode())
            raise
        atomic_write(receipt, json.dumps({"status": "completed", "request_hash": key}).encode())
        return self._reply(final, attempt)

    @staticmethod
    def _reconcile(attempt):
        receipt, final, events = attempt / "receipt.json", attempt / "final.json", attempt / "events.jsonl"
        if not receipt.is_file() or not final.is_file():
            return False
        info = json.loads(receipt.read_text("utf-8"))
        if info.get("status") == "completed":
            return True
        if events.exists():
            with events.open("r", encoding="utf-8", errors="replace") as stream:
                for line in stream:
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    if event.get("type") == "turn.completed":
                        atomic_write(receipt, json.dumps({**info, "status": "completed", "reconciled": True}).encode())
                        return True
        return False

    @staticmethod
    def _reply(final, attempt):
        text = final.read_text("utf-8")
        usage, thread = None, None
        events = attempt / "events.jsonl"
        if events.exists():
            with events.open("r", encoding="utf-8", errors="replace") as stream:
                for line in stream:
                    try:
                        event = json.loads(line)
                    except ValueError:
                        continue
                    if event.get("type") == "thread.started":
                        thread = event.get("thread_id")
                    if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
                        usage = event["usage"]
        return Reply(output_items=[{"type": "message", "role": "assistant", "content": [{"type": "output_text", "text": text}]}],
                     text=text, usage=usage, response_id=thread)

    def close(self):
        pass  # Each call has completed or terminated its process group; producer/reviewer sessions are not reused.
