import sys
import asyncio
from redis import Redis
import time

# 添加项目根目录到 Python 路径
sys.path.append("/Users/mac/projects/GO/myproject/bilinews")
from backend.services.bilibili_service import BilibiliService

async def test_cache():
    # B站Cookie
    cookie = "buvid3=86EC46BB-332C-38C3-34B3-1E83E01A52F106864infoc; b_nut=1738936706; _uuid=2F7D1D9F-A55E-93F2-3F77-3DF1C9B110B9807130infoc; enable_web_push=DISABLE; buvid4=60DB9ED7-508B-AE5C-BF6D-DA7EC2A75ABB08448-025020713-D4kPbYJsytkTqcahBgXGXg%3D%3D; buvid_fp=89340eb1bccec523dd4cfab5216fbdff; DedeUserID=1520229333; DedeUserID__ckMd5=e6e263d1e7cc3a17; rpdid=|(kkJlYkmJ0J'u~J)mJY~JR; header_theme_version=CLOSE; bsource=search_bing; enable_feed_channel=ENABLE; home_feed_column=5; CURRENT_QUALITY=80; SESSDATA=2b65ea70%2C1757552659%2C1a51e%2A31CjAGxMuRrUnSuBwBqJEtEh3JpSRtAh9RTjJhEY8H3Jd6mXCtHutOnda3C02SbPeMipASVjB2cmFEWEJ5SW1hNmdDRUh1VjlaSUs1dEZTR0g4OTBiN21FUnN1dXVIZGxsamdTSVpIbDZ1NFloVS0yYzY2NUlsVjBXNEljTmpjR1dILTliRTFrdnZRIIEC; bili_jct=fe500bf59827a5a3f90f1b33ba03cdd9; sid=8r9n1989; b_lsid=B1310B329_195984BEB39; browser_resolution=1466-802; bp_t_offset_1520229333=1044451190718332928; hit-dyn-v2=1; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDIyNzc4NDksImlhdCI6MTc0MjAxODU4OSwicGx0IjotMX0.9WNlL-VU7qIEubmLV2Tskm_NP8sQfuHeEb6UeXqYB0E; bili_ticket_expires=1742277789; CURRENT_FNVAL=4048"
    
    # 初始化服务
    service = BilibiliService(cookie)
    uid = "1520229333"  # 测试用UID
    
    # 第一次请求（无缓存）
    print("第一次请求（无缓存）...")
    start_time = time.time()
    dynamics1 = await service.get_user_dynamics(uid, max_pages=1)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    print(f"获取到 {len(dynamics1)} 条动态")
    
    # 第二次请求（应该走缓存）
    print("\n第二次请求（使用缓存）...")
    start_time = time.time()
    dynamics2 = await service.get_user_dynamics(uid, max_pages=1)
    print(f"耗时: {time.time() - start_time:.2f}秒")
    print(f"获取到 {len(dynamics2)} 条动态")
    
    # 验证缓存是否存在
    redis_client = Redis(host='localhost', port=6379, db=0)
    cache_key = f"bilibili:dynamics:{uid}"
    print(f"\n缓存状态: {'存在' if redis_client.exists(cache_key) else '不存在'}")
    print(f"缓存过期时间: {redis_client.ttl(cache_key)}秒")

if __name__ == "__main__":
    asyncio.run(test_cache())