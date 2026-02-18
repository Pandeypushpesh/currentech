import os
import requests
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
openai.api_key = os.environ.get("OPENAI_API_KEY")

app = Application.builder().token(BOT_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Send command:\n/category geopolitics\n/category science\n/category defence"
    )

async def category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_category = " ".join(context.args)

    url = f"https://newsapi.org/v2/everything?q={user_category}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    news = requests.get(url).json()

    headlines = ""
    for i in range(5):
        headlines += news["articles"][i]["title"] + "\n"

    prompt = f"Convert these current news headlines into 5 short Instagram reel topics:\n{headlines}"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}]
    )

    await update.message.reply_text(response.choices[0].message.content)

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("category", category))

async def handler(request):
    data = await request.json()
    update = Update.de_json(data, app.bot)
    await app.process_update(update)
    return {"status": "ok"}
