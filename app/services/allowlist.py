import json
import os
from functools import lru_cache
from typing import List, Set

from app.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)


@lru_cache(maxsize=1)
def _load() -> Set[str]:
    path = get_settings().ALLOWLIST_PATH
    if not os.path.exists(path):
        logger.warning("allowlist_file_missing", path=path)
        return set()
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    packages = {p.lower() for p in data.get("packages", [])}
    logger.info("allowlist_loaded", count=len(packages))
    return packages


def is_allowlisted(name: str) -> bool:
    return name.lower() in _load()


def get_allowlist() -> List[str]:
    return sorted(_load())
