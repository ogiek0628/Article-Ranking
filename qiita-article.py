import requests
from datetime import datetime, timedelta, timezone
from dateutil.parser import isoparse

QIITA_API_URL = "https://qiita.com/api/v2/items"
PER_PAGE = 100
PAGES = 1  # 必要なら2, 3に増やしてもOK（最大取得数 = PAGES × PER_PAGE）

def fetch_qiita_articles():
    articles = []
    for page in range(1, PAGES + 1):
        res = requests.get(QIITA_API_URL, params={"page": page, "per_page": PER_PAGE})
        if res.status_code == 200:
            articles.extend(res.json())
        else:
            print(f"Error fetching page {page}: {res.status_code}")
            break
    return articles

def filter_last_week(articles):
    one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
    return [
        a for a in articles
        if isoparse(a["created_at"]) > one_week_ago
    ]

def format_qiita_article(article):
    user_id = article["user"]["id"]
    article_id = article["id"]
    url = article.get("url", f"/{user_id}/items/{article_id}")
    if not url.startswith("http"):
        url = f"https://qiita.com{url}"
    return f'{article["likes_count"]} 👍  {article["title"]} - {url}'

def show_qiita_weekly_popular():
    print("=== 🗓 Qiita: 今週の人気記事 ===")
    articles = fetch_qiita_articles()
    weekly = filter_last_week(articles)
    sorted_articles = sorted(weekly, key=lambda x: x["likes_count"], reverse=True)
    for article in sorted_articles[:10]:
        print(format_qiita_article(article))

if __name__ == "__main__":
    show_qiita_weekly_popular()
