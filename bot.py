import os
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # Railway pe environment variable set karna hoga

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Namaste! 😊 Main aapko Hindi dubbed anime list dunga.\n/search likh ke try karo.")

# Search command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Kripya /search ke baad anime ka naam likhein.")
        return

    query = " ".join(context.args).lower()
    url = "https://animesalt.cc/?s=" + query.replace(" ", "+")
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    results = soup.find_all("h2", class_="title")
    if not results:
        await update.message.reply_text("Kuch nahi mila 😔")
        return

    reply_text = "🔍 Search Results:\n\n"
    for r in results[:5]:
        title = r.text.strip()
        link = r.find("a")["href"]
        reply_text += f"{title}\n{link}\n\n"

    await update.message.reply_text(reply_text)

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))

    app.run_polling()
