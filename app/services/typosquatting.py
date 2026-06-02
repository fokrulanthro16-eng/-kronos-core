import json
import os
import re
from functools import lru_cache
from typing import List, Optional

from rapidfuzz import distance as rf_distance, fuzz

from app.config import get_settings
from app.core.logging import get_logger
from app.models.audit import InstallScriptAnalysis, TyposquatMatch

logger = get_logger(__name__)

# The canonical set of popular packages the allowlist-first model defends against
POPULAR_PACKAGES = frozenset({
    "react", "react-dom", "react-router", "react-router-dom", "react-redux",
    "react-hook-form", "react-query",
    "vue", "vue-router", "vuex", "nuxt",
    "angular",
    "express", "koa", "fastify", "hapi",
    "lodash", "lodash.merge", "lodash.clonedeep", "underscore", "ramda",
    "axios", "node-fetch", "got", "superagent",
    "webpack", "webpack-cli", "vite", "rollup", "esbuild", "parcel",
    "typescript", "ts-node",
    "eslint", "prettier",
    "jest", "mocha", "chai", "jasmine", "sinon",
    "moment", "dayjs", "date-fns", "luxon",
    "uuid", "nanoid",
    "dotenv", "cors", "helmet", "morgan", "compression",
    "body-parser", "cookie-parser", "multer",
    "mongoose", "sequelize", "prisma", "typeorm", "knex",
    "jsonwebtoken", "passport", "bcrypt", "bcryptjs",
    "socket.io", "ws",
    "next", "gatsby",
    "redux", "mobx", "zustand", "recoil",
    "styled-components", "tailwindcss", "sass", "postcss",
    "puppeteer", "playwright", "cheerio",
    "sharp", "nodemailer", "stripe",
    "graphql", "apollo-server", "typeorm", "knex",
    "redis", "ioredis", "bull", "bullmq",
    "winston", "pino",
    "joi", "yup", "zod",
    "commander", "yargs", "chalk",
    "glob", "semver", "rxjs", "immer",
    "formik",
    "three", "d3", "chart.js",
    "framer-motion", "gsap",
    "cross-env", "rimraf", "concurrently", "nodemon", "pm2",
})

# Character-substitution pairs commonly exploited in typosquatting
_CHAR_SUBS = [
    ("l", "1"), ("o", "0"), ("i", "l"), ("i", "1"),
    ("-", "_"), ("_", "-"), ("-", ""),
]

# Install script patterns that flag suspicious behavior
_SUSPICIOUS_PATTERNS = [
    r"curl\s+",
    r"wget\s+",
    r"https?://",
    r"net\.connect",
    r"require\([\"']https?[\"']\)",
    r"rm\s+-rf\s+/",
    r"chmod\s+[74]77",
    r"sudo\s+",
    r"eval\s*\(",
    r"child_process",
    r"shelljs",
    r"process\.env\.[A-Z_]{4,}",
    r"\.ssh/",
    r"\.aws/",
    r"\.npmrc",
    r"atob\s*\(",
    r"Buffer\.from\s*\([^,]+,\s*[\"']base64[\"']\)",
    r"fromCharCode",
    r"(?:\\x[0-9a-f]{2}){3,}",  # 3+ consecutive hex escapes = encoded payload
]


@lru_cache(maxsize=1)
def _load_known_typosquats() -> dict:
    path = get_settings().KNOWN_TYPOSQUATS_PATH
    if not os.path.exists(path):
        logger.warning("known_typosquats_missing", path=path)
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _char_sub_match(name: str, target: str) -> bool:
    for old, new in _CHAR_SUBS:
        if name.replace(old, new) == target or name.replace(new, old) == target:
            return True
    return False


def detect_typosquatting(package_name: str) -> List[TyposquatMatch]:
    name = package_name.lower()
    matches: List[TyposquatMatch] = []
    seen: set = set()

    # 1. Check the curated known-typosquats database
    known = _load_known_typosquats().get("known_typosquats", {})
    if name in known:
        return [TyposquatMatch(
            similar_to=known[name],
            distance=1,
            similarity_score=0.97,
            attack_type="known_typosquat",
        )]

    # 2. Levenshtein distance against popular packages
    for popular in POPULAR_PACKAGES:
        if name == popular:
            continue
        dist = rf_distance.Levenshtein.distance(name, popular)
        if dist <= 2:
            attack = "character_substitution" if _char_sub_match(name, popular) else "levenshtein"
            if popular not in seen:
                seen.add(popular)
                matches.append(TyposquatMatch(
                    similar_to=popular,
                    distance=dist,
                    similarity_score=round(fuzz.ratio(name, popular) / 100.0, 3),
                    attack_type=attack,
                ))
        elif dist <= 3 and _char_sub_match(name, popular):
            if popular not in seen:
                seen.add(popular)
                matches.append(TyposquatMatch(
                    similar_to=popular,
                    distance=dist,
                    similarity_score=round(fuzz.ratio(name, popular) / 100.0, 3),
                    attack_type="character_substitution",
                ))

    # 3. Prefix/suffix injection patterns
    for popular in POPULAR_PACKAGES:
        if name == popular or popular in seen:
            continue
        variants = {
            f"node-{popular}", f"{popular}-js", f"{popular}js",
            f"my-{popular}", f"{popular}2", f"{popular}-v2",
            f"{popular}-safe", f"{popular}-fixed", f"{popular}-new",
        }
        if name in variants:
            seen.add(popular)
            matches.append(TyposquatMatch(
                similar_to=popular,
                distance=abs(len(name) - len(popular)),
                similarity_score=round(fuzz.ratio(name, popular) / 100.0, 3),
                attack_type="prefix_suffix",
            ))

    return sorted(matches, key=lambda m: m.distance)[:5]


def analyze_install_scripts(scripts: dict) -> InstallScriptAnalysis:
    analysis = InstallScriptAnalysis(
        has_preinstall="preinstall" in scripts,
        has_postinstall="postinstall" in scripts,
        has_install="install" in scripts,
    )
    risk = 0
    found: List[str] = []

    for hook in ("preinstall", "install", "postinstall", "prepare"):
        text = scripts.get(hook, "")
        if not text:
            continue
        for pat in _SUSPICIOUS_PATTERNS:
            if re.search(pat, text, re.IGNORECASE):
                found.append(f"{hook}: matches /{pat}/")
                risk += 20
        # Detect large base64 blobs
        if len(text) > 300 and re.search(r"[A-Za-z0-9+/]{60,}={0,2}", text):
            found.append(f"{hook}: possible base64 encoded payload")
            risk += 30

    if analysis.has_preinstall or analysis.has_postinstall:
        risk += 10  # baseline penalty for any lifecycle hook

    analysis.suspicious_patterns = found[:10]
    analysis.risk_score = min(risk, 100)
    return analysis
