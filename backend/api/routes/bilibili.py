from fastapi import APIRouter, HTTPException, Depends  # 添加 Depends
from typing import List, Dict
from ...services.bilibili_service import BilibiliService

router = APIRouter()

@router.post("/user/dynamics/{uid}")  # 确保这里是 POST 方法
async def get_user_dynamics(
    uid: str,
    cookie: str,
    max_pages: int = 1
) -> List[Dict]:
    try:
        bili_service = BilibiliService(cookie)
        dynamics = await bili_service.get_user_dynamics(uid, max_pages=max_pages)
        return dynamics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis/{bvid}")
async def analyze_video(
    bvid: str,
    cookie: str,
    service: BilibiliService = Depends(BilibiliService)  # 修改这里
) -> Dict:
    try:
        video_info = await service.get_video_info(bvid)
        return video_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))