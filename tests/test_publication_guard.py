# SPDX-License-Identifier: Apache-2.0
"""Publication guard for the Open Wave foreground repository."""

from __future__ import annotations

import ast
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

FORBIDDEN_PATTERNS = (
    "mq" + "l5",
    "meta" + "trader",
    "neozork_" + "q" + "wc" + "_api",
    "/users/" + "rostsh",
    "tr" + "ading",
    "gr" + "ant",
)

FORBIDDEN_IMPORT_PREFIXES = (
    "neozork",
    "server",
    "src." + "mq" + "l5",
    "scripts." + "mq" + "l5",
)

TEXT_SUFFIXES = {".py", ".md", ".toml", ".txt", ".json", ".yml", ".yaml"}


def _text_files() -> list[Path]:
    out: list[Path] = []
    for path in REPO_ROOT.rglob("*"):
        if any(part in {".git", ".venv", ".pytest_cache", "__pycache__", "dist", "build"} for part in path.parts):
            continue
        if path.is_dir():
            continue
        if path.suffix.lower() in TEXT_SUFFIXES or path.name in {"LICENSE", "NOTICE"}:
            out.append(path)
    return out


def test_no_forbidden_public_tokens_or_ru_text() -> None:
    cyrillic = re.compile(r"[\u0400-\u04FF]")
    violations: list[str] = []
    for path in _text_files():
        rel = path.relative_to(REPO_ROOT)
        text = path.read_text(encoding="utf-8", errors="replace")
        lower = text.lower()
        for token in FORBIDDEN_PATTERNS:
            if token in lower:
                violations.append(f"{rel}: forbidden token {token!r}")
        if "_" + "RU" in text:
            violations.append(f"{rel}: internal RU suffix reference")
        if cyrillic.search(text):
            violations.append(f"{rel}: Cyrillic text")
    assert violations == []


def test_python_imports_stay_inside_open_foreground() -> None:
    violations: list[str] = []
    for path in sorted((REPO_ROOT / "src").rglob("*.py")) + sorted((REPO_ROOT / "scripts").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                modules.append(node.module)
            for module in modules:
                if any(module == prefix or module.startswith(f"{prefix}.") for prefix in FORBIDDEN_IMPORT_PREFIXES):
                    violations.append(f"{path.relative_to(REPO_ROOT)} imports {module}")
    assert violations == []
