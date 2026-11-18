"""Narrow MCP surface for independent Experiment Cells."""
from pathlib import Path
import os
import sys

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from mcp.server.fastmcp import FastMCP
from colombo.shared.tool_jobs import submit_or_poll
from colombo.shared.tool_jobs import poll_job
from colombo.experiment_cell.controller import target_ref
from colombo.experiment_cell.controller import submit_report as save_report

RUN = Path(os.environ["CELL_RUN_DIR"]).resolve()
mcp = FastMCP("experiment-research")



@mcp.tool()
def run_experiment(question: str, code: str, request_id: str,
                   parameters: dict | None = None, input_files: list[str] | None = None) -> dict:
    """Run an experiment against the fixed Task. Reuse request_id only for identical inputs."""
    return submit_or_poll(RUN, "run_experiment", dict(question=question,
        target_ref=target_ref(RUN), code=code, request_id=request_id,
        parameters=parameters, input_files=input_files), request_id=request_id)


@mcp.tool()
def resume_experiment(experiment_id: str) -> dict:
    """Recover the original execution without making a replacement paid request."""
    return submit_or_poll(RUN, "resume_experiment", {"experiment_id": experiment_id})


@mcp.tool()
def job_status(job_id: str) -> dict:
    """Retrieve the original result; pending is not successful evidence."""
    return poll_job(RUN, job_id)


@mcp.tool()
def retrieve(record_id: str, revision: int | None = None, kind: str = "experiment_result") -> dict:
    """Read an immutable local research record."""
    from colombo.cell.record_store import Store
    return Store(RUN / "memory").get(kind, record_id, revision)


@mcp.tool()
def lookup(query: str = "", url: str = "", limit: int | None = None) -> dict:
    """Search/read external sources under the existing Cell search configuration."""
    from colombo.shared.literature_access import lookup as search
    return search(query=query, url=url, limit=limit)


@mcp.tool()
def budget_status() -> dict:
    """Read the existing Cell execution budget."""
    from colombo.cell.recovery import budget_status as status
    return status(RUN)


@mcp.tool()
def submit_report(report: dict, body: str) -> dict:
    """Submit empirical report and self-contained Markdown; does not certify a Proof.

    report requires summary, actual_scope, method, uncertainty (text), measurements,
    candidate_rates, limitations, failures (lists), experiment_refs (fixed refs),
    artifact_paths (local paths), and outcome=observations or inconclusive.
    """
    return save_report(RUN, report, body)


if __name__ == "__main__":
    mcp.run()
