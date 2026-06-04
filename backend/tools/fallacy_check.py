"""论证漏洞检测"""
import json
from llm import chat
from prompts import FALLACY_CHECK_SYSTEM, FALLACY_CHECK_USER


async def check_fallacies(argument: str) -> dict:
    """分析论证中的逻辑漏洞"""
    user_prompt = FALLACY_CHECK_USER.format(argument=argument)
    response = chat(system=FALLACY_CHECK_SYSTEM, user=user_prompt, json_mode=True)

    try:
        issues = json.loads(response)
    except json.JSONDecodeError:
        return {"issues": [], "total": 0}

    if isinstance(issues, list):
        return {"issues": issues, "total": len(issues)}
    # 如果 LLM 返回了完整分析而非纯数组
    if isinstance(issues, dict) and "issues" in issues:
        return issues
    return {"issues": issues if isinstance(issues, list) else [], "total": 0}
