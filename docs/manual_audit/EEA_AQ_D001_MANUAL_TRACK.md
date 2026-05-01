# EEA AQ D-001 Manual Track Runbook

This document is a complete manual runbook for the EEA Air Quality D-001 track.
It is not a completed result. Follow it from top to bottom when you are ready
to produce a public ClaimBound evidence record.

The track is a source-readiness and coverage audit for official EEA air-quality
PM10 data. It does not claim forecasting performance, deployment readiness, or
model superiority.

General manual audit rules are defined in
[docs/MANUAL_AUDIT_PROTOCOL.md](../MANUAL_AUDIT_PROTOCOL.md).

## 0. Fixed Scope

Do not change these fields after starting the run log.

```text
Track ID: EEA_AQ_D001
Claim type: source audit
Official source: EEA Air Quality Download Service
Dataset: verified E1a data
Pollutant: PM10
Countries: NL, BE, DE
Period: 2018-01-01 through 2024-12-31
Aggregation: daily records
Coverage gate: at least 85 percent daily coverage per sampling point
Selection rule: first five eligible sampling points per country after sorting
  by country code, city/locality if available, and sampling point ID
Raw payload policy: raw files stay outside this repository
Public output policy: commit only sanitized summary, evidence card, and card SVG
```

Allowed final statuses:

- `PASSED_UNDER_PROTOCOL`
- `NEGATIVE_RESULT_UNDER_PROTOCOL`
- `BLOCKED_SOURCE`
- `INSUFFICIENT_COVERAGE`

Status meanings for this track:

- Use `PASSED_UNDER_PROTOCOL` only if the source is accessible, rights are
  acceptable for sanitized public evidence, and all three countries have at
  least five eligible PM10 daily sampling points under the fixed coverage rule.
- Use `NEGATIVE_RESULT_UNDER_PROTOCOL` if the source is accessible and rights
  are acceptable, but the fixed gate does not pass for reasons other than
  source blockage.
- Use `BLOCKED_SOURCE` if access, rights, documentation, or file format prevents
  a fair run.
- Use `INSUFFICIENT_COVERAGE` if data exists but the fixed coverage requirement
  cannot be met.

## 1. Official Source References

Record these references in the run log before downloading anything.

- EEA AQ Portal download page:
  <https://aqportal.discomap.eea.europa.eu/download-data/>
- Air Quality Download web application:
  <https://eeadmz1-downloads-webapp.azurewebsites.net/>
- Air Quality Download API Swagger:
  <https://eeadmz1-downloads-api-appservice.azurewebsites.net/swagger/index.html>
- Air Quality Download documentation PDF:
  <https://eeadmz1-downloads-webapp.azurewebsites.net/content/documentation/How_To_Downloads.pdf>
- EEA copyright notice:
  <https://www.eea.europa.eu/en/about/policy/copyright>
- EEA reuse FAQ:
  <https://www.eea.europa.eu/en/about/contact-us/faqs/can-i-use-eea-content-in-my-work-or-in-my-organisations-products>

The EEA download page describes the Air Quality Download Service as a source
for verified E1a data and up-to-date E2a data. The EEA documentation PDF
describes the web application, API, filters, download behavior, metadata,
vocabulary, and parquet schema.

## 2. Before You Start

1. Open a terminal.
2. Go to the public repository.

   ```bash
   cd /path/to/claimbound-public-benchmarks
   ```

3. Confirm that the repository is clean.

   ```bash
   git status --short --branch
   ```

4. Expected output shape:

   ```text
   ## main...origin/main
   ```

5. If there are uncommitted changes, stop.
6. Do not mix this manual run with unrelated edits.
7. Confirm the current commit.

   ```bash
   git rev-parse --short HEAD
   ```

8. Copy the short commit into your notes as `starting_git_commit`.
9. Confirm Python is available.

   ```bash
   python3 --version
   ```

10. Confirm checksum tooling is available.

    ```bash
    shasum -a 256 README.md | head -1
    ```

11. Confirm the current date.

    ```bash
    date -u +"%Y-%m-%dT%H:%M:%SZ"
    ```

12. Write the UTC timestamp into your notes as `run_started_utc`.

## 3. Execution Mode Declaration

13. Decide the execution mode before opening data files.
14. Use `MANUAL_NO_AI` if you do not ask an AI tool to inspect data, choose
    stations, tune gates, decide the status, or write the final claim.
15. Use `MANUAL_AI_ASSISTED` if you ask an AI tool for help during the run.
16. If you use AI assistance, record what was used and for what purpose.
17. Do not use AI to choose favorable stations after seeing results.
18. Do not use AI to rewrite a failed or blocked result as a success.
19. Do not change the fixed scope after this point.

Copy this declaration into the run log:

```text
Execution mode: MANUAL_NO_AI or MANUAL_AI_ASSISTED
AI assistance used during execution: yes/no
If yes, describe exactly:
Operator name or handle:
Run started UTC:
Starting git commit:
```

## 4. Create External Working Folders

Raw files must stay outside the public repository.

20. Choose a run date in `YYYYMMDD` format.
21. Create a run root outside the repo.

    ```bash
    RUN_ID="eea_aq_d001_$(date -u +%Y%m%d)"
    RUN_ROOT="$HOME/claimbound_runs/$RUN_ID"
    mkdir -p "$RUN_ROOT"/{raw,downloads,hashes,logs,reports,scripts,work}
    printf '%s\n' "$RUN_ROOT"
    ```

22. Copy the printed path into your notes as `external_run_root`.
23. Confirm you are not inside the public repo.

    ```bash
    pwd
    ```

24. Go back to the public repo only when editing public sanitized files.
25. Keep browser downloads in `$RUN_ROOT/downloads`.
26. Move raw downloaded files into `$RUN_ROOT/raw`.
27. Never commit files from `$RUN_ROOT/raw`.

## 5. Create The Run Log

28. Create the run log.

    ```bash
    cat > "$RUN_ROOT/logs/operator_log.md" <<'EOF'
    # EEA AQ D-001 Operator Log

    ## Run Identity

    Track ID: EEA_AQ_D001
    Operator:
    Execution mode:
    Run started UTC:
    Starting git commit:
    External run root:

    ## Fixed Scope

    Official source: EEA Air Quality Download Service
    Dataset: verified E1a
    Pollutant: PM10
    Countries: NL, BE, DE
    Period: 2018-01-01 through 2024-12-31
    Aggregation: daily records
    Coverage gate: at least 85 percent daily coverage per sampling point
    Selection rule: first five eligible sampling points per country after sorting

    ## Source Notes

    Download page:
    Web application:
    API Swagger:
    Documentation PDF:
    Copyright/reuse note:

    ## Download Notes

    Browser used:
    Download method: web application / API Swagger / other
    Dataset selected:
    Countries selected:
    Pollutant selected:
    Type selected:
    Date start selected:
    Date end selected:
    Summary result:
    Download files:

    ## Processing Notes

    Python version:
    pandas version:
    pyarrow version:
    Input file count:
    Raw hash manifest:
    Analysis CSV:
    Sanitized summary JSON:

    ## Status Decision

    Result status:
    Reason:
    Deviations:
    Known limitations:
    EOF
    ```

29. Open the run log in your editor.
30. Fill `Operator`.
31. Fill `Execution mode`.
32. Fill `Run started UTC`.
33. Fill `Starting git commit`.
34. Fill `External run root`.
35. Save the file.

## 6. Manual Source-Rights Audit

36. Open the EEA AQ Portal download page in a browser.
37. Confirm that it links to the Air Quality Download service.
38. Open the Air Quality Download web application.
39. Open the documentation PDF.
40. Open the EEA copyright notice.
41. Open the EEA reuse FAQ.
42. Read the pages manually.
43. In `operator_log.md`, record whether sanitized public summaries are allowed.
44. In `operator_log.md`, record that raw payload files will not be committed.
45. If reuse terms are unavailable, ambiguous, or contradictory, stop.
46. If blocked by rights uncertainty, set candidate status to `BLOCKED_SOURCE`.
47. If blocked, skip to section 18 and create a blocked summary.

## 7. Download Method A: Web Application

Use this method first. Use Method B only if the web UI fails or you need a
repeatable API fallback.

48. Open <https://eeadmz1-downloads-webapp.azurewebsites.net/>.
49. Wait until the page is fully loaded.
50. Find the country filter.
51. Select `NL`.
52. Select `BE`.
53. Select `DE`.
54. Find the pollutant filter.
55. Select `PM10`.
56. Find the dataset filter.
57. Select verified E1a data.
58. Find the type or aggregation filter.
59. Select daily records.
60. Find temporal coverage.
61. Set start to `2018-01-01T00:00:00Z` if the UI accepts time.
62. If the UI accepts only dates, set start to `2018-01-01`.
63. Set end to `2024-12-31T23:59:59Z` if the UI accepts time.
64. If the UI accepts only dates, set end to `2024-12-31`.
65. Leave city blank.
66. Leave email blank unless you want to provide one.
67. If there is a `Summary` button, click it before downloading.
68. Copy the summary count and size into `operator_log.md`.
69. If the UI says the request is too large, select the option for list of URLs.
70. If the UI offers parquet download directly and size is acceptable, keep it.
71. Click `Download`.
72. Wait until the browser finishes downloading.
73. If a ZIP is downloaded, move it into `$RUN_ROOT/raw`.
74. If a CSV list of URLs is downloaded, move it into `$RUN_ROOT/downloads`.
75. If the browser downloads multiple parquet files, move them into
    `$RUN_ROOT/raw`.
76. Record every downloaded filename in `operator_log.md`.
77. If nothing downloads after two attempts, do not keep clicking randomly.
78. Switch to Method B.

## 8. Download Method B: API Swagger Fallback

79. Open the API Swagger page.
80. Find the endpoint group for parquet files.
81. Prefer the endpoint that returns a list of parquet URLs.
82. Click `Try it out`.
83. Use country values `NL`, `BE`, `DE`.
84. Use pollutant value `PM10`.
85. Use dataset value `2` for verified E1a data.
86. Use source value `API`.
87. Use start `2018-01-01T00:00:00Z` if the endpoint accepts it.
88. Use end `2024-12-31T23:59:59Z` if the endpoint accepts it.
89. Use daily type if the endpoint exposes a type or frequency field.
90. Click `Execute`.
91. Copy the request URL or request body into `operator_log.md`.
92. Copy the HTTP status code into `operator_log.md`.
93. If the endpoint returns URLs, copy them into a local text file:

    ```bash
    touch "$RUN_ROOT/downloads/parquet_urls.txt"
    ```

94. Paste one URL per line into `parquet_urls.txt`.
95. Download the URL list.

    ```bash
    cd "$RUN_ROOT/raw"
    while IFS= read -r url; do
      [ -z "$url" ] && continue
      filename="$(basename "${url%%\?*}")"
      curl -L --fail --retry 3 --output "$filename" "$url"
    done < "$RUN_ROOT/downloads/parquet_urls.txt"
    ```

96. If the API returns a ZIP URL, download the ZIP into `$RUN_ROOT/raw`.
97. If the API returns an error, record the response.
98. If both Method A and Method B fail, set candidate status to `BLOCKED_SOURCE`.

## 9. Freeze The Raw Payload Set

99. List raw files.

    ```bash
    find "$RUN_ROOT/raw" -type f | sort
    ```

100. If there are ZIP files, keep the original ZIP.
101. Extract a copy into a subfolder.

     ```bash
     mkdir -p "$RUN_ROOT/work/extracted"
     find "$RUN_ROOT/raw" -name '*.zip' -print0 | while IFS= read -r -d '' z; do
       unzip -n "$z" -d "$RUN_ROOT/work/extracted"
     done
     ```

102. Hash the raw files.

     ```bash
     cd "$RUN_ROOT"
     find raw work/extracted -type f | sort | xargs shasum -a 256 > hashes/raw_payloads.sha256
     ```

103. Hash the hash manifest.

     ```bash
     shasum -a 256 "$RUN_ROOT/hashes/raw_payloads.sha256" > "$RUN_ROOT/hashes/raw_payloads_manifest.sha256"
     ```

104. Copy the manifest hash into `operator_log.md`.
105. Do not copy raw hashes into public docs unless needed as an external
     manifest reference.
106. Do not copy raw payloads into the public repository.

## 10. Prepare Local Processing Environment

107. Create a local virtual environment outside the repo.

     ```bash
     cd "$RUN_ROOT"
     python3 -m venv .venv
     . .venv/bin/activate
     python -m pip install --upgrade pip
     python -m pip install pandas pyarrow
     ```

108. Record versions.

     ```bash
     python - <<'PY'
     import pandas as pd
     import pyarrow as pa
     import sys
     print("python", sys.version)
     print("pandas", pd.__version__)
     print("pyarrow", pa.__version__)
     PY
     ```

109. Copy those versions into `operator_log.md`.

## 11. Create The Inspection Script

110. Create the script.

     ```bash
     cat > "$RUN_ROOT/scripts/inspect_eea_aq_d001.py" <<'PY'
     from __future__ import annotations

     import json
     import zipfile
     from datetime import date
     from pathlib import Path

     import pandas as pd

     RUN_ROOT = Path(__file__).resolve().parents[1]
     INPUT_DIRS = [RUN_ROOT / "raw", RUN_ROOT / "work" / "extracted"]
     OUT_DIR = RUN_ROOT / "reports"
     OUT_DIR.mkdir(parents=True, exist_ok=True)

     START = pd.Timestamp("2018-01-01")
     END = pd.Timestamp("2024-12-31")
     EXPECTED_DAYS = (END - START).days + 1
     MIN_COVERAGE = 0.85
     COUNTRIES = {"NL", "BE", "DE"}

     def norm(name: object) -> str:
         return str(name).strip().lower().replace(" ", "").replace("_", "")

     def find_col(cols: list[str], candidates: list[str]) -> str | None:
         lookup = {norm(c): c for c in cols}
         for c in candidates:
             if norm(c) in lookup:
                 return lookup[norm(c)]
         for col in cols:
             n = norm(col)
             if any(norm(c) in n for c in candidates):
                 return col
         return None

     def files() -> list[Path]:
         out: list[Path] = []
         for root in INPUT_DIRS:
             if not root.exists():
                 continue
             for path in root.rglob("*"):
                 if path.is_file() and path.suffix.lower() in {".parquet", ".csv"}:
                     out.append(path)
         return sorted(out)

     def read(path: Path) -> pd.DataFrame:
         if path.suffix.lower() == ".parquet":
             return pd.read_parquet(path)
         return pd.read_csv(path)

     frames = []
     file_summaries = []
     for path in files():
         try:
             df = read(path)
         except Exception as exc:
             file_summaries.append({"path": str(path), "read_error": repr(exc)})
             continue

         cols = list(df.columns)
         sampling_col = find_col(cols, ["Samplingpoint", "SamplingPoint", "samplingpoint"])
         pollutant_col = find_col(cols, ["Pollutant", "pollutant"])
         start_col = find_col(cols, ["Start", "DatetimeBegin", "begin"])
         end_col = find_col(cols, ["End", "DatetimeEnd", "end"])
         value_col = find_col(cols, ["Value", "Concentration", "value"])
         unit_col = find_col(cols, ["Unit", "unit"])
         agg_col = find_col(cols, ["AggType", "aggregationtype", "type"])
         country_col = find_col(cols, ["Country", "countrycode", "CountryCode"])
         city_col = find_col(cols, ["City", "Locality", "locality"])

         file_summaries.append(
             {
                 "path": str(path),
                 "rows": int(len(df)),
                 "columns": cols,
                 "sampling_col": sampling_col,
                 "pollutant_col": pollutant_col,
                 "start_col": start_col,
                 "value_col": value_col,
                 "agg_col": agg_col,
             }
         )

         required = [sampling_col, pollutant_col, start_col, value_col]
         if any(c is None for c in required):
             continue

         small = pd.DataFrame()
         small["samplingpoint"] = df[sampling_col].astype(str)
         small["pollutant"] = df[pollutant_col].astype(str)
         small["start"] = pd.to_datetime(df[start_col], errors="coerce", utc=False)
         small["value"] = pd.to_numeric(df[value_col], errors="coerce")
         small["unit"] = df[unit_col].astype(str) if unit_col else ""
         small["aggtype"] = df[agg_col].astype(str) if agg_col else ""
         if country_col:
             small["country"] = df[country_col].astype(str).str.upper().str[:2]
         else:
             small["country"] = small["samplingpoint"].str.upper().str[:2]
         if city_col:
             small["city"] = df[city_col].astype(str)
         else:
             small["city"] = ""
         frames.append(small)

     if frames:
         data = pd.concat(frames, ignore_index=True)
     else:
         data = pd.DataFrame(
             columns=["samplingpoint", "pollutant", "start", "value", "unit", "aggtype", "country", "city"]
         )

     filtered = data[
         data["country"].isin(COUNTRIES)
         & data["pollutant"].str.upper().str.contains("PM10", na=False)
         & (data["start"] >= START)
         & (data["start"] <= END)
         & data["value"].notna()
     ].copy()

     if not filtered.empty and filtered["aggtype"].astype(str).str.len().sum() > 0:
         daily_mask = filtered["aggtype"].str.lower().str.contains("day|daily", na=False)
         if daily_mask.any():
             filtered = filtered[daily_mask].copy()

     filtered["date"] = filtered["start"].dt.date
     grouped = (
         filtered.groupby(["country", "city", "samplingpoint"], dropna=False)
         .agg(
             observed_days=("date", "nunique"),
             row_count=("value", "size"),
             first_date=("date", "min"),
             last_date=("date", "max"),
             unit_values=("unit", lambda x: sorted({str(v) for v in x if str(v) != ""})[:5]),
         )
         .reset_index()
     )
     grouped["expected_days"] = EXPECTED_DAYS
     grouped["coverage_ratio"] = grouped["observed_days"] / EXPECTED_DAYS
     grouped["eligible"] = grouped["coverage_ratio"] >= MIN_COVERAGE
     grouped = grouped.sort_values(["country", "city", "samplingpoint"], kind="stable")
     selected = grouped[grouped["eligible"]].groupby("country", group_keys=False).head(5)

     by_country = {}
     for country in sorted(COUNTRIES):
         country_rows = grouped[grouped["country"] == country]
         selected_rows = selected[selected["country"] == country]
         by_country[country] = {
             "sampling_points_seen": int(country_rows["samplingpoint"].nunique()) if not country_rows.empty else 0,
             "eligible_sampling_points": int(country_rows[country_rows["eligible"]]["samplingpoint"].nunique()) if not country_rows.empty else 0,
             "selected_sampling_points": selected_rows["samplingpoint"].tolist(),
             "gate_passed": bool(len(selected_rows) >= 5),
         }

     overall_passed = all(v["gate_passed"] for v in by_country.values())
     if filtered.empty:
         status = "BLOCKED_SOURCE"
         reason = "No usable PM10 daily records were parsed from the downloaded files."
     elif overall_passed:
         status = "PASSED_UNDER_PROTOCOL"
         reason = "All fixed countries have at least five eligible PM10 daily sampling points."
     else:
         status = "INSUFFICIENT_COVERAGE"
         reason = "At least one fixed country has fewer than five eligible PM10 daily sampling points."

     grouped.to_csv(OUT_DIR / "station_coverage.csv", index=False)
     selected.to_csv(OUT_DIR / "selected_sampling_points.csv", index=False)
     summary = {
         "schema": "claimbound_eea_aq_d001_manual_summary_v1",
         "track_id": "EEA_AQ_D001",
         "source": {
             "name": "EEA Air Quality Download Service",
             "web_application": "https://eeadmz1-downloads-webapp.azurewebsites.net/",
             "api_swagger": "https://eeadmz1-downloads-api-appservice.azurewebsites.net/swagger/index.html",
             "raw_payload_committed": False,
         },
         "fixed_scope": {
             "dataset": "verified E1a",
             "pollutant": "PM10",
             "countries": sorted(COUNTRIES),
             "period": "2018-01-01..2024-12-31",
             "aggregation": "daily records",
             "coverage_gate": "at least 85 percent daily coverage per sampling point",
             "selection_rule": "first five eligible sampling points per country after sorting",
         },
         "file_summaries": file_summaries,
         "by_country": by_country,
         "result": {
             "result_status": status,
             "reason": reason,
         },
         "claim_boundary": {
             "allowed": "EEA AQ D-001 source-readiness status under the fixed PM10 coverage protocol only.",
             "forbidden": [
                 "air-quality forecasting performance",
                 "deployment readiness",
                 "model superiority",
                 "health-impact claim",
                 "raw payload redistribution",
             ],
         },
     }
     (OUT_DIR / "eea_aq_d001_manual_summary.json").write_text(
         json.dumps(summary, indent=2, sort_keys=True),
         encoding="utf-8",
     )
     print(json.dumps(summary["result"], indent=2, sort_keys=True))
     PY
     ```

111. Save the script.
112. Do not edit the script after seeing the result unless the script fails to
     read the documented source format.
113. If you edit the script, record the reason in `operator_log.md`.

## 12. Run The Inspection Script

114. Run it.

     ```bash
     cd "$RUN_ROOT"
     . .venv/bin/activate
     python scripts/inspect_eea_aq_d001.py
     ```

115. If the script prints `PASSED_UNDER_PROTOCOL`, do not celebrate yet.
116. Open the generated station coverage file.

     ```bash
     open "$RUN_ROOT/reports/station_coverage.csv"
     ```

117. If `open` is unavailable, print the first rows.

     ```bash
     python - <<'PY'
     import pandas as pd, os
     root = os.environ["RUN_ROOT"]
     print(pd.read_csv(f"{root}/reports/station_coverage.csv").head(30).to_string())
     PY
     ```

118. Check that countries are only `BE`, `DE`, `NL`.
119. Check that sampling points are not blank.
120. Check that coverage ratios are plausible.
121. Check that selected sampling points are sorted by the fixed rule.
122. Open the selected sampling points file.

     ```bash
     open "$RUN_ROOT/reports/selected_sampling_points.csv"
     ```

123. Confirm that each passing country has exactly five selected sampling
     points.
124. If any file has unreadable columns, inspect `file_summaries` in the JSON.
125. If the downloaded source format cannot be parsed without changing the
     protocol, choose `BLOCKED_SOURCE`.

## 13. Manual Result Decision

126. Open the generated summary JSON.

     ```bash
     python -m json.tool "$RUN_ROOT/reports/eea_aq_d001_manual_summary.json" | less
     ```

127. Read `result.result_status`.
128. Read `result.reason`.
129. Read `by_country`.
130. Do not override the status because it is disappointing.
131. Do not change country list.
132. Do not change pollutant.
133. Do not lower coverage after seeing the output.
134. Do not select different stations after seeing coverage.
135. If source access failed, status must be `BLOCKED_SOURCE`.
136. If rights were unclear, status must be `BLOCKED_SOURCE`.
137. If the parser could read data but coverage failed, status should be
     `INSUFFICIENT_COVERAGE`.
138. If all gates passed, status may be `PASSED_UNDER_PROTOCOL`.
139. Write the final status into `operator_log.md`.
140. Write the reason into `operator_log.md`.
141. Write any deviations into `operator_log.md`.

## 14. Create Public Sanitized Summary

142. Go to the public repository.

     ```bash
     cd /path/to/claimbound-public-benchmarks
     ```

143. Create a new branch.

     ```bash
     git switch -c manual/eea-aq-d001-result
     ```

144. Copy only the sanitized summary JSON into `artifacts/`.

     ```bash
     cp "$RUN_ROOT/reports/eea_aq_d001_manual_summary.json" artifacts/eea_aq_d001_manual_summary.json
     ```

145. Do not copy raw parquet files.
146. Do not copy raw CSV files.
147. Do not copy ZIP files.
148. Do not copy browser screenshots.
149. Hash the sanitized summary.

     ```bash
     shasum -a 256 artifacts/eea_aq_d001_manual_summary.json
     ```

150. Copy this hash into `operator_log.md`.

## 15. Create The Evidence Card JSON

151. Choose the current date in `YYYY-MM-DD` format.
152. Set `CARD_DATE` to that date.

     ```bash
     CARD_DATE="$(date -u +%Y-%m-%d)"
     CARD_PATH="docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-${CARD_DATE}.json"
     ```

153. Create the evidence card.

     ```bash
     SUMMARY_SHA="$(shasum -a 256 artifacts/eea_aq_d001_manual_summary.json | awk '{print $1}')"
     RAW_MANIFEST_SHA="$(awk '{print $1}' "$RUN_ROOT/hashes/raw_payloads_manifest.sha256")"
     STATUS="$(python3 - <<'PY'
     import json
     data=json.load(open("artifacts/eea_aq_d001_manual_summary.json"))
     print(data["result"]["result_status"])
     PY
     )"
     cat > "$CARD_PATH" <<EOF
     {
       "access_date": "$CARD_DATE",
       "ai_assistance": "not used during manual status decision",
       "baseline_control_summary": "Fixed source-readiness controls: official source, verified E1a dataset, PM10 pollutant, BE/DE/NL country set, daily aggregation, 2018-2024 period, 85 percent coverage gate, first five eligible sampling points per country.",
       "card_svg_template": "docs/assets/claimbound_evidence_card.svg",
       "claim_boundary": "EEA AQ D-001 reports only source-readiness and coverage status under the fixed PM10 manual protocol.",
       "claim_type": "source audit",
       "created_at": "$CARD_DATE",
       "domain": "air-quality",
       "evidence_id": "CLAIMBOUND-EEA-AQ-D001-$CARD_DATE",
       "evidence_url": "https://github.com/NeoZorK/claimbound-public-benchmarks/blob/main/$CARD_PATH",
       "execution_mode": "MANUAL_NO_AI",
       "git_commit": "$(git rev-parse --short HEAD)",
       "known_limitations": [
         "This is a source-readiness and coverage audit only.",
         "No forecasting performance is claimed.",
         "No deployment readiness is claimed.",
         "No raw payloads are committed."
       ],
       "manual_review": "operator reviewed source access, source rights, raw payload boundary, station selection and final status",
       "official_source_name": "EEA Air Quality Download Service",
       "official_source_url": "https://eeadmz1-downloads-webapp.azurewebsites.net/",
       "operator": "fill operator name or handle",
       "protocol_id": "EEA_AQ_D001",
       "protocol_version": "manual-track-v1",
       "raw_payload_committed": false,
       "raw_payload_manifest": "external raw payload manifest SHA-256: $RAW_MANIFEST_SHA",
       "reproduction_level": "not independently reproduced",
       "result_status": "$STATUS",
       "runner_command": "manual runbook docs/manual_audit/EEA_AQ_D001_MANUAL_TRACK.md plus local external inspection script",
       "sanitized_report_path": "artifacts/eea_aq_d001_manual_summary.json",
       "sanitized_report_sha256": "$SUMMARY_SHA",
       "source_rights_note": "Official public EEA source; raw payloads are not committed."
     }
     EOF
     ```

154. Open the card.

     ```bash
     python3 -m json.tool "$CARD_PATH" | less
     ```

155. Replace `operator` with your actual public operator name or handle.
156. If AI was used, change `execution_mode` and `ai_assistance` honestly.
157. If status is not `PASSED_UNDER_PROTOCOL`, keep
     `baseline_control_summary`; it explains the source-audit controls.
158. Validate the card.

     ```bash
     uv run --extra dev python scripts/claimbound_validate_evidence_card.py "$CARD_PATH"
     ```

159. Fix only validation errors.
160. Do not change the result status to make the validator pass.

## 16. Create The Visual SVG Card

161. Copy the SVG template.

     ```bash
     SVG_PATH="${CARD_PATH%.json}.svg"
     cp docs/assets/claimbound_evidence_card.svg "$SVG_PATH"
     ```

162. Replace placeholders manually in the SVG.
163. Use the evidence card JSON as the source of truth.
164. Suggested replacements:

     ```text
     {{status_exact}} -> the result_status value
     {{reproduction_level}} -> not reproduced, outcome reproduced, or exact level
     {{allowed_claim_sentence}} -> EEA AQ D-001 source-readiness status recorded
     {{record_id}} -> EEA-AQ-D001
     {{protocol_id}} -> EEA_AQ_D001 manual-track-v1
     {{target_definition}} -> PM10 daily source coverage
     {{candidate_definition}} -> official EEA E1a records
     {{controls_and_gate}} -> 85 percent coverage, 5 stations per country
     {{source_name}} -> EEA Air Quality Download Service
     {{period_scope}} -> 2018-2024, BE/DE/NL
     {{evidence_date}} -> CARD_DATE
     {{artifact_ref}} -> short commit plus sanitized summary
     {{evidence_url}} -> CARD_PATH
     ```

165. Search for leftover placeholders.

     ```bash
     rg "\\{\\{" "$SVG_PATH"
     ```

166. If placeholders remain, fill them.
167. Open the SVG in a browser.
168. Confirm the card text is readable.
169. Confirm the status matches the JSON card.
170. Confirm there is no broader claim than the JSON card.

## 17. Update The Registry Index

171. Open `docs/registry/evidence_index.json`.
172. Add a new entry for the EEA card under `cards`.
173. Use the JSON card path.
174. Add the SVG URL.
175. Add the result status.
176. Add domain `air-quality`.
177. Add source `EEA Air Quality Download Service`.
178. Add reproduction level.
179. Increment `card_count`.
180. Increment `statistics.by_result_status`.
181. Increment `statistics.by_domain.air-quality`.
182. Increment `statistics.by_source.EEA Air Quality Download Service`.
183. Save the file.
184. Validate JSON formatting.

     ```bash
     python3 -m json.tool docs/registry/evidence_index.json >/tmp/claimbound_registry_check.json
     ```

## 18. If The Track Is Blocked

185. Do not delete the failed notes.
186. Create a sanitized blocked summary JSON.
187. Use `BLOCKED_SOURCE`.
188. Explain exactly what blocked the run.
189. Do not include private browser tokens.
190. Do not include raw payloads.
191. Create an evidence card anyway.
192. Include `block_reason` in the evidence card.
193. Validate the card.
194. A blocked card is a valid ClaimBound result.

## 19. Final Local Checks

195. Run tests.

     ```bash
     uv run --extra dev python -m pytest -n auto
     ```

196. Scan for raw payload-like files.

     ```bash
     find . \( -path ./.git -o -path ./.venv -o -path ./.pytest_cache -o -path ./__pycache__ \) -prune -o -type f \( -name '*.csv' -o -name '*.parquet' -o -name '*.zip' -o -name '*.jsonl' -o -name '*.env' -o -name '*.key' -o -name '*.pem' \) -print
     ```

197. The command should not print raw payload files.
198. If it prints your raw payload files, remove them before committing.
199. Scan for forbidden broad claims.

     ```bash
     rg -n -i "universal forecasting edge|deployment readiness|best model|model superiority|breakthrough" artifacts docs
     ```

200. If matches are in forbidden contexts, rewrite the public claim boundary.
201. Validate the evidence card again.
202. Check git status.

     ```bash
     git status --short
     ```

203. Confirm only intended public files changed.

## 20. Commit And Pull Request

204. Stage the sanitized public files.

     ```bash
     git add artifacts/eea_aq_d001_manual_summary.json
     git add docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-*.json
     git add docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-*.svg
     git add docs/registry/evidence_index.json
     ```

205. Do not stage `$RUN_ROOT`.
206. Do not stage raw files.
207. Commit.

     ```bash
     git commit -m "docs: add EEA AQ D-001 manual evidence card"
     ```

208. Push the branch.

     ```bash
     git push -u origin manual/eea-aq-d001-result
     ```

209. Open a pull request.
210. In the pull request body, include:

     ```text
     Summary:
     - ran EEA AQ D-001 manual source-readiness track
     - added sanitized summary
     - added evidence card JSON/SVG
     - updated public registry index

     Verification:
     - evidence-card validator passed
     - pytest passed
     - raw payload scan clean

     Raw payload policy:
     - raw files stored outside repository
     - raw payload manifest hash recorded externally
     ```

211. Wait for GitHub checks.
212. If checks fail, inspect logs.
213. Fix only the real issue.
214. Do not change the result status just to pass checks.
215. Merge only after checks pass.

## 21. Final Review Questions

Before merging, answer these questions:

216. Did the protocol stay fixed from the beginning?
217. Did raw payloads stay outside the repository?
218. Did the source rights note stay honest?
219. Did the selected stations follow the sorting rule?
220. Did coverage use the fixed 85 percent threshold?
221. Does the public summary avoid raw payload details?
222. Does the evidence card validate?
223. Does the SVG match the JSON card?
224. Does the registry index point to the right card?
225. Does the final claim stay inside source-readiness and coverage only?
226. Would another operator understand how to rerun this track?
227. If the result is negative or blocked, is it recorded without shame?
228. If the result passed, are the limitations still visible?

## 22. What To Share

Share these public links after merge:

- the sanitized summary JSON;
- the evidence card JSON;
- the visual SVG card;
- the registry index entry;
- the pull request.

Do not share:

- raw parquet files;
- raw ZIP files;
- browser screenshots containing local paths;
- private notes;
- claims outside this protocol.
