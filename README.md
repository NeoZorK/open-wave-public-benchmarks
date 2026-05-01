# Open Wave Public Benchmarks

<p align="center">
  <img
    src="docs/assets/openwave-logo-x400.png"
    alt="OpenWave public benchmarks logo"
    width="400"
  />
</p>

Open Wave Public Benchmarks is an open-source foreground for pre-registered
public time-series evaluation.

It is not a production forecasting service. It is a public toolkit for checking
whether a narrow time-series claim was tested under rules fixed before the run.

The project focuses on reproducibility discipline:

- source eligibility is checked before a real run;
- targets, scorers, controls and acceptance gates are fixed before execution;
- raw public-source payloads stay outside the repository;
- committed artifacts contain commands, hashes, summaries and claim boundaries;
- negative and blocked results remain first-class evidence.

## Current Evidence

The current public evidence contains one narrow positive result and multiple
negative or source-blocked records:

```text
NASA POWER D-103 passed the pre-registered gate under protocol 1.0.143 and was
independently reproduced at outcome/gate level on 2026-04-29.
```

Additional records show source lineage and negative/blocked outcomes:

- NOAA CO-OPS D-131: official-source run completed; statistical acceptance did
  not pass.
- NYC TLC Phase 4: official-source run completed; statistical acceptance did
  not pass.
- CDC mirror path: public mirror proof path completed, but external source
  equivalence remained unresolved.

This does not imply a universal forecasting edge, deployment readiness, or
superiority over all statistical methods.

## How The Pipeline Works

```text
official public source
  -> local raw payload outside this repository
  -> parser and source manifest
  -> pre-registered runner
  -> baseline and control comparison
  -> result status and sanitized evidence summary
```

Result statuses are defined in [docs/RESULT_STATUS.md](docs/RESULT_STATUS.md).
Claim boundaries are defined in [docs/CLAIMS.md](docs/CLAIMS.md).

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

Detailed reproduction instructions are in
[docs/REPRODUCTION.md](docs/REPRODUCTION.md).

## Manual Domain Track

A future public-domain manual track template is included for European air
quality data:

[docs/manual_audit/EEA_AQ_D001_MANUAL_TRACK.md](docs/manual_audit/EEA_AQ_D001_MANUAL_TRACK.md)

This template is designed for a no-AI operator audit: rules first, then source
download, then run, then publish the exact result status.

## Boundary

This repository is independently usable as an open benchmark foreground. It does
not include, import, or require private background technology.

## Community

- [Contributing guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security policy](SECURITY.md)
- [Discussions — maintainer announcements and community Q&A](https://github.com/NeoZorK/open-wave-public-benchmarks/discussions)

## License

Apache-2.0. See [LICENSE](LICENSE).
