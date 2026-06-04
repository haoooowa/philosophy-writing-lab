"""相关论证检索"""
import json
from llm import chat
from prompts import RELATED_ARGS_SYSTEM, RELATED_ARGS_USER


async def find_related_arguments(argument: str) -> dict:
    """检索支持性、对立性和变体论证"""
    user_prompt = RELATED_ARGS_USER.format(argument=argument)
    response = chat(system=RELATED_ARGS_SYSTEM, user=user_prompt, json_mode=True)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {}
