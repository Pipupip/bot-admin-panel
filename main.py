import asyncio
import logging
import time
from contextlib import asynccontextmanager
from functools import wraps

from fastapi import FastAPI, Request, Form, Depends, HTTPException, RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
import httpx

from config import ADMIN_LOGIN, ADMIN_PASSWORD, BOT_TOKEN, SECRET_KEY
from database import init_db, get_total_users, get_today_orders, get_all_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")

# Rate limiting state
_rate_limit = {}


def rate_limit(max_per_minute: int = 5):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            client_ip = request.client.host if request.client else "unknown"
            now = time.time()
            window = 60
            key = f"{client_ip}:{func.__name__}"
            if key in _rate_limit:
                count, start = _rate_limit[key]
                if now - start < window:
                    if count >= max_per_minute:
                        raise HTTPException(status_code=429, detail="Too many requests. Try again later.")
                    _rate_limit[key] = (count + 1, start)
                else:
                    _rate_limit[key] = (1, now)
            else:
                _rate_limit[key] = (1, now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
app.mount("/static", StaticFiles(directory="static"), name="static")


def require_auth(request: Request):
    if not request.session.get("logged_in"):
        raise HTTPException(status_code=303, detail="Not authenticated", headers={"Location": "/login"})


@app.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    if request.session.get("logged_in"):
        return RedirectResponse("/dashboard", status_code=303)
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
        request.session["logged_in"] = True
        logger.info(f"Успешный вход: {username} с IP {request.client.host if request.client else 'unknown'}")
        return RedirectResponse("/dashboard", status_code=303)
    logger.warning(f"Неудачная попытка входа: {username} с IP {request.client.host if request.client else 'unknown'}")
    return templates.TemplateResponse("login.html", {"request": request, "error": "Неверный логин или пароль"})


@app.get("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=303)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    require_auth(request)
    loop = asyncio.get_event_loop()
    total_users = await loop.run_in_executor(None, get_total_users)
    today_orders = await loop.run_in_executor(None, get_today_orders)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_users": total_users,
        "today_orders": today_orders,
    })


@app.get("/users", response_class=HTMLResponse)
async def users_page(request: Request):
    require_auth(request)
    loop = asyncio.get_event_loop()
    users = await loop.run_in_executor(None, get_all_users)
    return templates.TemplateResponse("users.html", {
        "request": request,
        "users": users,
    })


@app.get("/mailing", response_class=HTMLResponse)
async def mailing_page(request: Request):
    require_auth(request)
    return templates.TemplateResponse("mailing.html", {"request": request})


@app.post("/mailing/send")
@rate_limit(max_per_minute=3)
async def send_mailing(request: Request, message: str = Form(...)):
    require_auth(request)
    loop = asyncio.get_event_loop()
    users = await loop.run_in_executor(None, get_all_users)
    sent = 0
    failed = 0

    async with httpx.AsyncClient(timeout=15) as client:
        for user in users:
            try:
                payload = {
                    "chat_id": user["user_id"],
                    "text": message,
                    "parse_mode": "HTML",
                }
                resp = await client.post(
                    f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                    json=payload,
                )
                if resp.status_code == 200:
                    sent += 1
                else:
                    failed += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                logger.error(f"Ошибка отправки пользователю {user['user_id']}: {e}")
                failed += 1

    return templates.TemplateResponse("mailing.html", {
        "request": request,
        "result": f"✅ Рассылка завершена. Отправлено: {sent}, ошибок: {failed}.",
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
