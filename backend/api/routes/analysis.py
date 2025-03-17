from fastapi import APIRouter, HTTPException
from typing import Dict
from ...services.bilibili_service import BilibiliService
from ...llmservice.llm_service import LLMAnalysisService

router = APIRouter()

@router.post("/user/dynamics/analysis/{uid}")
async def analyze_user_dynamics(
    uid: str,
    cookie: str,
    api_key: str,
    max_pages: int = 1
) -> Dict:
    try:
        print("\n=== 开始处理请求 ===")
        print(f"接收到请求 - UID: {uid}, Max Pages: {max_pages}")
        
        bili_service = BilibiliService(cookie)
        print("正在获取B站动态...")
        dynamics = await bili_service.get_user_dynamics(uid, max_pages=max_pages)
        
        if not dynamics:
            print("未获取到任何动态数据")
            return {"error": "未获取到动态数据"}
            
        print(f"\n获取到动态数量: {len(dynamics)}")
        print(f"第一条动态数据示例:")
        print(dynamics[0] if dynamics else "No dynamics")
        
        llm_service = LLMAnalysisService(api_key=api_key)
        analysis_results = []
        
        print("\n=== 开始处理视频数据 ===")
        for idx, dynamic in enumerate(dynamics, 1):
            print(f"\n处理第 {idx} 条动态:")
            print(f"动态内容: {dynamic}")  # 打印完整的动态数据
            
            if video_info := dynamic.get('video'):
                print(f"找到视频信息: {video_info}")
                video_data = {
                    "title": video_info.get("title", ""),
                    "text": dynamic.get("content", {}).get("text", ""),
                    "description": video_info.get("description", ""),
                    "play_count": video_info.get("play_count", 0),
                    "likes": dynamic.get("stats", {}).get("likes", 0)
                }
                
                print(f"准备发送给LLM的数据: {video_data}")
                
                try:
                    analysis = await llm_service.analyze_video_content(video_data)
                    print(f"LLM分析结果: {analysis}")
                    
                    analysis_results.append({
                        "video_info": video_info,
                        "analysis": analysis
                    })
                except Exception as e:
                    print(f"LLM分析出错: {str(e)}")
            else:
                print("该动态不包含视频信息，跳过")
        
        print(f"\n=== 处理完成 ===")
        print(f"成功分析视频数量: {len(analysis_results)}")
        
        return {
            "uid": uid,
            "total_videos": len(analysis_results),
            "analysis_results": analysis_results
        }
    except Exception as e:
        print(f"\n=== 发生错误 ===")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        print(f"错误详情: ", e)
        raise HTTPException(status_code=500, detail=str(e))