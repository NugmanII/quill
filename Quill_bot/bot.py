import os
import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# logging
logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("8009195086:AAHIDtA1IDvjEjYDjt5okGaHFSgqbuG8MWA")
CHAT_ID = os.getenv("1512545110")  # ID чата или пользователя, куда слать утреннее сообщение

app = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я журнал-бот. Готов к работе!")

async def morning_prompt():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    text = f"🌅 Доброе утро! Сейчас {now}. Готов записать твои мысли?"
    await app.bot.send_message(chat_id=CHAT_ID, text=text)

@app.on_startup
async def setup_scheduler(application):
    scheduler = AsyncIOScheduler(timezone="Asia/Almaty")
    scheduler.add_job(morning_prompt, trigger="cron", hour=8, minute=0)
    scheduler.start()

def main():
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
