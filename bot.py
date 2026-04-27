import re
import os
import asyncio
from yt_dlp import YoutubeDL
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest

TOKEN = os.getenv("TOKEN")

YOUTUBE_REGEX = r"(https?://(?:www\.)?(?:youtube\.com|youtu\.be)/[^\s]+)"


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title).80s.%(ext)s',
        'noplaylist': True,
        'quiet': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '0',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return os.path.splitext(filename)[0] + ".mp3", info.get("title", "audio")


async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text or ""
    match = re.search(YOUTUBE_REGEX, text)

    if not match:
        return

    url = match.group(0)
    msg = await update.message.reply_text("⏬ качаю...")

    try:
        loop = asyncio.get_running_loop()
        file_path, title = await loop.run_in_executor(None, download_audio, url)

        if not os.path.exists(file_path):
            raise Exception("Файл не найден")

        size = os.path.getsize(file_path)

        if size > 50 * 1024 * 1024:
            raise Exception("Файл слишком большой (>50MB)")

        with open(file_path, "rb") as audio:
            await update.message.reply_audio(audio=audio, title=title)

        os.remove(file_path)
        await msg.delete()

    except Exception as e:
        print("ERROR:", e)
        await msg.edit_text(f"Ошибка: {e}")


if __name__ == "__main__":
    request = HTTPXRequest(
        connect_timeout=30,
        read_timeout=30,
        write_timeout=30,
        pool_timeout=30,
    )

    app = ApplicationBuilder().token(TOKEN).request(request).build()

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle))

    print("Бот запущен")

    app.run_polling(drop_pending_updates=True)