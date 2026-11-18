# Testing and scientific scope

Run the checks from a dedicated Python environment after installing the source component:

```bash
python -m pytest -q
python scripts/check_resources.py
python examples/offline_demo.py --output ./demo_paper
python examples/offline_expansion_demo.py --output ./demo_expansion
```

The examples mark every scientific judgment as synthetic. Their bounded scripted drivers allow 16 context segments and 90 turns per job while preserving the 60000-character input cap. These settings do not raise production defaults. A source installation exposes `structural-exploration --help`, `oracle-atlas-expand --help` and `oracle-atlas --help` for checking the primary and compatibility commands.

External literature services and model responses use fixtures. Local MCP transport tests start local servers and require loopback access. Run output belongs in ignored local directories.

## Fixture and scientific scope

The fixture directory contains target schemas. Tests generate synthetic native records in temporary directories, including a historical-format example without joint analysis. They verify that such a record remains readable while a new write requires an explicit current analysis and independent review. Target-schema tests construct synthetic input and provenance.

Software checks establish neither literature completeness nor mathematical correctness. Model research, independent scientific review and actual Atlas publication are separate operations. A completed ingestion requires its own receipt bound to the exact reviewed content.
