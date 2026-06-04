"""书籍搜索 — LLM 推荐"""
import json
from llm import chat
from prompts import BOOK_SEARCH_SYSTEM, BOOK_SEARCH_USER


async def search_books(topic: str) -> list[dict]:
    """LLM 推荐相关哲学书籍"""
    user_prompt = BOOK_SEARCH_USER.format(topic=topic)
    response = chat(system=BOOK_SEARCH_SYSTEM, user=user_prompt, json_mode=True)
    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return []
