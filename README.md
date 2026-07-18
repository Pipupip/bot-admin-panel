# Bot Admin Panel

<p align="align">
  <img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Jinja2-B41717?style=for-the-badge&logo=jinja" alt="Jinja2">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/Tailwind_CSS-06B6D4?style=for-the-badge&logo=tailwindcss" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/license-MIT-green?style=for-the-badge" alt="License">
</p>

A web-based admin panel for managing a Telegram bot, built with FastAPI. Provides a clean dashboard, user management, and broadcasting capabilities.

> ⚠️ **Demo / Educational project.** This panel is designed for local administration and is not production-hardened.

## Features

- **Dashboard** — aggregate statistics (users, orders today)
- **Users** — full list of bot users from the database
- **Broadcast** — send bulk messages to all bot users via the Telegram Bot API
- **Authentication** — session-based login with configurable admin credentials

## Tech Stack

- **Python** 3.9+
- **FastAPI**
- **Jinja2** (server-side templates)
- **SQLite**
- **Tailwind CSS** (CDN)
- **Uvicorn**

## Installation

```bash
git clone https://github.com/pipupip/bot-admin-panel
cd bot-admin-panel
pip install -r requirements.txt
```

## Configuration

Edit `config.py`:

```python
ADMIN_LOGIN = "admin"
ADMIN_PASSWORD = "your-secure-password"
BOT_TOKEN = "your-telegram-bot-token"
```

## Running

```bash
uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## Project Structure

```
bot_4_admin_panel/
├── main.py             # FastAPI application entry point
├── config.py           # Configuration (credentials, token)
├── database.py         # SQLite database layer
├── templates/          # Jinja2 HTML templates
│   ├── dashboard.html  # Main dashboard
│   ├── users.html      # User management
│   └── broadcast.html  # Broadcast form
└── requirements.txt    # Dependencies
```

## Deployment

For production-like deployment, run with a production ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Consider adding a reverse proxy (Nginx) and HTTPS for security.

---

<p align="center">Built with ❤️ by <a href="https://github.com/pipupip">pipupip</a></p>
