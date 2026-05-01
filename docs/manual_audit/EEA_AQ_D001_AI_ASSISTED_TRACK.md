# EEA AQ D-001 AI-Assisted Track Runbook

This document is a complete AI-assisted runbook for the EEA Air Quality D-001
track.

It is not a completed result. Follow it from top to bottom when you are ready
to produce a public ClaimBound evidence record with disclosed AI assistance.

The track is a source-readiness and coverage audit for official EEA
air-quality PM10 data. It does not claim forecasting performance, deployment
readiness, or model superiority.

The AI assistant is allowed to help make the work clearer and more auditable.
The AI assistant is not allowed to decide the result, tune the gate after
seeing the result, choose favorable stations, fabricate citations, fabricate
hashes, or rewrite a blocked or negative outcome as success.

General rules are defined in:

- [docs/MANUAL_AUDIT_PROTOCOL.md](../MANUAL_AUDIT_PROTOCOL.md)
- [docs/AI_OPERATOR_PROTOCOL.md](../AI_OPERATOR_PROTOCOL.md)

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
Execution mode: MANUAL_AI_ASSISTED
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

The AI assistant may explain these meanings, but it must not invent a fifth
status or override the deterministic status rules.

## 1. AI Trust Boundary

1. Treat the AI assistant as an untrusted drafting and review tool.
2. Treat commands, hashes, source links, and status values as facts that must be
   verified outside the AI model.
3. Never accept an AI-generated hash.
4. Never accept an AI-generated source-rights conclusion without opening the
   official source yourself.
5. Never accept an AI-generated result status unless it is copied from the
   deterministic summary JSON or manual checklist.
6. Do not paste raw payload files into a hosted AI chat.
7. If AI sees raw rows, record that fact and why it was necessary.
8. Prefer giving AI schema, column names, errors, and sanitized summaries rather
   than raw data.
9. Keep all AI prompts and AI answers in the external run folder.
10. Publish only a short AI disclosure in the evidence card.

Allowed AI help:

- explain the protocol before execution;
- find missing checklist fields before raw data is inspected;
- draft prompts, commands, parsers, and tests before scoring;
- review parser code for deterministic behavior;
- summarize official documentation already opened by the operator;
- summarize the final sanitized summary after the result status exists;
- check consistency between evidence card, claim boundary, and result status.

Prohibited AI actions:

- choose countries, pollutant, period, station count, or coverage gate after
  seeing the data;
- choose favorable sampling points after seeing coverage;
- lower the coverage threshold;
- ignore failed countries;
- alter raw payloads;
- fabricate source-rights notes;
- fabricate command output;
- fabricate SHA-256 values;
- remove deviations;
- convert blocked or insufficient coverage into a positive status;
- add broad forecasting, health-impact, deployment, or model-superiority claims.

## 2. Official Source References

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

The AI assistant may help summarize these pages, but the operator must open the
official pages and decide whether the source boundary is acceptable.

## 3. Before You Start

11. Open a terminal.
12. Go to the public repository.

    ```bash
    cd /path/to/claimbound-public-benchmarks
    ```

13. Confirm that the repository is clean.

    ```bash
    git status --short --branch
    ```

14. Expected output shape:

    ```text
    ## main...origin/main
    ```

15. If there are uncommitted changes, stop.
16. Do not mix this AI-assisted run with unrelated edits.
17. Confirm the current commit.

    ```bash
    git rev-parse --short HEAD
    ```

18. Copy the short commit into your notes as `starting_git_commit`.
19. Confirm Python is available.

    ```bash
    python3 --version
    ```

20. Confirm checksum tooling is available.

    ```bash
    shasum -a 256 README.md | head -1
    ```

21. Confirm the current UTC time.

    ```bash
    date -u +"%Y-%m-%dT%H:%M:%SZ"
    ```

22. Write the timestamp into your notes as `run_started_utc`.

## 4. Create External Working Folders

Raw files and AI transcripts must stay outside the public repository unless a
sanitized excerpt is intentionally committed.

23. Create the external run root.

    ```bash
    RUN_ID="eea_aq_d001_ai_$(date -u +%Y%m%d)"
    RUN_ROOT="$HOME/claimbound_runs/$RUN_ID"
    mkdir -p "$RUN_ROOT"/{raw,downloads,hashes,logs,reports,scripts,work,ai}
    mkdir -p "$RUN_ROOT/ai"/{prompts,responses,review_packets}
    printf '%s\n' "$RUN_ROOT"
    ```

24. Copy the printed path into your notes as `external_run_root`.
25. Keep browser downloads in `$RUN_ROOT/downloads`.
26. Move raw downloaded files into `$RUN_ROOT/raw`.
27. Put AI prompts in `$RUN_ROOT/ai/prompts`.
28. Put AI responses in `$RUN_ROOT/ai/responses`.
29. Put AI review packets in `$RUN_ROOT/ai/review_packets`.
30. Never commit files from `$RUN_ROOT/raw`.
31. Do not commit full AI transcripts unless they are sanitized and necessary.

## 5. Create The Run Log

32. Create the operator log.

    ```bash
    cat > "$RUN_ROOT/logs/operator_log.md" <<'EOF'
    # EEA AQ D-001 AI-Assisted Operator Log

    ## Run Identity

    Track ID: EEA_AQ_D001
    Operator:
    Execution mode: MANUAL_AI_ASSISTED
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

    ## AI Assistance Declaration

    AI tool name:
    AI tool version or model if known:
    AI used for protocol review before outcome inspection: yes/no
    AI used for source documentation summary: yes/no
    AI used for parser drafting: yes/no
    AI used after sanitized result summary existed: yes/no
    AI saw raw payload rows: yes/no
    If AI saw raw rows, explain why:
    AI was allowed to decide status: no
    AI was allowed to change gates after result: no

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

    ## AI Audit Trail

    Prompt hash manifest:
    Response hash manifest:
    AI review packet hashes:
    AI deviations:

    ## Status Decision

    Result status:
    Reason:
    Deviations:
    Known limitations:
    EOF
    ```

33. Open the run log in your editor.
34. Fill `Operator`.
35. Fill `Run started UTC`.
36. Fill `Starting git commit`.
37. Fill `External run root`.
38. Fill AI tool details.
39. Save the file.

## 6. Freeze The Protocol Before AI Sees Results

40. Create a protocol lock file.

    ```bash
    cat > "$RUN_ROOT/logs/protocol_lock.txt" <<'EOF'
    Track ID: EEA_AQ_D001
    Execution mode: MANUAL_AI_ASSISTED
    Official source: EEA Air Quality Download Service
    Dataset: verified E1a data
    Pollutant: PM10
    Countries: NL, BE, DE
    Period: 2018-01-01 through 2024-12-31
    Aggregation: daily records
    Coverage gate: at least 85 percent daily coverage per sampling point
    Selection rule: first five eligible sampling points per country after sorting by country code, city/locality if available, and sampling point ID
    Status source: deterministic summary JSON plus operator checklist
    AI status authority: none
    EOF
    ```

41. Hash the protocol lock.

    ```bash
    shasum -a 256 "$RUN_ROOT/logs/protocol_lock.txt" > "$RUN_ROOT/hashes/protocol_lock.sha256"
    ```

42. Copy the hash into `operator_log.md`.
43. Do not edit `protocol_lock.txt` after this point.
44. If a correction is unavoidable, create a new file named
    `protocol_lock_deviation.txt` and record the reason.

## 7. AI Prompt 1: Protocol Review Before Data

Use this prompt before downloading or opening data. Do not include raw payloads.

45. Create the prompt.

    ```bash
    cat > "$RUN_ROOT/ai/prompts/001_protocol_review.txt" <<'EOF'
    You are assisting a ClaimBound EEA AQ D-001 source-readiness audit.

    Fixed scope:
    - Official source: EEA Air Quality Download Service
    - Dataset: verified E1a data
    - Pollutant: PM10
    - Countries: NL, BE, DE
    - Period: 2018-01-01 through 2024-12-31
    - Aggregation: daily records
    - Coverage gate: at least 85 percent daily coverage per sampling point
    - Selection rule: first five eligible sampling points per country after sorting
    - Raw payloads stay outside the public repository

    Your task:
    1. Check for missing pre-run fields.
    2. Identify ambiguity that must be resolved before outcome inspection.
    3. Do not change countries, pollutant, period, threshold, or selection rule.
    4. Do not propose easier gates.
    5. Do not infer any result status.
    EOF
    ```

46. Send this prompt to the AI assistant.
47. Save the AI answer as:

    ```text
    $RUN_ROOT/ai/responses/001_protocol_review.md
    ```

48. Read the answer manually.
49. Accept only pre-run clarity improvements.
50. Reject any suggested change to countries, pollutant, period, threshold, or
    station selection.
51. Record accepted and rejected suggestions in `operator_log.md`.

## 8. Manual Source-Rights Audit With AI Support

52. Open the EEA AQ Portal download page in a browser.
53. Open the Air Quality Download web application.
54. Open the API Swagger page.
55. Open the documentation PDF.
56. Open the EEA copyright notice.
57. Open the EEA reuse FAQ.
58. Read the pages manually.
59. Copy only short citations or summarized notes into your local log.
60. Do not ask AI to guess source rights from memory.
61. If using AI, give it only the official links and your own notes.

Create a source-review prompt:

62. Create the prompt.

    ```bash
    cat > "$RUN_ROOT/ai/prompts/002_source_rights_review.txt" <<'EOF'
    You are assisting a ClaimBound source-rights checklist.

    Official links opened by the human operator:
    - https://aqportal.discomap.eea.europa.eu/download-data/
    - https://eeadmz1-downloads-webapp.azurewebsites.net/
    - https://eeadmz1-downloads-api-appservice.azurewebsites.net/swagger/index.html
    - https://eeadmz1-downloads-webapp.azurewebsites.net/content/documentation/How_To_Downloads.pdf
    - https://www.eea.europa.eu/en/about/policy/copyright
    - https://www.eea.europa.eu/en/about/contact-us/faqs/can-i-use-eea-content-in-my-work-or-in-my-organisations-products

    Task:
    - Produce a checklist of facts the operator must verify manually.
    - Do not invent source-rights conclusions.
    - Do not claim that raw payload redistribution is allowed.
    - Keep the public output boundary limited to sanitized summaries, evidence card JSON, evidence card SVG, hashes, and claim boundaries.
    EOF
    ```

63. Send the prompt to the AI assistant.
64. Save the response as:

    ```text
    $RUN_ROOT/ai/responses/002_source_rights_review.md
    ```

65. Manually verify every source-rights point against the official pages.
66. In `operator_log.md`, record whether sanitized public summaries are allowed.
67. In `operator_log.md`, record that raw payload files will not be committed.
68. If rights are unavailable, ambiguous, or contradictory, stop.
69. If blocked by rights uncertainty, set candidate status to `BLOCKED_SOURCE`.

## 9. Download Method A: Web Application

Use this method first. Use Method B only if the web UI fails or you need a
repeatable API fallback.

70. Open <https://eeadmz1-downloads-webapp.azurewebsites.net/>.
71. Wait until the page is fully loaded.
72. Find the country filter.
73. Select `NL`.
74. Select `BE`.
75. Select `DE`.
76. Find the pollutant filter.
77. Select `PM10`.
78. Find the dataset filter.
79. Select verified E1a data.
80. Find the type or aggregation filter.
81. Select daily records.
82. Find temporal coverage.
83. Set start to `2018-01-01T00:00:00Z` if the UI accepts time.
84. If the UI accepts only dates, set start to `2018-01-01`.
85. Set end to `2024-12-31T23:59:59Z` if the UI accepts time.
86. If the UI accepts only dates, set end to `2024-12-31`.
87. Leave city blank.
88. Leave email blank unless you want to provide one.
89. If there is a `Summary` button, click it before downloading.
90. Copy the summary count and size into `operator_log.md`.
91. If the UI says the request is too large, select the option for list of URLs.
92. If the UI offers parquet download directly and size is acceptable, keep it.
93. Click `Download`.
94. Wait until the browser finishes downloading.
95. If a ZIP is downloaded, move it into `$RUN_ROOT/raw`.
96. If a CSV list of URLs is downloaded, move it into `$RUN_ROOT/downloads`.
97. If the browser downloads multiple parquet files, move them into
    `$RUN_ROOT/raw`.
98. Record every downloaded filename in `operator_log.md`.
99. If nothing downloads after two attempts, do not keep clicking randomly.
100. Switch to Method B.

## 10. Download Method B: API Swagger Fallback

101. Open the API Swagger page.
102. Find the endpoint group for parquet files.
103. Prefer the endpoint that returns a list of parquet URLs.
104. Click `Try it out`.
105. Use country values `NL`, `BE`, `DE`.
106. Use pollutant value `PM10`.
107. Use dataset value `2` for verified E1a data if the API requires a numeric
     dataset value.
108. Use source value `API` if the endpoint exposes that field.
109. Use start `2018-01-01T00:00:00Z` if the endpoint accepts it.
110. Use end `2024-12-31T23:59:59Z` if the endpoint accepts it.
111. Use daily type if the endpoint exposes a type or frequency field.
112. Click `Execute`.
113. Copy the request URL or request body into `operator_log.md`.
114. Copy the HTTP status code into `operator_log.md`.
115. If the endpoint returns URLs, copy them into a local text file:

     ```bash
     touch "$RUN_ROOT/downloads/parquet_urls.txt"
     ```

116. Paste one URL per line into `parquet_urls.txt`.
117. Download the URL list.

     ```bash
     cd "$RUN_ROOT/raw"
     while IFS= read -r url; do
       [ -z "$url" ] && continue
       filename="$(basename "${url%%\?*}")"
       curl -L --fail --retry 3 --output "$filename" "$url"
     done < "$RUN_ROOT/downloads/parquet_urls.txt"
     ```

118. If the API returns a ZIP URL, download the ZIP into `$RUN_ROOT/raw`.
119. If the API returns an error, record the response.
120. If both Method A and Method B fail, set candidate status to
     `BLOCKED_SOURCE`.

## 11. Freeze The Raw Payload Set

121. List raw files.

     ```bash
     find "$RUN_ROOT/raw" -type f | sort
     ```

122. If there are ZIP files, keep the original ZIP.
123. Extract a copy into a subfolder.

     ```bash
     mkdir -p "$RUN_ROOT/work/extracted"
     find "$RUN_ROOT/raw" -name '*.zip' -print0 | while IFS= read -r -d '' z; do
       unzip -n "$z" -d "$RUN_ROOT/work/extracted"
     done
     ```

124. Hash the raw files.

     ```bash
     cd "$RUN_ROOT"
     find raw work/extracted -type f | sort | xargs shasum -a 256 > hashes/raw_payloads.sha256
     ```

125. Hash the hash manifest.

     ```bash
     shasum -a 256 "$RUN_ROOT/hashes/raw_payloads.sha256" > "$RUN_ROOT/hashes/raw_payloads_manifest.sha256"
     ```

126. Copy the manifest hash into `operator_log.md`.
127. Do not copy raw hashes into public docs unless needed as an external
     manifest reference.
128. Do not copy raw payloads into the public repository.

## 12. Prepare Local Processing Environment

129. Create a local virtual environment outside the repo.

     ```bash
     cd "$RUN_ROOT"
     python3 -m venv .venv
     . .venv/bin/activate
     python -m pip install --upgrade pip
     python -m pip install pandas pyarrow
     ```

130. Record versions.

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

131. Copy those versions into `operator_log.md`.

## 13. AI Prompt 3: Parser Draft Or Review

Use this prompt before scoring. Give AI schema information, not the full raw
payload.

132. Create a small schema packet.

     ```bash
     cd "$RUN_ROOT"
     find raw work/extracted -type f \( -name '*.parquet' -o -name '*.csv' \) | sort | head -5 > ai/review_packets/schema_sample_files.txt
     ```

133. If parquet files exist, print only column names and row counts.

     ```bash
     . .venv/bin/activate
     python - <<'PY' > "$RUN_ROOT/ai/review_packets/schema_packet.txt"
     from pathlib import Path
     import pandas as pd

     root = Path(__import__("os").environ["RUN_ROOT"])
     paths = sorted([p for p in (root / "raw").rglob("*") if p.suffix.lower() in {".parquet", ".csv"}])
     paths += sorted([p for p in (root / "work" / "extracted").rglob("*") if p.suffix.lower() in {".parquet", ".csv"}])
     for path in paths[:5]:
         try:
             df = pd.read_parquet(path) if path.suffix.lower() == ".parquet" else pd.read_csv(path, nrows=5)
             print("FILE", path.name)
             print("ROWS", len(df))
             print("COLUMNS", list(df.columns))
             print()
         except Exception as exc:
             print("FILE", path.name)
             print("READ_ERROR", repr(exc))
             print()
     PY
     ```

134. Create the parser-review prompt.

     ```bash
     cat > "$RUN_ROOT/ai/prompts/003_parser_review.txt" <<'EOF'
     You are reviewing a deterministic parser plan for ClaimBound EEA AQ D-001.

     Fixed protocol:
     - verified E1a data only
     - PM10 only
     - countries NL, BE, DE only
     - 2018-01-01 through 2024-12-31
     - daily records only
     - at least 85 percent daily coverage per sampling point
     - first five eligible sampling points per country after sorting

     You may:
     - identify column mapping risks;
     - suggest deterministic parsing checks;
     - suggest validation assertions;
     - identify where the script should stop as BLOCKED_SOURCE.

     You must not:
     - suggest changing countries, pollutant, period, threshold, or selection rule;
     - infer the result status;
     - choose stations;
     - optimize for a positive result.

     Review the schema packet and parser plan. Return only deterministic checks.
     EOF
     ```

135. Send the prompt plus `schema_packet.txt` to AI.
136. Save the response as:

     ```text
     $RUN_ROOT/ai/responses/003_parser_review.md
     ```

137. Apply only deterministic parser checks that preserve the fixed protocol.
138. Record any accepted AI parser suggestions in `operator_log.md`.

## 14. Create The Inspection Script

139. Create the script.

     ```bash
     cat > "$RUN_ROOT/scripts/inspect_eea_aq_d001.py" <<'PY'
     from __future__ import annotations

     import json
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
         small["city"] = df[city_col].astype(str) if city_col else ""
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
         "schema": "claimbound_eea_aq_d001_ai_assisted_summary_v1",
         "track_id": "EEA_AQ_D001",
         "execution_mode": "MANUAL_AI_ASSISTED",
         "ai_assistance_boundary": {
             "ai_may_summarize": True,
             "ai_may_decide_status": False,
             "ai_may_change_gate_after_result": False,
         },
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
     (OUT_DIR / "eea_aq_d001_ai_assisted_summary.json").write_text(
         json.dumps(summary, indent=2, sort_keys=True),
         encoding="utf-8",
     )
     print(json.dumps(summary["result"], indent=2, sort_keys=True))
     PY
     ```

140. Save the script.
141. Do not edit the script after seeing the result unless the script fails to
     read the documented source format.
142. If AI suggests a post-result script edit, treat it as a deviation.
143. If you edit the script, record the exact reason in `operator_log.md`.

## 15. Run The Inspection Script

144. Run it.

     ```bash
     cd "$RUN_ROOT"
     . .venv/bin/activate
     python scripts/inspect_eea_aq_d001.py
     ```

145. Open the generated station coverage file.

     ```bash
     open "$RUN_ROOT/reports/station_coverage.csv"
     ```

146. If `open` is unavailable, print the first rows.

     ```bash
     python - <<'PY'
     import os
     import pandas as pd
     root = os.environ["RUN_ROOT"]
     print(pd.read_csv(f"{root}/reports/station_coverage.csv").head(30).to_string())
     PY
     ```

147. Check that countries are only `BE`, `DE`, `NL`.
148. Check that sampling points are not blank.
149. Check that coverage ratios are plausible.
150. Check that selected sampling points are sorted by the fixed rule.
151. Open the selected sampling points file.

     ```bash
     open "$RUN_ROOT/reports/selected_sampling_points.csv"
     ```

152. Confirm that each passing country has exactly five selected sampling
     points.
153. If any file has unreadable columns, inspect `file_summaries` in the JSON.
154. If the downloaded source format cannot be parsed without changing the
     protocol, choose `BLOCKED_SOURCE`.

## 16. Manual Status Decision

155. Open the generated summary JSON.

     ```bash
     python3 -m json.tool "$RUN_ROOT/reports/eea_aq_d001_ai_assisted_summary.json" | less
     ```

156. Read `result.result_status`.
157. Read `result.reason`.
158. Read `by_country`.
159. Do not ask AI to choose a different result.
160. Do not override the status because it is disappointing.
161. Do not change country list.
162. Do not change pollutant.
163. Do not lower coverage after seeing the output.
164. Do not select different stations after seeing coverage.
165. If source access failed, status must be `BLOCKED_SOURCE`.
166. If rights were unclear, status must be `BLOCKED_SOURCE`.
167. If the parser could read data but coverage failed, status should be
     `INSUFFICIENT_COVERAGE`.
168. If all gates passed, status may be `PASSED_UNDER_PROTOCOL`.
169. Write the final status into `operator_log.md`.
170. Write the reason into `operator_log.md`.
171. Write any deviations into `operator_log.md`.

## 17. AI Prompt 4: Post-Result Consistency Review

Use AI only after the deterministic summary exists.

172. Create a sanitized review packet.

     ```bash
     cp "$RUN_ROOT/reports/eea_aq_d001_ai_assisted_summary.json" "$RUN_ROOT/ai/review_packets/sanitized_summary_for_ai.json"
     ```

173. Create the post-result prompt.

     ```bash
     cat > "$RUN_ROOT/ai/prompts/004_post_result_consistency.txt" <<'EOF'
     You are reviewing a completed ClaimBound EEA AQ D-001 sanitized summary.

     Rules:
     - The result status has already been produced by deterministic processing.
     - Do not suggest changing the result status.
     - Do not suggest changing the coverage gate.
     - Do not add forecasting, health-impact, deployment, or model-superiority claims.
     - Check only whether the summary, claim boundary, evidence card draft, and limitations are internally consistent.
     - If the result is blocked or insufficient coverage, keep it as such.
     EOF
     ```

174. Send the prompt and sanitized summary to AI.
175. Save the response as:

     ```text
     $RUN_ROOT/ai/responses/004_post_result_consistency.md
     ```

176. Accept only consistency fixes.
177. Reject any suggestion to improve the result by changing gates, data, or
     station selection.
178. Record accepted and rejected suggestions in `operator_log.md`.

## 18. Hash The AI Audit Trail

179. Hash prompts.

     ```bash
     cd "$RUN_ROOT"
     find ai/prompts -type f | sort | xargs shasum -a 256 > hashes/ai_prompts.sha256
     ```

180. Hash responses.

     ```bash
     find ai/responses -type f | sort | xargs shasum -a 256 > hashes/ai_responses.sha256
     ```

181. Hash review packets.

     ```bash
     find ai/review_packets -type f | sort | xargs shasum -a 256 > hashes/ai_review_packets.sha256
     ```

182. Hash the AI manifests.

     ```bash
     shasum -a 256 hashes/ai_prompts.sha256 hashes/ai_responses.sha256 hashes/ai_review_packets.sha256 > hashes/ai_audit_manifests.sha256
     ```

183. Copy the AI manifest hashes into `operator_log.md`.
184. Do not publish private AI transcripts unless they are sanitized and needed
     for reproduction.

## 19. Create Public Sanitized Summary

185. Go to the public repository.

     ```bash
     cd /path/to/claimbound-public-benchmarks
     ```

186. Create a new branch.

     ```bash
     git switch -c manual/eea-aq-d001-ai-assisted-result
     ```

187. Copy only the sanitized summary JSON into `artifacts/`.

     ```bash
     cp "$RUN_ROOT/reports/eea_aq_d001_ai_assisted_summary.json" artifacts/eea_aq_d001_ai_assisted_summary.json
     ```

188. Do not copy raw parquet files.
189. Do not copy raw CSV files.
190. Do not copy ZIP files.
191. Do not copy full AI transcripts.
192. Do not copy browser screenshots.
193. Hash the sanitized summary.

     ```bash
     shasum -a 256 artifacts/eea_aq_d001_ai_assisted_summary.json
     ```

194. Copy this hash into `operator_log.md`.

## 20. Create The Evidence Card JSON

195. Choose the current date in `YYYY-MM-DD` format.
196. Set `CARD_DATE` to that date.

     ```bash
     CARD_DATE="$(date -u +%Y-%m-%d)"
     CARD_PATH="docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-AI-${CARD_DATE}.json"
     ```

197. Create the evidence card.

     ```bash
     SUMMARY_SHA="$(shasum -a 256 artifacts/eea_aq_d001_ai_assisted_summary.json | awk '{print $1}')"
     RAW_MANIFEST_SHA="$(awk '{print $1}' "$RUN_ROOT/hashes/raw_payloads_manifest.sha256")"
     AI_MANIFEST_SHA="$(shasum -a 256 "$RUN_ROOT/hashes/ai_audit_manifests.sha256" | awk '{print $1}')"
     STATUS="$(python3 - <<'PY'
     import json
     data=json.load(open("artifacts/eea_aq_d001_ai_assisted_summary.json"))
     print(data["result"]["result_status"])
     PY
     )"
     cat > "$CARD_PATH" <<EOF
     {
       "access_date": "$CARD_DATE",
       "ai_assistance": "AI used for protocol review, source checklist support, parser review and post-result consistency review; AI was not allowed to decide status or change gates.",
       "ai_audit_manifest": "external AI audit manifest SHA-256: $AI_MANIFEST_SHA",
       "baseline_control_summary": "Fixed source-readiness controls: official source, verified E1a dataset, PM10 pollutant, BE/DE/NL country set, daily aggregation, 2018-2024 period, 85 percent coverage gate, first five eligible sampling points per country.",
       "card_svg_template": "docs/assets/claimbound_evidence_card.svg",
       "claim_boundary": "EEA AQ D-001 reports only source-readiness and coverage status under the fixed PM10 AI-assisted manual protocol.",
       "claim_type": "source audit",
       "created_at": "$CARD_DATE",
       "domain": "air-quality",
       "evidence_id": "CLAIMBOUND-EEA-AQ-D001-AI-$CARD_DATE",
       "evidence_url": "https://github.com/NeoZorK/claimbound-public-benchmarks/blob/main/$CARD_PATH",
       "execution_mode": "MANUAL_AI_ASSISTED",
       "git_commit": "$(git rev-parse --short HEAD)",
       "known_limitations": [
         "This is a source-readiness and coverage audit only.",
         "No forecasting performance is claimed.",
         "No deployment readiness is claimed.",
         "No raw payloads are committed.",
         "AI assistance is disclosed but not trusted as result authority."
       ],
       "manual_review": "operator reviewed source access, source rights, raw payload boundary, AI assistance boundary, station selection and final status",
       "official_source_name": "EEA Air Quality Download Service",
       "official_source_url": "https://eeadmz1-downloads-webapp.azurewebsites.net/",
       "operator": "fill operator name or handle",
       "protocol_id": "EEA_AQ_D001",
       "protocol_version": "ai-assisted-manual-track-v1",
       "raw_payload_committed": false,
       "raw_payload_manifest": "external raw payload manifest SHA-256: $RAW_MANIFEST_SHA",
       "reproduction_level": "not independently reproduced",
       "result_status": "$STATUS",
       "runner_command": "AI-assisted manual runbook docs/manual_audit/EEA_AQ_D001_AI_ASSISTED_TRACK.md plus local external inspection script",
       "sanitized_report_path": "artifacts/eea_aq_d001_ai_assisted_summary.json",
       "sanitized_report_sha256": "$SUMMARY_SHA",
       "source_rights_note": "Official public EEA source; raw payloads and full AI transcripts are not committed."
     }
     EOF
     ```

198. Open the card.

     ```bash
     python3 -m json.tool "$CARD_PATH" | less
     ```

199. Replace `operator` with your actual public operator name or handle.
200. If AI saw raw rows, add that fact to `ai_assistance`.
201. If the result is not `PASSED_UNDER_PROTOCOL`, keep the exact status.
202. Validate the card.

     ```bash
     uv run --extra dev python scripts/claimbound_validate_evidence_card.py "$CARD_PATH"
     ```

203. Fix only validation errors.
204. Do not change the result status to make the validator pass.

## 21. Create The Visual SVG Card

205. Copy the SVG template.

     ```bash
     SVG_PATH="${CARD_PATH%.json}.svg"
     cp docs/assets/claimbound_evidence_card.svg "$SVG_PATH"
     ```

206. Replace placeholders manually in the SVG.
207. Use the evidence card JSON as the source of truth.
208. Suggested replacements:

     ```text
     {{status_exact}} -> the result_status value
     {{reproduction_level}} -> not reproduced, outcome reproduced, or exact level
     {{allowed_claim_sentence}} -> EEA AQ D-001 source-readiness status recorded with disclosed AI assistance
     {{record_id}} -> EEA-AQ-D001-AI
     {{protocol_id}} -> EEA_AQ_D001 ai-assisted-manual-track-v1
     {{target_definition}} -> PM10 daily source coverage
     {{candidate_definition}} -> official EEA E1a records
     {{controls_and_gate}} -> 85 percent coverage, 5 stations per country
     {{source_name}} -> EEA Air Quality Download Service
     {{period_scope}} -> 2018-2024, BE/DE/NL
     {{evidence_date}} -> CARD_DATE
     {{artifact_ref}} -> short commit plus sanitized summary
     {{evidence_url}} -> CARD_PATH
     ```

209. Search for leftover placeholders.

     ```bash
     rg "\\{\\{" "$SVG_PATH"
     ```

210. If placeholders remain, fill them.
211. Open the SVG in a browser.
212. Confirm the card text is readable.
213. Confirm the status matches the JSON card.
214. Confirm the card says AI assistance was disclosed.
215. Confirm there is no broader claim than the JSON card.

## 22. Update The Registry Index

216. Open `docs/registry/evidence_index.json`.
217. Add a new entry for the AI-assisted EEA card under `cards`.
218. Use the JSON card path.
219. Add the SVG URL.
220. Add the result status.
221. Add domain `air-quality`.
222. Add source `EEA Air Quality Download Service`.
223. Add reproduction level.
224. Add execution mode `MANUAL_AI_ASSISTED` if the registry schema supports it.
225. Increment `card_count`.
226. Increment `statistics.by_result_status`.
227. Increment `statistics.by_domain.air-quality`.
228. Increment `statistics.by_source.EEA Air Quality Download Service`.
229. Save the file.
230. Validate JSON formatting.

     ```bash
     python3 -m json.tool docs/registry/evidence_index.json >/tmp/claimbound_registry_check.json
     ```

## 23. If The Track Is Blocked

231. Do not delete the failed notes.
232. Do not ask AI to make the blocked run look successful.
233. Create a sanitized blocked summary JSON.
234. Use `BLOCKED_SOURCE`.
235. Explain exactly what blocked the run.
236. Include whether AI helped diagnose the block.
237. Do not include private browser tokens.
238. Do not include raw payloads.
239. Do not include full private AI transcripts.
240. Create an evidence card anyway.
241. Include `block_reason` in the evidence card if the schema allows it.
242. Validate the card.
243. A blocked card is a valid ClaimBound result.

## 24. Final Local Checks

244. Run tests.

     ```bash
     uv run --extra dev python -m pytest -n auto
     ```

245. Scan for raw payload-like files.

     ```bash
     find . \( -path ./.git -o -path ./.venv -o -path ./.pytest_cache -o -path ./__pycache__ \) -prune -o -type f \( -name '*.csv' -o -name '*.parquet' -o -name '*.zip' -o -name '*.jsonl' -o -name '*.env' -o -name '*.key' -o -name '*.pem' \) -print
     ```

246. The command should not print raw payload files.
247. If it prints your raw payload files, remove them before committing.
248. Scan for unsupported broad claims.

     ```bash
     rg -n -i "universal forecasting edge|deployment readiness|best model|model superiority|breakthrough" artifacts docs
     ```

249. If matches are in forbidden contexts, rewrite the public claim boundary.
250. Validate the evidence card again.
251. Check git status.

     ```bash
     git status --short
     ```

252. Confirm only intended public files changed.

## 25. Commit And Pull Request

253. Stage the sanitized public files.

     ```bash
     git add artifacts/eea_aq_d001_ai_assisted_summary.json
     git add docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-AI-*.json
     git add docs/evidence_cards/CLAIMBOUND-EEA-AQ-D001-AI-*.svg
     git add docs/registry/evidence_index.json
     ```

254. Do not stage `$RUN_ROOT`.
255. Do not stage raw files.
256. Do not stage full AI transcripts.
257. Commit.

     ```bash
     git commit -m "docs: add EEA AQ D-001 AI-assisted evidence card"
     ```

258. Push the branch.

     ```bash
     git push -u origin manual/eea-aq-d001-ai-assisted-result
     ```

259. Open a pull request.
260. In the pull request body, include:

     ```text
     Summary:
     - ran EEA AQ D-001 AI-assisted manual source-readiness track
     - added sanitized summary
     - added evidence card JSON/SVG
     - updated public registry index

     Verification:
     - evidence-card validator passed
     - pytest passed
     - raw payload scan clean
     - AI assistance disclosed

     Raw payload policy:
     - raw files stored outside repository
     - raw payload manifest hash recorded externally

     AI policy:
     - AI prompts and responses stored outside repository
     - AI did not decide status
     - AI did not change gates after result
     ```

261. Wait for GitHub checks.
262. If checks fail, inspect logs.
263. Fix only the real issue.
264. Do not change the result status just to pass checks.
265. Merge only after checks pass.

## 26. Final Review Questions

Before merging, answer these questions:

266. Did the protocol stay fixed from the beginning?
267. Is `execution_mode` set to `MANUAL_AI_ASSISTED`?
268. Did raw payloads stay outside the repository?
269. Did full AI transcripts stay outside the repository?
270. Did the source rights note stay honest?
271. Did the selected stations follow the sorting rule?
272. Did coverage use the fixed 85 percent threshold?
273. Does the public summary avoid raw payload details?
274. Does the evidence card validate?
275. Does the SVG match the JSON card?
276. Does the registry index point to the right card?
277. Does the final claim stay inside source-readiness and coverage only?
278. Did AI avoid deciding the status?
279. Did AI avoid changing gates after result?
280. Did AI avoid selecting favorable stations?
281. Are accepted and rejected AI suggestions recorded?
282. Would another operator understand how to rerun this track?
283. If the result is negative or blocked, is it recorded without shame?
284. If the result passed, are the limitations still visible?

## 27. What To Share

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
- full AI transcripts;
- claims outside this protocol.

## 28. Minimal Public AI Disclosure

Use a short disclosure like this in the evidence card:

```text
AI assistance was used for protocol review, source-checklist support, parser
review and post-result consistency review. AI was not allowed to decide the
result status, change gates after seeing results, choose stations, alter raw
payloads, fabricate hashes, or broaden the claim boundary.
```

Do not publish a vague disclosure such as:

```text
AI helped with the run.
```

That is too broad to audit.
