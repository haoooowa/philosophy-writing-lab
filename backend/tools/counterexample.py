"""反例生成"""
import json
from llm import chat
from prompts import COUNTEREXAMPLE_SYSTEM, COUNTEREXAMPLE_USER


async def generate_counterexamples(argument: str) -> dict:
    """为论证生成三类反例"""
    user_prompt = COUNTEREXAMPLE_USER.format(argument=argument)
    response = chat(system=COUNTEREXAMPLE_SYSTEM, user=user_prompt, json_mode=True)

    try:
        return json.loads(response)
    except json.JSONDecodeError:
        return {}
