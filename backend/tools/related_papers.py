"""根据指定论文查找相关文献"""
import json
from llm import chat

SYSTEM_PROMPT = """你是哲学文献专家。用户给出一篇论文，找出 8 篇相关文献。
每篇提供：title_en, title_cn, authors, year, relation（一句话说明关系）。
返回 JSON 数组，只返回 JSON。"""

USER_TEMPLATE = "请查找与以下论文相关的文献：\n\n{paper_info}"


async def find_related_papers(paper_info: str) -> list[dict]:
    """根据论文标题/描述查找相关文献"""
    try:
        text = chat(
            system=SYSTEM_PROMPT,
            user=USER_TEMPLATE.format(paper_info=paper_info),
            json_mode=True,
        )
        return json.loads(text)
    except Exception:
        return []
