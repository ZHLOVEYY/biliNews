import asyncio
import aiohttp
from typing import List, Dict, Optional
from ..models.bilibili_model import DynamicItem, VideoInfo
from ..utils.cache import RedisCache

class BilibiliService:
    def __init__(self, cookie: str):
        self.cookie = cookie
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Cookie": cookie,
            "Referer": "https://t.bilibili.com/"
        }
        self.cache = RedisCache()

    async def get_user_dynamics(self, uid: str, max_pages: int = 10) -> List[Dict]:
        # 尝试从缓存获取数据
        cache_key = f"bilibili:dynamics:{uid}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        all_dynamics = []
        offset = ""

        async with aiohttp.ClientSession() as session:
            for page in range(1, max_pages + 1):
                url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
                params = {
                    "type": "video",
                    "offset": offset,
                    "features": "itemOpusStyle"
                }

                try:
                    async with session.get(url, headers=self.headers, params=params) as response:
                        result = await response.json()
                        print("\n=== API 请求信息 ===")
                        print(f"请求 URL: {url}")
                        print(f"请求参数: {params}")
                        print(f"响应状态码: {result.get('code')}")
                        print(f"响应消息: {result.get('message')}")
                        print(f"数据项数量: {len(result.get('data', {}).get('items', []))}")
                        
                        # 打印第一条数据的结构
                        if result.get('data', {}).get('items'):
                            first_item = result['data']['items'][0]
                            print("\n=== 第一条动态数据结构 ===")
                            print(f"模块类型: {first_item.get('type')}")
                            print(f"模块列表: {list(first_item.get('modules', {}).keys())}")
                            if 'module_dynamic' in first_item.get('modules', {}):
                                major = first_item['modules']['module_dynamic'].get('major', {})
                                print(f"动态类型: {major.get('type')}")
                        print("=====================")

                        if result["code"] != 0:
                            print(f"B站API错误: {result.get('message', '未知错误')}")
                            break

                        items = result.get("data", {}).get("items", [])
                        if not items:
                            break

                        # 处理动态数据
                        for item in items:
                            try:
                                parsed_data = self._parse_dynamic(item)
                                if parsed_data:  # 不要过滤视频，让解析函数处理
                                    all_dynamics.append(parsed_data)
                                    print(f"成功解析动态")
                            except Exception as e:
                                print(f"解析单条动态出错: {str(e)}")
                                continue

                        # 更新offset
                        if result.get('data', {}).get('offset'):
                            offset = result['data']['offset']
                        else:
                            break

                        await asyncio.sleep(1)  # 添加延时避免请求过快

                except Exception as e:
                    print(f"请求出错: {str(e)}")
                    break

        # 缓存结果
        if all_dynamics:
            await self.cache.set(cache_key, all_dynamics)
        
        return all_dynamics

    async def get_video_info(self, bvid: str) -> Optional[VideoInfo]:
        cache_key = f"bilibili:video:{bvid}"
        cached_data = await self.cache.get(cache_key)
        if cached_data:
            return cached_data

        url = f"https://api.bilibili.com/x/web-interface/view"
        params = {"bvid": bvid}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers, params=params) as response:
                result = await response.json()
                if result['code'] == 0:
                    video_info = VideoInfo.from_api_response(result['data'])
                    await self.cache.set(cache_key, video_info.dict(), expire=3600)
                    return video_info
        return None

    def _parse_dynamic(self, dynamic_item: Dict) -> Dict:
        try:
            author = dynamic_item.get('modules', {}).get('module_author', {})
            content = dynamic_item.get('modules', {}).get('module_dynamic', {})
            stats = dynamic_item.get('modules', {}).get('module_stat', {})

            parsed_data = {
                'author': {
                    'name': author.get('name', '未知用户'),
                    'mid': author.get('mid', ''),
                    'face': author.get('face', '')
                },
                'content': {
                    'text': self._get_dynamic_text(content),
                    'timestamp': author.get('pub_ts', ''),
                    'publish_time': author.get('pub_time', '')
                },
                'stats': {
                    'likes': stats.get('like', {}).get('count', 0),
                    'comments': stats.get('comment', {}).get('count', 0),
                    'forwards': stats.get('forward', {}).get('count', 0)
                }
            }

            if video_info := self._extract_video_info(content):
                parsed_data['video'] = video_info

            return parsed_data
        except Exception as e:
            print(f"解析动态出错: {str(e)}")
            return {}

    @staticmethod
    def _get_dynamic_text(content: Dict) -> str:
        desc = content.get('desc', '')
        if isinstance(desc, dict):
            return desc.get('text', '')
        return desc if isinstance(desc, str) else ''

    @staticmethod
    def _extract_video_info(content: Dict) -> Optional[Dict]:
        if content.get('major', {}).get('type') == 'MAJOR_TYPE_ARCHIVE':
            video_info = content['major'].get('archive', {})
            return {
                'title': video_info.get('title', ''),
                'bvid': video_info.get('bvid', ''),
                'aid': video_info.get('aid', ''),
                'cover': video_info.get('cover', ''),
                'duration': video_info.get('duration_text', ''),
                'play_count': video_info.get('stat', {}).get('play', 0),
                'danmaku_count': video_info.get('stat', {}).get('danmaku', 0),
                'url': f"https://www.bilibili.com/video/{video_info.get('bvid', '')}",
                'description': video_info.get('desc', '')
            }
        return None