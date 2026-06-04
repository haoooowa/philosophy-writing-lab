"""配置加载 — 优先读取环境变量，兼容 DeepSeek / Anthropic"""
import os
from dotenv import load_dotenv

load_dotenv()

# API Key：支持 ANTHROPIC_API_KEY 和 ANTHROPIC_AUTH_TOKEN 两种变量名
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN", "")

# Base URL：DeepSeek 兼容接口 vs Anthropic 官方
ANTHROPIC_BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")

# 模型：DeepSeek 代理用 deepseek-v4-pro，Anthropic 官方用 claude-sonnet
DEFAULT_MODEL = os.getenv("ANTHROPIC_MODEL") or os.getenv("ANTHROPIC_DEFAULT_SONNET_MODEL") or "claude-sonnet-4-20250514"
ANTHROPIC_MODEL = os.getenv("PHILOSOPHY_MODEL", DEFAULT_MODEL)
MAX_TOKENS = 2048
TEMPERATURE = 0.7
