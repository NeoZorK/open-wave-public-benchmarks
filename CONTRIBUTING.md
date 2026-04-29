# Contributing

Contributions are welcome when they preserve the evidence boundary.

Rules:

- do not commit raw CSV, JSON, parquet, ZIP or account-export payloads;
- do not commit secrets, API keys, private paths or personal account screenshots;
- do not add private production integrations or private background technology;
- do not change a frozen target, scorer, control or acceptance gate after seeing
  a result;
- record failed or blocked runs honestly.

Before opening a pull request:

```bash
uv run pytest -n auto
```

