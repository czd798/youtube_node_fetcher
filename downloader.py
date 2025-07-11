import os
import re
import requests
from urllib.parse import urlparse, parse_qs

def download_files_to_folder(links: list[str], save_folder: str) -> None:
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    for url in links:
        try:
            print(f"正在下载: {url}")
            response = requests.get(url, stream=True, timeout=15)
            response.raise_for_status()

            filename = None
            cd = response.headers.get("content-disposition", "")
            if "filename=" in cd:
                match = re.search(r'filename="?([^"]+)"?', cd)
                if match:
                    filename = match.group(1)

            if not filename:
                parsed = urlparse(url)
                query = parse_qs(parsed.query)
                file_id = query.get("id", ["unknown"])[0]
                filename = f"{file_id}.bin"

            filename = re.sub(r'[\\/*?:"<>|]', "_", filename)
            filepath = os.path.join(save_folder, filename)

            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"保存完成: {filepath}")

        except Exception as e:
            print(f"下载失败: {url}\n错误: {e}")

