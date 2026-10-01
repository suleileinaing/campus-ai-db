from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

TEXT2SQL_DIR = Path(__file__).resolve().parent


def _find_project_dir() -> Path:
    for parent in TEXT2SQL_DIR.parents:
        if (parent / "database" / "campus_ai.db").exists():
            return parent
    return TEXT2SQL_DIR.parent


PROJECT_DIR = _find_project_dir()
DEFAULT_DATABASE_PATH = PROJECT_DIR / "database" / "campus_ai.db"
SCHEMA_PATH = PROJECT_DIR / "database" / "schema.sql"
SAMPLE_QUERIES_PATH = PROJECT_DIR / "database" / "sample_queries.sql"
RESULTS_DIR = TEXT2SQL_DIR / "results"

CHATKHU_BASE_URL = "https://factchat-cloud.mindlogic.ai/v1/gateway"


def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


_load_dotenv(TEXT2SQL_DIR / ".env")


def _resolve_db_path() -> Path:
    raw = os.environ.get("TEXT2SQL_DB_PATH", "").strip()
    if not raw:
        return DEFAULT_DATABASE_PATH
    path = Path(raw)
    return path if path.is_absolute() else (PROJECT_DIR / path)


DATABASE_PATH = _resolve_db_path()
CURRENT_TERM = os.environ.get("TEXT2SQL_CURRENT_TERM", "2026-2")


@dataclass
class Settings:
    api_key: str | None = os.environ.get("CHATKHU_API_KEY")
    base_url: str = os.environ.get("CHATKHU_BASE_URL", CHATKHU_BASE_URL)
    model: str = os.environ.get("CHATKHU_MODEL", "")
    temperature: float | None = (
        float(os.environ["CHATKHU_TEMPERATURE"]) if os.environ.get("CHATKHU_TEMPERATURE") else None
    )
    max_repair_attempts: int = int(os.environ.get("TEXT2SQL_MAX_REPAIRS", "2"))
    row_limit: int = int(os.environ.get("TEXT2SQL_ROW_LIMIT", "500"))
    query_timeout_sec: float = float(os.environ.get("TEXT2SQL_TIMEOUT", "10"))
    request_timeout_sec: float = float(os.environ.get("CHATKHU_REQUEST_TIMEOUT", "120"))