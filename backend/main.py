"""哲学论文写作助手 — FastAPI 后端 + 前端静态文件"""
import time
import os
from collections import defaultdict
from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from tools.paper_search import search_papers
from tools.book_search import search_books
from tools.fallacy_check import check_fallacies
from tools.counterexample import generate_counterexamples
from tools.related_args import find_related_arguments
from tools.related_papers import find_related_papers

# ─── 配置 ───
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "")  # 不设置则跳过认证
MAX_TOPIC_LEN = 2000
MAX_ARGUMENT_LEN = 5000
MAX_PAPER_LEN = 500
RATE_LIMIT = 10      # 每个 IP 每分钟最多 10 次请求
RATE_WINDOW = 60     # 窗口 60 秒

# ─── 简易频率限制（内存） ───
rate_store: dict[str, list[float]] = defaultdict(list)

def check_rate(ip: str) -> bool:
    """返回 True 表示未超频"""
    now = time.time()
    # 清理过期记录
    rate_store[ip] = [t for t in rate_store[ip] if now - t < RATE_WINDOW]
    if len(rate_store[ip]) >= RATE_LIMIT:
        return False
    rate_store[ip].append(now)
    return True

# ─── 应用 ───
app = FastAPI(title="哲学论文写作助手 API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        "https://heartfelt-dragon-6a485f.netlify.app",
        "https://*.trycloudflare.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def security_middleware(request: Request, call_next):
    """统一安全中间件：频率限制 + 认证 + 错误脱敏"""
    ip = request.client.host if request.client else "unknown"

    # 1. 频率限制（health 检查除外）
    if not request.url.path.endswith("/health") and not check_rate(ip):
        return JSONResponse(
            status_code=429,
            content={"error": "请求太频繁，请稍后再试"}
        )

    # 2. 认证（如果配置了 AUTH_TOKEN）
    if AUTH_TOKEN and request.url.path.startswith("/api/"):
        auth = request.headers.get("Authorization", "")
        if auth != f"Bearer {AUTH_TOKEN}":
            return JSONResponse(
                status_code=401,
                content={"error": "未授权"}
            )

    # 3. 执行请求 + 错误脱敏
    try:
        return await call_next(request)
    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "服务器内部错误，请稍后再试"}
        )


from starlette.responses import JSONResponse


# ─── 请求模型（带长度校验） ───

class TopicRequest(BaseModel):
    topic: str = Field(min_length=1, max_length=MAX_TOPIC_LEN)


class ArgumentRequest(BaseModel):
    argument: str = Field(min_length=1, max_length=MAX_ARGUMENT_LEN)


class PaperRequest(BaseModel):
    paper: str = Field(min_length=1, max_length=MAX_PAPER_LEN)


# ─── 统一错误处理 ───

@app.exception_handler(RequestValidationError)
async def validation_handler(request: Request, exc: RequestValidationError):
    # 提取第一条验证错误信息
    errors = exc.errors()
    msg = errors[0]["msg"] if errors else "请求参数无效"
    return JSONResponse(status_code=400, content={"error": msg})


@app.exception_handler(ValueError)
async def value_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"error": str(exc)})


@app.exception_handler(HTTPException)
async def http_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# ─── API 路由 ───

@app.get("/api/health")
async def health():
    return {"status": "ok"}


@app.post("/api/search-papers")
async def api_search_papers(req: TopicRequest):
    papers = await search_papers(req.topic)
    return {"papers": papers, "count": len(papers)}


@app.post("/api/search-books")
async def api_search_books(req: TopicRequest):
    books = await search_books(req.topic)
    return {"books": books, "count": len(books)}


@app.post("/api/check-fallacies")
async def api_check_fallacies(req: ArgumentRequest):
    result = await check_fallacies(req.argument)
    return result


@app.post("/api/counterexamples")
async def api_counterexamples(req: ArgumentRequest):
    result = await generate_counterexamples(req.argument)
    return result


@app.post("/api/related-arguments")
async def api_related_arguments(req: ArgumentRequest):
    result = await find_related_arguments(req.argument)
    return result


@app.post("/api/related-papers")
async def api_related_papers(req: PaperRequest):
    papers = await find_related_papers(req.paper)
    return {"papers": papers, "count": len(papers)}


# 挂载前端（必须在 API 路由之后）
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="frontend")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
