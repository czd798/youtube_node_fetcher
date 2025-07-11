from logger_config import setup_logger, log_info
from youtube import get_latest_video_info
from parser import extract_node_url, find_subscription_context_with_links
from downloader import download_files_to_folder
from datetime import datetime
from dotenv import load_dotenv
import os


def process_latest_video(channel_handle: str) -> None:
    today = datetime.now().strftime("%Y-%m-%d")
    save_folder = os.path.join(".", "V2RayFiles", today)

    description, video_date, video_title = get_latest_video_info(channel_handle)

    log_info("=" * 50)
    log_info(f"视频标题: {video_title or '未知'}")
    log_info(f"发布日期: {video_date or '未知'}")

    if not description:
        log_info("未能成功获取视频描述")
        log_info("=" * 50)
        return

    log_info("视频描述已获取")
    node_url = extract_node_url(description)

    if not node_url:
        log_info("描述中未找到节点获取地址")
        log_info("=" * 50)
        return

    log_info(f"节点获取地址: {node_url}")
    links = find_subscription_context_with_links(node_url)

    if not links:
        log_info("未找到任何有效的订阅链接")
    else:
        log_info(f"共找到 {len(links)} 个可用链接，开始下载...")
        for link in links:
            log_info(link)
        download_files_to_folder(links, save_folder)

    log_info("=" * 50)


if __name__ == "__main__":
    load_dotenv()
    setup_logger()
    process_latest_video(os.getenv("CHANNEL_HANDLE"))

