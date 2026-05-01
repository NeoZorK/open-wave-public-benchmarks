# EEA Air Quality D-001 Manual Track

This document is a fillable manual checklist for a future public-domain audit.
It is not a completed result.

General manual audit rules are defined in
[docs/MANUAL_AUDIT_PROTOCOL.md](../MANUAL_AUDIT_PROTOCOL.md).

## No-AI Declaration

```text
Domain: EEA Air Quality D-001
Operator: fill manually
Date started: YYYY-MM-DD

For this benchmark domain I did not use ChatGPT, Codex, Copilot or any other AI
assistant to choose favorable data after seeing results, design the acceptance
gate after seeing results, tune thresholds after seeing results, rewrite failed
outcomes as success, or generate evidence claims.

Allowed tools: terminal, browser, official source documentation, Python, pytest,
git, SHA-256 command-line tools and text editor.
```

## Source Audit

- [ ] Official source identified.
- [ ] Source rights read manually.
- [ ] Attribution requirement recorded.
- [ ] Raw payload redistribution policy decided.
- [ ] Raw files excluded from git.
- [ ] API or download terms saved as citation note.

Official source references:

- https://aqportal.discomap.eea.europa.eu/download-data/
- https://www.eea.europa.eu/legal
- https://www.eea.europa.eu/en/about/contact-us/faqs/can-i-use-eea-content-in-my-work-or-in-my-organisations-products

## Data Availability

- [ ] Time range available.
- [ ] PM10 available.
- [ ] Station metadata available.
- [ ] Units known.
- [ ] Time zone or local-date convention known.
- [ ] Missing values documented.
- [ ] Coverage rule applied before outcome scoring.

## Pre-Run Protocol

- [ ] Countries fixed before outcome inspection.
- [ ] Station selection rule fixed before outcome inspection.
- [ ] Target fixed before outcome inspection.
- [ ] Candidate fixed before outcome inspection.
- [ ] Baselines fixed before outcome inspection.
- [ ] Acceptance gate fixed before outcome inspection.
- [ ] Forbidden after-result changes written down.

Suggested station selection:

```text
Countries: NL, BE, DE
Pollutant: PM10
Time range: 2018-01-01 to 2024-12-31
Coverage: at least 85% daily coverage
Selection: first five eligible stations sorted by country code, locality and
station identifier
```

## Raw Payload Handling

Create raw folders outside this repository:

```bash
mkdir -p ~/claimbound_raw/eea_aq_d001/raw
mkdir -p ~/claimbound_raw/eea_aq_d001/hashes
mkdir -p ~/claimbound_raw/eea_aq_d001/reports
```

After download:

```bash
cd ~/claimbound_raw/eea_aq_d001/raw
shasum -a 256 * > ../hashes/raw_payloads.sha256
```

## Operator Log

```text
Date:
Machine:
OS:
Python:
Git commit:
Protocol version:
Access date:
Source:
Pollutant:
Countries:
Time range:
Raw files outside repo:
Raw hash file:
Manifest hash:
Report hash:
Deviations:
Result status:
Manual notes:
```

## Result Status

Choose one:

- `PASSED_UNDER_PROTOCOL`
- `NEGATIVE_RESULT_UNDER_PROTOCOL`
- `BLOCKED_SOURCE`
- `INSUFFICIENT_COVERAGE`

Any of these statuses is valid if it is recorded honestly.
