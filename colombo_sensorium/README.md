# Colombo Sensorium

This directory bundles the following Sensorium components:

| Directory | Contents |
| --- | --- |
| [Complexity_altas](Complexity_altas/README.md) | Native records for 425 settings, scientific history, static browsing pages, and PDF/TeX/Markdown exports |
| [Structural_exploration](Structural_exploration/README.md) | Independent setting-neighborhood discovery, research, review, and explicitly authorized Atlas publication tools |
| [Literature_grounded_discovery](Literature_grounded_discovery/README.md) | Literature discovery, setting extraction, independent bound review, and transactional Atlas maintenance |
| [Atlas_renew](Atlas_renew/README.md) | Bounded maintenance of existing setting profiles, joint bracket analysis, independent review, and native Atlas adoption |

The spelling `Complexity_altas` matches the source directory. Each component keeps its existing scientific identifiers, data contracts, entry points, and review/publication requirements.

## Browse the Atlas

From this directory, serve the static Atlas with:

```sh
python3 -m http.server 8000 --directory Complexity_altas
```

Open `http://localhost:8000/` in a browser. See the [Atlas guide](Complexity_altas/README.md) for native records, exports, and validation commands.

## Structural exploration

Use a dedicated Python 3.11+ environment and follow the [component guide](Structural_exploration/README.md). The bundled Atlas is available at `../Complexity_altas` when working from `Structural_exploration/`. Research proposals and publication remain separate operations with the original approval gates.

## Sources and local data

The Atlas and structural exploration components originate from the [Sensorium source tree](https://github.com/HaihanZhang2001/Colombo_Code). Scientific setting identifiers, source citations and review limitations remain part of the research data. Software checks do not grant mathematical acceptance to Atlas records.

Workstation credentials, local execution records, test results, environments and generated packages are excluded from this source distribution. Runtime stores and local research outputs are generated only when the tools are used.

`Literature_grounded_discovery` provides literature discovery and independent review. Follow its own guide for installation, configuration and validation.

`Atlas_renew` maintains settings already present in an Atlas using finite research plans, exact source checks, cumulative budgets, independent review and native file transactions. Follow its guide and begin with an Atlas copy.
