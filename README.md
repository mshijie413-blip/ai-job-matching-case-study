# AI Job Matching Case Study

一个可解释的人岗匹配作品集案例：从简历文本中识别技能，对岗位必备与加分技能进行覆盖率计算，并输出匹配证据与缺口。

> 原课程项目方案包含 OCR、BERT-BiLSTM-CRF、向量检索与知识图谱。本仓库没有冒充缺失的原始模型源码，而是用纯 Python 重建一个透明、可测试的基线，用于展示产品逻辑和评估边界。

## 匹配逻辑

```text
简历文本 → 技能词典归一化 → 必备技能覆盖率
                           → 加分技能覆盖率
                           → 文本余弦相似度
                           → 可解释排序结果
```

综合得分：`70% × 必备技能覆盖率 + 20% × 加分技能覆盖率 + 10% × 文本相似度`。

## 运行

```bash
python3 matcher.py sample_jobs.json "熟悉 Python、FastAPI、RAG 与 PostgreSQL"
python3 -m unittest -v test_matcher.py
```

## 生产化边界

真实招聘场景还需要简历隐私保护、偏差评估、技能本体维护、OCR 误差审计、人工复核和离线评测。本演示不声称具备生产招聘决策能力。
