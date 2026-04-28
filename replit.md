# YouTube Audio Telegram Bot

## Overview
A Telegram bot that downloads audio from YouTube links sent to it and replies with the MP3 file. Built with `python-telegram-bot` (v20.7) and `yt-dlp`, with `ffmpeg` used for audio extraction.

## Project Structure
- `bot.py` — Bot entry point. Listens to text messages, extracts YouTube URLs, downloads audio with `yt-dlp`, and replies with the MP3.
- `requirements.txt` — Python dependencies.
- `runtime.txt` / `Dockerfile` / `Procfile` — Original deploy descriptors from upstream (not used in Replit; kept for reference).

## Environment
- Python 3.11 (Replit module)
- System dependency: `ffmpeg` (already provided by the Replit runtime)
- Python packages: `python-telegram-bot==20.7`, `yt-dlp`

## Secrets
- `TOKEN` — Telegram Bot API token from @BotFather

## Workflow
- `Telegram Bot` — runs `python bot.py` as a console workflow (no port; long-running polling process).

## Deployment
- Target: **VM** (always-on) — required because the bot maintains a long-running polling connection to Telegram.
- Run command: `python bot.py`
