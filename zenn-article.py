import requests
from datetime import datetime, timedelta, timezone

def fetch_zenn_articles():
    url = "https://zenn.dev/api/articles?order=latest"
    res = requests.get(url)
    return res.json().get("articles", [])

def get_zenn_weekly_popular_articles(articles, top_n=10):
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    filtered = [
        a for a in articles
        if "published_at" in a and
        datetime.fromisoformat(a["published_at"]) > one_week_ago
    ]
    return sorted(filtered, key=lambda a: a.get("liked_count", 0), reverse=True)[:top_n]

def format_zenn_article(article):
    return {
        "platform": "zenn",
        "title": article["title"],
        "url": f"https://zenn.dev{article['path']}",
        "likes": article["liked_count"],
        "published_at": article["published_at"][:10]
    }

if __name__ == "__main__":
    zenn_raw = fetch_zenn_articles()
    zenn_top = [format_zenn_article(a) for a in get_zenn_weekly_popular_articles(zenn_raw)]

    print("\n🔥 Zenn（今週の人気記事）")
    for a in zenn_top:
        print(f"{a['published_at']} | 👍{a['likes']} | {a['title']} | {a['url']}")
