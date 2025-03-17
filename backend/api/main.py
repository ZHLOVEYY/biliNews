from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routes import analysis, bilibili

app = FastAPI(title="BiliNews API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(bilibili.router, prefix="/api/bilibili")  # 确保这个在前面
app.include_router(analysis.router, prefix="/api/analysis")