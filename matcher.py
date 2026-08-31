from __future__ import annotations

import json
import math
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Iterable


SKILL_ALIASES = {
    "python": ["python", "pandas"],
    "fastapi": ["fastapi"],
    "rag": ["rag", "retrieval augmented generation", "检索增强"],
    "postgresql": ["postgresql", "postgres", "pg"],
    "react": ["react"],
    "typescript": ["typescript", "ts"],
    "product_design": ["产品设计", "prd", "需求分析"],
    "llm": ["llm", "大模型", "prompt engineering"],
}


def tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9+#.]+|[\u4e00-\u9fff]+", text.lower())


def extract_skills(text: str) -> set[str]:
    normalized = text.lower()
    return {skill for skill, aliases in SKILL_ALIASES.items() if any(alias.lower() in normalized for alias in aliases)}


def cosine_similarity(left: str, right: str) -> float:
    left_counts, right_counts = Counter(tokenize(left)), Counter(tokenize(right))
    if not left_counts or not right_counts:
        return 0.0
    dot = sum(value * right_counts.get(key, 0) for key, value in left_counts.items())
    left_norm = math.sqrt(sum(value * value for value in left_counts.values()))
    right_norm = math.sqrt(sum(value * value for value in right_counts.values()))
    return dot / (left_norm * right_norm)


def coverage(found: set[str], expected: Iterable[str]) -> float:
    expected_set = set(expected)
    return len(found & expected_set) / len(expected_set) if expected_set else 1.0


def rank_jobs(resume_text: str, jobs: list[dict]) -> list[dict]:
    found = extract_skills(resume_text)
    results = []
    for job in jobs:
        required = set(job.get("required_skills", []))
        optional = set(job.get("optional_skills", []))
        required_score = coverage(found, required)
        optional_score = coverage(found, optional)
        text_score = cosine_similarity(resume_text, f"{job['title']} {job.get('description', '')}")
        score = 0.70 * required_score + 0.20 * optional_score + 0.10 * text_score
        results.append(
            {
                "job_id": job["job_id"],
                "title": job["title"],
                "score": round(score, 4),
                "matched_required": sorted(found & required),
                "missing_required": sorted(required - found),
                "matched_optional": sorted(found & optional),
            }
        )
    return sorted(results, key=lambda item: (-item["score"], item["job_id"]))


def main() -> None:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "sample_jobs.json")
    resume = sys.argv[2] if len(sys.argv) > 2 else "熟悉 Python、FastAPI、RAG、PostgreSQL 与产品设计"
    print(json.dumps(rank_jobs(resume, json.loads(path.read_text(encoding="utf-8"))), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
