# BotAdminPanel — веб-админка для Telegram-бота

FastAPI-приложение для управления Telegram-ботом через веб-интерфейс.

## Возможности

- **Дашборд** — общая статистика (пользователи, заказы)
- **Пользователи** — список всех пользователей бота
- **Рассылка** — отправка массовых сообщений через бота
- **Авторизация** — сессионная аутентификация

## Стек

- Python 3.9+
- FastAPI
- Jinja2 (шаблоны)
- SQLite
- Tailwind CSS
- Uvicorn

## Установка

```bash
git clone https://github.com/pipupip/bot-admin-panel
cd bot-admin-panel
pip install -r requirements.txt
# настройте config.py
uvicorn main:app --reload
```

## Конфигурация

- `ADMIN_LOGIN` / `ADMIN_PASSWORD` — данные для входа
- `BOT_TOKEN` — токен вашего Telegram-бота
