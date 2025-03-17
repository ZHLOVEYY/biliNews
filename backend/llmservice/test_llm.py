import asyncio
from llm_service import LLMAnalysisService

async def test_llm_analysis():
    # 测试数据
    test_video = {
        "title": "国产汽车，从笑话到神话",
        "text": "兄弟们快来看",
        "description": "国产汽车，十年前还是个笑话，如今却写下属于自己的神话。今天咱们用10分钟，共同精读《基业长青》这本书，分析中国企业崛起的原因，并且尽量推测它未来发展的方向。",
        "play_count": 1704,
        "likes": 0
    }
    
    # 初始化 LLM 服务
    llm_service = LLMAnalysisService()
    
    # 执行分析
    result = await llm_service.analyze_video_content(test_video)
    
    # 打印结果
    print("\n=== LLM 分析结果 ===")
    print(result)
    print("==================")

if __name__ == "__main__":
    asyncio.run(test_llm_analysis())