from pydantic import BaseModel
from typing import Optional, Dict, List

class Author(BaseModel):
    name: str
    mid: str
    face: str

class Content(BaseModel):
    text: str
    timestamp: int
    publish_time: str

class Stats(BaseModel):
    likes: int
    comments: int
    forwards: int

class VideoInfo(BaseModel):
    title: str
    bvid: str
    aid: str
    cover: str
    duration: str
    play_count: int
    danmaku_count: int
    url: str
    description: str

    @classmethod
    def from_api_response(cls, data: Dict) -> 'VideoInfo':
        return cls(
            title=data.get('title', ''),
            bvid=data.get('bvid', ''),
            aid=str(data.get('aid', '')),
            cover=data.get('pic', ''),
            duration=data.get('duration', ''),
            play_count=data.get('stat', {}).get('view', 0),
            danmaku_count=data.get('stat', {}).get('danmaku', 0),
            url=f"https://www.bilibili.com/video/{data.get('bvid', '')}",
            description=data.get('desc', '')
        )

class DynamicItem(BaseModel):
    author: Author
    content: Content
    stats: Stats
    video: Optional[VideoInfo] = None