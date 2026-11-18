"""Fresh Codex CLI sessions. No optimization runtime or Brain/Cell scheduler import."""
from __future__ import annotations
from dataclasses import dataclass
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import tomllib
import uuid
from colombo.memory.contracts import ContractError
from colombo.memory.store import atomic_json, now


class BackendTransportError(ContractError):
    """A model call failed without producing a reviewable content result."""


@dataclass
class ModelResult:
    run_id: str
    backend: str
    payload: dict
    run_directory: Path

class CodexBackend:
    name = "codex_cli"
    def __init__(self, *, model: str | None = None, executable: str = "codex", timeout: int = 900,
                 reviewer_model: str | None = None):
        self.model, self.executable, self.timeout = model, executable, timeout
        self.reviewer_model = reviewer_model

    def _user_preferences(self) -> dict:
        # Whitelist the model and native system-proxy opt-in. Never forward
        # plugins, MCP servers, profiles, providers or other user configuration.
        codex_directory = Path(os.environ.get("CODEX_HOME") or Path.home() / ".codex").expanduser()
        config = codex_directory / "config.toml"
        try:
            with config.open("rb") as stream:
                user = tomllib.load(stream)
        except FileNotFoundError:
            return {}
        except (OSError, tomllib.TOMLDecodeError) as exc:
            raise ContractError("Cannot read Codex model/transport preferences from config.toml") from exc
        features = user.get("features", {})
        if not isinstance(features, dict):
            raise ContractError("Codex features must be a table to read the system-proxy preference")
        preferences = {"model": user.get("model")}
        if "respect_system_proxy" in features:
            value = features["respect_system_proxy"]
            if type(value) is not bool:
                raise ContractError("Codex features.respect_system_proxy must be a boolean")
            preferences["respect_system_proxy"] = value
        return preferences

    def _resolve_model(self, role: str, preferences: dict | None = None) -> tuple[str | None, str]:
        if role == "reviewer" and self.reviewer_model:
            return self.reviewer_model, "reviewer_model"
        if self.model:
            return self.model, "explicit"
        model = (self._user_preferences() if preferences is None else preferences).get("model")
        if model is None:
            return None, "cli_default"
        if not isinstance(model, str) or not model.strip():
            raise ContractError("The top-level Codex model must be a nonempty string; pass --model explicitly")
        return model, "user_config"

    def run(self, *, role: str, prompt: str, schema: dict, workspace: Path, runs: Path) -> ModelResult:
        binary = shutil.which(self.executable)
        if binary is None:
            raise BackendTransportError("Codex CLI not found. Install/configure it separately; no model call was made.")
        preferences = self._user_preferences()
        selected_model, model_source = self._resolve_model(role, preferences)
        transport = {key: preferences[key] for key in ("respect_system_proxy",) if key in preferences}
        run_id = role + "-" + uuid.uuid4().hex
        directory = runs / run_id; directory.mkdir(parents=True)
        schema_path = directory / "output.schema.json"
        output_path = directory / "model-output.json"
        atomic_json(schema_path, schema)
        (directory / "prompt.txt").write_text(prompt, encoding="utf-8")
        # CLI itself writes the result outside the model's read-only sandbox.
        command = [binary, "--ask-for-approval", "never", "exec", "--ignore-user-config", "--ephemeral",
                   "--sandbox", "read-only",
                   "--skip-git-repo-check", "--json", "--output-schema", str(schema_path),
                   "--output-last-message", str(output_path)]
        if selected_model:
            command += ["--model", selected_model]
        # --ignore-user-config still uses CODEX_HOME authentication, but drops
        # this opt-in needed on system-proxy/PAC networks. Keep that one bool.
        if "respect_system_proxy" in transport:
            command += ["-c", "features.respect_system_proxy=" + json.dumps(transport["respect_system_proxy"])]
        command += ["-"]
        receipt = {"run_id": run_id, "role": role, "backend": self.name, "started_at": now(),
                   "command": command, "workspace": str(workspace), "status": "running",
                   "model": selected_model, "model_source": model_source,
                   "transport_preferences": transport,
                   "config_mode": "ignore-user-config", "ephemeral": True,
                   "scientific_review_claim": "none; process provenance only"}
        atomic_json(directory / "run.json", receipt)
        try:
            with (directory / "events.jsonl").open("wb") as out, (directory / "stderr.txt").open("wb") as err:
                process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=out, stderr=err,
                    cwd=workspace, start_new_session=(os.name != "nt"))
                try:
                    process.communicate(prompt.encode("utf-8"), timeout=self.timeout)
                except subprocess.TimeoutExpired:
                    if os.name != "nt":
                        os.killpg(process.pid, signal.SIGKILL)
                    else:
                        process.kill()
                    process.communicate()
                    raise BackendTransportError("Model process timed out; its output is not an accepted checkpoint")
            if process.returncode:
                raise BackendTransportError(f"Codex exited with {process.returncode}; inspect {directory / 'stderr.txt'}")
            payload = json.loads(output_path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ContractError("Model output must be a JSON object")
            receipt.update(status="transport_complete", finished_at=now())
            atomic_json(directory / "run.json", receipt)
            return ModelResult(run_id, self.name, payload, directory)
        except Exception as exc:
            receipt.update(status="rejected_transport", finished_at=now(), error=str(exc))
            atomic_json(directory / "run.json", receipt)
            raise
