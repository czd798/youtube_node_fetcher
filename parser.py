import re
from bs4 import BeautifulSoup
import requests

def extract_node_url(description: str) -> str | None:
    if not description:
        return None

    for line in description.splitlines():
        if "本期免费节点获取地址" in line:
            http_pos = line.find("http")
            if http_pos != -1:
                return line[http_pos:].strip()
    return None


def find_subscription_context_with_links(node_url: str) -> list[str]:
    try:
        response = requests.get(node_url, timeout=10)
        response.encoding = "utf-8"
    except Exception:
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    valid_domains = ["drive.google.com"]
    results = set()

    for tag in soup.find_all(string=re.compile("订阅")):
        nearby = tag.parent.find_all_next(string=True, limit=5)
        combined_text = " ".join(nearby)
        links = re.findall(r"https://[^\s\"'>]+", combined_text)

        for link in links:
            if any(domain in link for domain in valid_domains):
                results.add(link)

    return list(results)

