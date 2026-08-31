import unittest

from matcher import extract_skills, rank_jobs


class JobMatcherTests(unittest.TestCase):
    def test_aliases_are_normalized(self):
        self.assertEqual(extract_skills("使用 Postgres 和检索增强完成项目"), {"postgresql", "rag"})

    def test_ranking_returns_evidence(self):
        jobs = [
            {"job_id": "A", "title": "AI 产品经理", "required_skills": ["product_design", "llm"], "optional_skills": ["rag"], "description": "产品设计与大模型"},
            {"job_id": "B", "title": "前端工程师", "required_skills": ["react", "typescript"], "optional_skills": [], "description": "前端开发"},
        ]
        result = rank_jobs("负责产品设计、RAG 和大模型应用", jobs)
        self.assertEqual(result[0]["job_id"], "A")
        self.assertEqual(result[0]["missing_required"], [])
        self.assertEqual(result[1]["missing_required"], ["react", "typescript"])

    def test_unknown_words_do_not_create_skills(self):
        self.assertEqual(extract_skills("擅长沟通协作"), set())


if __name__ == "__main__":
    unittest.main()
