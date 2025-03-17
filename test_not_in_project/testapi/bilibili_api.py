import requests
import time

def get_user_dynamics(uid, cookie, start_page=1, end_page=10):
    all_dynamics = []
    offset = ""  # 初始化offset
    
    for page in range(start_page, end_page + 1):
        url = "https://api.bilibili.com/x/polymer/web-dynamic/v1/feed/all"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Cookie": cookie,
            "Referer": "https://t.bilibili.com/"
        }
        
        params = {
            "type": "video",
            "offset": offset,  # 使用当前的offset
            "features": "itemOpusStyle"
        }
        
        response = requests.get(url, headers=headers, params=params)
        result = response.json()
        
        if result['code'] == 0 and result.get('data', {}).get('items'):
            items = result['data']['items']
            all_dynamics.extend(items)
            # 获取下一页的offset
            if result['data'].get('offset'):
                offset = result['data']['offset']
            else:
                break  # 如果没有offset，说明已经到最后一页
        else:
            break
        
        time.sleep(1)  # 添加延时避免请求过快
    
    return all_dynamics

# 可以print方便查看数据配置具体参数