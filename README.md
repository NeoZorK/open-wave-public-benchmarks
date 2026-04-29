# Open Wave Public Benchmarks

Open Wave Public Benchmarks is an open-source foreground for pre-registered
public time-series evaluation.

The project focuses on reproducibility discipline:

- source eligibility is checked before a real run;
- targets, scorers, controls and acceptance gates are fixed before execution;
- raw public-source payloads stay outside the repository;
- committed artifacts contain commands, hashes, summaries and claim boundaries;
- negative and blocked results remain first-class evidence.

## Current Evidence

The current public evidence contains one narrow positive result:

```text
NASA POWER D-103 passed the pre-registered gate under protocol 1.0.143 and was
independently reproduced at outcome/gate level on 2026-04-29.
```

This does not imply a universal forecasting edge, deployment readiness, or
superiority over all statistical methods.

## Install

```bash
uv sync --extra dev
uv run pytest -n auto
```

## Offline Smoke

```bash
uv run python scripts/fetch_nasa_power.py --help
uv run python scripts/openwave_run_nasa_power_prereg.py --help
```

The real NASA POWER payload files used for the recorded D-103 run are not
committed. Reproduction requires downloading fresh official NASA POWER Daily
JSON payloads outside the repository and recording their hashes.

## Boundary

This repository is independently usable as an open benchmark foreground. It does
not include, import, or require private background technology.

## License

Apache-2.0. See [LICENSE](LICENSE).

