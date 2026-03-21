import asyncio
import logging
import os
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def ffmpeg_video_to_note(input_path: Path, output_path: Path) -> None:
    """
    Convert regular video to Telegram video note format:
    - crop to square
    - scale to 384x384
    - trim to 60 seconds
    """
    import subprocess

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-t",
        "60",
        "-vf",
        "crop='min(iw,ih)':'min(iw,ih)',scale=384:384",
        "-c:v",
        "libx264",
        "-preset",
        "veryfast",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-b:a",
        "96k",
        "-movflags",
        "+faststart",
        str(output_path),
    ]

    subprocess.run(command, check=True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Отправь видео, и я преобразую его в кружок (video note)."
    )


async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    if message is None or message.video is None:
        return

    status = await message.reply_text("Скачиваю и обрабатываю видео...")
    video = message.video

    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)
        source = tmp_path / "source.mp4"
        result = tmp_path / "note.mp4"

        file = await context.bot.get_file(video.file_id)
        await file.download_to_drive(custom_path=str(source))

        try:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, ffmpeg_video_to_note, source, result)
        except Exception as exc:
            logger.exception("Video conversion failed")
            await status.edit_text(f"Ошибка обработки видео: {exc}")
            return

        with result.open("rb") as f:
            await message.reply_video_note(video_note=f)

    await status.delete()


def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError("BOT_TOKEN не найден. Добавь его в .env")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.VIDEO, handle_video))

    logger.info("Bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
