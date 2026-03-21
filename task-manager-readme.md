# Task Manager — How to run & learn

Full-stack **MAD 2** demo: Flask API + Vue SPA, with **Redis**, **Celery**, **mail**, and **caching**.

---

## What you need installed

- **Python 3**
- **Node.js** + npm
- **Redis** (running locally — used for Celery + cache)

Check Redis: `redis-cli ping` should print `PONG`.

---

## 1. Configure the backend

```bash
cd task-manager-backend
cp .env.example .env
```

Edit **`.env`**: set **`MAIL_USERNAME`**, **`MAIL_PASSWORD`** (Gmail [App Password](https://support.google.com/accounts/answer/185833)), **`ADMIN_EMAIL`**, and keep Redis URLs if Redis is on `127.0.0.1`.

---

## 2. Backend — Python venv + API

```bash
cd task-manager-backend
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Default **admin** (created automatically if no admin exists): **`admin` / `admin123`** — change in `.env`.

---

## 3. Backend — Celery (2 extra terminals)

**Worker** (handles async emails + scheduled jobs):

```bash
cd task-manager-backend
source .venv/bin/activate
celery -A app.celery_app worker --loglevel=info
```

**Beat** (daily employee reminders + monthly admin report):

```bash
cd task-manager-backend
source .venv/bin/activate
celery -A app.celery_app beat --loglevel=info
```

---

## 4. Frontend

```bash
cd task-manager-frontend
npm install
npm run dev
```

Open the URL Vite shows (e.g. **http://localhost:5173**).

---

## 5. Try it (beginner path)

1. Log in as **admin** (`admin` / `admin123` unless you changed `.env`).  
2. Open **Admin** in the nav — see cached **summary**; click **Email me the report** (check inbox after the worker runs).  
3. **Clear server cache** — summary refetches from the database.  
4. **Register** a normal user (optional **email** for daily reminder emails).  
5. Log in as that user — use **Tasks** as before.

---

## If something breaks

| Problem | What to check |
|--------|----------------|
| “Report” never arrives | Celery **worker** running? **`ADMIN_EMAIL`** set? Gmail app password correct? |
| Admin summary errors | **Redis** running? `.env` **`CACHE_REDIS_URL`** correct? |
| Old database errors | Delete **`taskmanager.db`** and restart `python app.py` once. |
| CORS / network | API on **5000**, Vue on **5173** — URLs in Vue must match your Flask host. |

---

## Where to read more

- **`task-manager-backend/README.md`** — API + Celery commands  
- **`task-manager-frontend/README.md`** — Vue layout  
