from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_CONFIG = {
    "brand": {
        "audience": "忙しい働く人",
        "voice": "やさしく、現実的で、責めない",
        "banned_claims": "医療断定や誇張表現は禁止",
        "goal": "睡眠改善の小さな実践を毎日1つ届ける",
    }
}


def load_config(repo_root: Path) -> dict[str, Any]:
    config_path = repo_root / "config.json"
    if not config_path.exists():
        config_path.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2), encoding="utf-8")
        return DEFAULT_CONFIG
    return json.loads(config_path.read_text(encoding="utf-8"))
