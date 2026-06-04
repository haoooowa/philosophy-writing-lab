"""LLM 调用封装 — 单一 _chat 网关，复用 ai-media-agent 模式"""
import json
import anthropic
from config import ANTHROPIC_API_KEY, ANTHROPIC_MODEL, ANTHROPIC_BASE_URL, MAX_TOKENS, TEMPERATURE

client = anthropic.Anthropic(
    api_key=ANTHROPIC_API_KEY,
    base_url=ANTHROPIC_BASE_URL,
)


def chat(system: str, user: str, json_mode: bool = False) -> str:
    """统一的 LLM 调用网关
    - system: 系统提示词（角色定义 + 输出要求）
    - user: 用户输入
    - json_mode: 是否要求 JSON 输出（在 system prompt 中指示）
    """
    messages = [{"role": "user", "content": user}]

    # 如果要求 JSON 输出，在 system prompt 末尾加上格式约束
    system_text = system
    if json_mode:
        system_text += "\n\n你必须只返回一个有效的 JSON 对象，不要包含任何其他文本、解释或 markdown 标记。"

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=MAX_TOKENS,
        system=system_text,
        messages=messages,
        temperature=TEMPERATURE,
        thinking={"type": "disabled"},
    )

    # 提取文本：DeepSeek 可能在 content[0] 返回 thinking 块（text=None）
    # 遍历找到第一个 type='text' 且有内容的块
    text = ""
    for block in response.content:
        if block.type == 'text' and block.text:
            text = block.text
            break

    if not text:
        return ""

    if json_mode:
        # 清理可能的 markdown 代码块包裹
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:]) if len(lines) > 1 else text
        if text.endswith("```"):
            text = text[:-3].strip()
        try:
            json.loads(text)  # 验证可解析
        except json.JSONDecodeError:
            pass  # 返回原始文本，调用方处理

    return text
