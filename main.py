import feedparser
import requests
import os

DASHSCOPE_API_KEY = os.getenv("QWEN_API_KEY")

RSS_FEEDS = [
    "https://techcrunch.com/feed/",
    "https://www.theverge.com/rss/index.xml",
    "https://www.wired.com/feed/rss",
    "https://www.reddit.com/r/artificial/.rss"
]


def get_news():

    articles = []

    for feed in RSS_FEEDS:

        data = feedparser.parse(feed)

        for entry in data.entries[:3]:

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary
            })

    return articles


def summarize(text):

    prompt = f"""
请用中文总结以下科技新闻，控制在60字以内：

{text}
"""

    url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    headers = {
        "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "qwen-plus",
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    result = response.json()

    return result["output"]["choices"][0]["message"]["content"]


def generate_report():

    news = get_news()

    report = "# AI科技新闻日报\n\n"

    for item in news:

        summary = summarize(item["summary"])

        report += f"## {item['title']}\n"
        report += f"{summary}\n\n"
        report += f"[阅读原文]({item['link']})\n\n"

    with open("README.md", "w", encoding="utf-8") as f:

        f.write(report)


if __name__ == "__main__":

    generate_report()
