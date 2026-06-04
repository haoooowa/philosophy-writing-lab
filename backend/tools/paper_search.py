"""论文搜索 — 单次 LLM 调用，中英文 + 书籍一起返回"""
import json
import httpx
from llm import chat

SYSTEM_PROMPT = """你是一位哲学文献专家。用户给出一个主题后，列出相关文献：

- **英文论文** 5 篇
- **中文论文** 3 篇
- **相关书籍** 3 本

每篇只需：title_en, title_cn, authors, year, summary（一句话）。
书籍加 is_book: true。

返回 {"papers": [...], "books": [...]}。只返回 JSON。"""

USER_TEMPLATE = "请推荐与「{topic}」相关的文献。"


async def search_papers(topic: str) -> list[dict]:
    """搜索文献：Semantic Scholar + LLM 合并搜索"""
    results = []

    # 1. Semantic Scholar（快速失败）
    try:
        async with httpx.AsyncClient(timeout=5) as client:
            resp = await client.get(
                "https://api.semanticscholar.org/graph/v1/paper/search",
                params={"query": topic, "limit": 8, "fields": "title,authors,year,abstract"},
            )
            if resp.status_code == 200:
                for paper in resp.json().get("data", []):
                    authors = [a.get("name", "") for a in paper.get("authors", [])]
                    results.append({
                        "title_en": paper.get("title", ""), "title_cn": "",
                        "authors": authors[:3], "year": paper.get("year", ""),
                        "summary": (paper.get("abstract") or "")[:300],
                        "source": "semantic_scholar",
                    })
    except Exception:
        pass

    # 2. LLM 一次调用返回所有内容
    try:
        text = chat(system=SYSTEM_PROMPT, user=USER_TEMPLATE.format(topic=topic), json_mode=True)
        data = json.loads(text)

        existing = {r["title_en"].lower() for r in results}
        for item in data.get("papers", []) + data.get("books", []):
            title = (item.get("title_en") or item.get("title_cn") or "").lower()
            if title and title not in existing:
                item["source"] = "llm"
                existing.add(title)
                results.append(item)
    except Exception:
        pass

    return results
