import os
import requests
from datetime import datetime
from dotenv import load_dotenv
from logger_config import setup_logger, log_info

def get_latest_video_info(channel_handle):
    """
    通过YouTube频道的handle获取最新上传视频的信息，包括描述、发布日期和标题。

    参数：
        channel_handle (str): 频道的handle，例如 "@SFZY666"

    返回：
        tuple: (description, formatted_date, video_title)，如果获取失败返回 (None, None, None)
    """

    load_dotenv()
    API_KEY = os.getenv("YOUTUBE_API_KEY")

    try:
        # 1. 通过handle获取频道ID
        handle = channel_handle.lstrip("@")
        search_url = (
            f"https://www.googleapis.com/youtube/v3/search"
            f"?part=snippet&q={handle}&type=channel&key={API_KEY}"
        )
        response = requests.get(search_url)
        response.raise_for_status()
        data = response.json()

        if not data.get("items"):
            print("频道未找到")
            return None, None, None

        channel_id = data["items"][0]["snippet"]["channelId"]

        # 2. 获取频道上传的播放列表ID
        channels_url = (
            f"https://www.googleapis.com/youtube/v3/channels"
            f"?part=contentDetails&id={channel_id}&key={API_KEY}"
        )
        response = requests.get(channels_url)
        response.raise_for_status()
        data = response.json()

        uploads_playlist_id = (
            data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
        )

        # 3. 从上传播放列表中获取最新视频
        playlist_url = (
            f"https://www.googleapis.com/youtube/v3/playlistItems"
            f"?part=snippet&playlistId={uploads_playlist_id}&maxResults=1&key={API_KEY}"
        )
        response = requests.get(playlist_url)
        response.raise_for_status()
        data = response.json()

        if not data.get("items"):
            print("没有找到视频")
            return None, None, None

        video_snippet = data["items"][0]["snippet"]
        video_id = video_snippet["resourceId"]["videoId"]
        published_at = video_snippet["publishedAt"]
        video_title = video_snippet["title"]

        # 格式化发布日期
        published_date = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = published_date.strftime("%Y-%m-%d %H:%M:%S")

        # 4. 获取视频详情（包含说明）
        video_url = (
            f"https://www.googleapis.com/youtube/v3/videos"
            f"?part=snippet&id={video_id}&key={API_KEY}"
        )
        response = requests.get(video_url)
        response.raise_for_status()
        data = response.json()

        if not data.get("items"):
            return None, formatted_date, video_title

        description = data["items"][0]["snippet"]["description"]

        # 打印视频说明信息
        # log_info(f"++++++++++++++++最新视频信息: {video_title}")
        # log_info(f"++++++++++++++++发布时间: {formatted_date}")
        # log_info(f"++++++++++++++++说明: {description}")

        return description, formatted_date, video_title

    except requests.RequestException as e:
        print(f"请求错误: {e}")
        return None, None, None
    except Exception as e:
        print(f"未知错误: {e}")
        return None, None, None
