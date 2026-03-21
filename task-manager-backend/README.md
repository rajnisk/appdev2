# Task Manager — Backend (MAD 2)

Flask **JSON API** (no blueprints): routes live in **`routes.py`**. **Models** in `models.py`. **Celery** jobs in `celery_worker.py`.

## Files

| File | Role |
|------|------|
| `app.py` | App factory, `.env` config, mail/cache/JWT/Celery init, **`ensure_admin()`** |
| `models.py` | **Model** — `User` (role, email), `Task` |
| `routes.py` | **Controller** — `@app.route` only |
| `extensions.py` | `mail`, `cache` |
| `celery_worker.py` | Async email: daily reminders, monthly report, admin “email report” button |

## Setup

1. Copy **`.env.example`** → **`.env`** and set mail + Redis + `ADMIN_EMAIL` (needed for admin emails).

2. Install & run **Redis** (broker + cache).

3. Python venv:

```bash
cd task-manager-backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

4. **Three processes** (3 terminals):

```bash
# Terminal A — API
python app.py
```

```bash
# Terminal B — Celery worker (required for async report + scheduled mail)
celery -A app.celery_app worker --loglevel=info
```

```bash
# Terminal C — Beat (daily reminder + monthly admin report)
celery -A app.celery_app beat --loglevel=info
```

## Default admin

On first run, if **no** user has `role=admin`, one is created from `.env`:

- `ADMIN_USERNAME` (default `admin`)
- `ADMIN_PASSWORD` (default `admin123`)
- `ADMIN_EMAIL` — **set this** so “Email report” and monthly reports work.

If you already have an old SQLite file **without** `role` / `email` columns, delete `taskmanager.db` and run again.

## Endpoints

| Method | Path | Notes |
|--------|------|--------|
| POST | `/register` | JSON: `username`, `password`, optional `email` |
| POST | `/login` | Returns `token`, `username`, `role` |
| GET/POST | `/tasks` | JWT |
| PUT/DELETE | `/tasks/<id>` | JWT |
| GET | `/admin/summary` | JWT + admin; **`@cache.cached`** (60s) |
| POST | `/admin/email-report` | JWT + admin; queues **Celery** task → email CSV |
| POST | `/admin/cache-clear` | JWT + admin; **`cache.clear()`** |

## Gmail

Use a [Google App Password](https://support.google.com/accounts/answer/185833) in `MAIL_PASSWORD`, not your normal Gmail password.
