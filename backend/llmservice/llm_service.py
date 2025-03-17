from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.schema import StrOutputParser
from typing import Dict
import os
import json

class LLMAnalysisService:
    def __init__(self, api_key: str = None):
        if not api_key:
            raise ValueError("API key is required")
            
        self.llm = ChatOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            model="deepseek/deepseek-chat:free",
            temperature=0.5,
        )
        
    async def analyze_video_content(self, video_info: Dict) -> Dict:
        try:
            print(f"LLM服务收到的视频信息: {video_info}")
            
            # 确保所有必要字段都存在
            if not video_info.get("title"):
                raise ValueError("视频标题不能为空")
                
            analysis_data = {
                "title": str(video_info.get("title", "无标题")),
                "text": str(video_info.get("text", "无附言")),
                "description": str(video_info.get("description", "无描述")),
                "play_count": str(video_info.get("play_count", 0)),
                "likes": str(video_info.get("likes", 0))
            }
            
            print(f"处理后的分析数据: {analysis_data}")
            
            # 创建提示模板
            video_prompt = PromptTemplate.from_template(
                """你是一个专业的视频内容分析助手。请分析以下B站视频内容并严格按照JSON格式返回：
    
                标题：{title}
                博主附言：{text}
                描述：{description}
                数据：播放量 {play_count}，点赞数 {likes}
                
                仅返回如下JSON格式数据（不要包含其他任何文字）：
                {{
                    "summary": "在这里写100字以内的视频内容概述"
                }}
                """
            )
            
            # 创建处理链
            chain = video_prompt | self.llm | StrOutputParser()
            
            # 添加更详细的错误处理
            try:
                result = await chain.ainvoke(analysis_data)
                llm_result = json.loads(result)
            except Exception as e:
                print(f"LLM调用或解析错误: {str(e)}")
                raise
            
            return {
                "video_analysis": {
                    "summary": llm_result.get("summary", "AI分析过程出现错误"),
                    "quality_assessment": "暂无评估"
                }
            }
        except Exception as e:
            print(f"LLM分析错误: {str(e)}")
            print(f"错误类型: {type(e).__name__}")
            print(f"完整错误信息: {str(e)}")
            return {
                "video_analysis": {
                    "summary": f"AI分析过程出现错误: {str(e)}",
                    "quality_assessment": "分析失败"
                }
            }