from http.server import BaseHTTPRequestHandler
import json
import requests
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps({
            "status": "ok",
            "message": "Telegram bot webhook is running on Vercel"
        }).encode())

    def do_POST(self):
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            update = json.loads(body)

            if "message" not in update:
                self.send_response(200)
                self.end_headers()
                return

            chat_id = update["message"]["chat"]["id"]
            text = update["message"].get("text", "").lower()

            if text == "/start":
                reply = (
                    "👋 Welcome!\n\n"
                    "Send me a category to get reel topics from current affairs.\n\n"
                    "Examples:\n"
                    "➡️ technology\n"
                    "➡️ ai\n"
                    "➡️ geopolitics\n"
                    "➡️ india\n"
                    "➡️ space"
                )
            else:
                topics = get_topics(text)

                if not topics:
                    reply = "❌ No news found for this category. Try another topic."
                else:
                    reply = "🔥 Reel Topics from Current Affairs:\n\n"
                    for i, t in enumerate(topics, 1):
                        reply += f"{i}. {t}\n"

            requests.post(TELEGRAM_URL, json={
                "chat_id": chat_id,
                "text": reply
            })

            self.send_response(200)
            self.end_headers()

        except Exception as e:
            print("Error:", e)
            self.send_response(500)
            self.end_headers()


def get_topics(category):
    url = (
        "https://newsapi.org/v2/everything?"
        f"q={category}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    articles = data.get("articles", [])[:5]
    topics = [a["title"] for a in articles if "title" in a]

    return topics
