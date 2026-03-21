# Telegram бот: видео -> кружок

Бот принимает обычное видео и отправляет его обратно как `video_note` (кружок).

## 1) Установи зависимости

```bash
cd "/Users/anton/Documents/telegram_video_note_bot"
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Установи ffmpeg (если не установлен)

На macOS через Homebrew:

```bash
brew install ffmpeg
```

Проверка:

```bash
ffmpeg -version
```

## 3) Добавь токен бота

```bash
cp .env.example .env
```

Открой `.env` и подставь токен от `@BotFather`.

## 4) Запуск

```bash
python bot.py
```

## Как использовать

- Открой бота в Telegram.
- Напиши `/start`.
- Отправь видео файлом/видео.
- Бот вернет кружок.
