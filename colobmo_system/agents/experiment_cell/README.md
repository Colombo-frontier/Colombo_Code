# Experiment Cell

Brain dispatches specialization="experiment" into an independent empirical lifecycle. The research agent uses the [main instruction](agent.md), [protocol](protocol.md) and relevant [Skills](skills/README.md). Runtime code lives in src/colombo/experiment_cell/controller.py and mcp_server.py; fixed-script execution and recovery are shared with the existing Experiment executor.

Each Skill owns its method guidance and any scenario references or executable examples. Current examples are GD matched families and a rational quadratic inequality probe. They are optional research resources, not mandatory pipeline stages. Actual run data belongs in Task artifacts. Skill evaluation cases and expected answers remain in project tests and are not installed into researcher workspaces.

One researcher can perform several batches, inspect evidence and revise the method before submitting a report. The existing outer Result Verifier reviews the returned empirical finding; Brain decides adoption and follow-up. Execution or scientific review does not grant mathematical Proof status.
