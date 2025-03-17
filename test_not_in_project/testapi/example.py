from bilibili_api import get_user_dynamics

def parse_dynamic(dynamic_item):
    try:
        # 获取基础信息
        author = dynamic_item.get('modules', {}).get('module_author', {})
        content = dynamic_item.get('modules', {}).get('module_dynamic', {})
        stats = dynamic_item.get('modules', {}).get('module_stat', {})
        
        # 安全获取文本内容
        text = ''
        if content.get('desc'):
            if isinstance(content['desc'], dict):
                text = content['desc'].get('text', '')
            elif isinstance(content['desc'], str):
                text = content['desc']
        
        # 构建结构化数据
        parsed_data = {
            'author': {
                'name': author.get('name', '未知用户'),
                'mid': author.get('mid', ''),
                'face': author.get('face', '')
            },
            'content': {
                'text': text,
                'timestamp': author.get('pub_ts', ''),
                'publish_time': author.get('pub_time', '')
            },
            'stats': {
                'likes': stats.get('like', {}).get('count', 0),
                'comments': stats.get('comment', {}).get('count', 0),
                'forwards': stats.get('forward', {}).get('count', 0)
            }
        }
        
        # 获取视频信息（如果有）
        if content.get('major', {}).get('type') == 'MAJOR_TYPE_ARCHIVE':
            video_info = content['major'].get('archive', {})
            parsed_data['video'] = {
                'title': video_info.get('title', ''),
                'bvid': video_info.get('bvid', ''),
                'aid': video_info.get('aid', ''),
                'cover': video_info.get('cover', ''),
                'duration': video_info.get('duration_text', ''),
                'play_count': video_info.get('stat', {}).get('play', 0),
                'danmaku_count': video_info.get('stat', {}).get('danmaku', 0),
                'url': f"https://www.bilibili.com/video/{video_info.get('bvid', '')}",
                'description': video_info.get('desc', ''),  # 添加视频描述
            }
        
        return parsed_data
    except Exception as e:
        print(f"解析错误: {str(e)}")
        return None

# B站登录后的Cookie
cookie = "你的cookie"
# 用户UID 个人主页页面后面的数字
uid = "你的uid"

# 获取动态数据并解析
dynamics_list = get_user_dynamics(uid, cookie, start_page=1, end_page=6)

# 遍历所有动态
if not dynamics_list:
    print("获取动态失败或没有数据")
else:
    for item in dynamics_list:
        parsed = parse_dynamic(item)
        if parsed:
            print("\n=== 动态信息 ===")
            print(f"作者: {parsed['author']['name']}")
            print(f"动态内容: {parsed['content']['text']}")
            if 'video' in parsed:
                print(f"视频标题: {parsed['video']['title']}")
                if parsed['video']['description']:  # 只在有描述时显示
                    print(f"视频简介: {parsed['video']['description']}")
                print(f"播放量: {parsed['video']['play_count']}")
                print(f"视频链接: {parsed['video']['url']}")
            print(f"点赞数: {parsed['stats']['likes']}")
            print(f"发布时间: {parsed['content']['publish_time']}")
            print("================")

# 删除重复的请求
# dynamics_list = get_user_dynamics(uid, cookie, start_page=1, end_page=5)
# dynamics_list = get_user_dynamics(uid, cookie)
