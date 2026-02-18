from http.server import BaseHTTPRequestHandler
import json
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

class handler(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        update = json.loads(body)

        chat_id = update["message"]["chat"]["id"]
        text = update["message"]["text"].lower()

        topics = get_topics(text)

        reply = "🔥 Reel Topics from Current Affairs:\n\n"
        for i, t in enumerate(topics, 1):
            reply += f"{i}. {t}\n"

        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": chat_id, "text": reply}
        )

        self.send_response(200)
        self.end_headers()


def get_topics(category):
    url = f"https://newsapi.org/v2/everything?q={category}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    r = requests.get(url).json()

    articles = r.get("articles", [])[:5]

    topics = []
    for a in articles:
        topics.append(a["title"])

    return topics
