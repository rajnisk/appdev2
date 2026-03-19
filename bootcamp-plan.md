# MAD 2 Bootcamp: 8-Day Plan (Private)

**Format:** 1.5–2 hours per day · One gap day after Day 0  
**Total:** 8 days (Day 0 → gap → Day 1 → … → Day 7)

**Vue:** We use **Vue 3 with the Options API** (e.g. `data()`, `computed`, `methods`, `export default { }` in `.vue` files), not the Composition API / `<script setup>`.

---

## Overview

We cover **Module 1 and Module 2 first** (Vite/Vue/SFCs, then reactivity/directives/events), then the rest of the stack.

| Day   | Concepts & tools covered | Duration |
|:------|:-------------------------|:---------|
| **Day 0** | Setup & orientation | 1.5–2 hrs |
| *Gap day* | — | — |
| **Day 1** | Introduction, plan rest of bootcamp, revise APP Dev I | 1.5–2 hrs |
| **Day 2** | *(Module 1 first)* Vite, Vue 3 Options API, SFCs, client-side rendering, SPA | 1.5–2 hrs |
| **Day 3** | *(Module 2)* Reactivity, data(), computed, directives (v-model, v-for, v-if), events | 1.5–2 hrs |
| **Day 4** | REST API, JSON, Flask-RESTful, Resources, CRUD, CORS | 1.5–2 hrs |
| **Day 5** | Stateless auth, JWT, localStorage, Bearer token, @jwt_required | 1.5–2 hrs |
| **Day 6** | Redis caching, Flask-Caching; Celery, broker, .delay(), async tasks | 1.5–2 hrs |
| **Day 7** | CSV export, SMTP/email, Celery Beat; Pinia/state, validation, loaders, UX polish | 1.5–2 hrs |

---

## Day 0 — Setup & Orientation  
**Duration:** 1.5–2 hours

**Goal:** Environment ready and big picture clear.

### 1. Environment check (≈20 min)
- [ ] **Node.js** and **npm** — `node -v`, `npm -v`
- [ ] **Redis** installed and running — `redis-cli ping` → `PONG`
- [ ] Repo open; skim project layout and docs

### 2. Tour of the stack (≈30 min)
- **Vite & Vue 3** — frontend build tool and reactive UI
- **Flask-RESTful** — API layer (JSON, not HTML)
- **JWT** — stateless authentication
- **Redis** — caching and task queue broker
- **Celery** — background workers
- Skim glossary terms: SFC, REST, CORS, JWT, stateless, broker

### 3. Optional: first run (≈20–30 min)
- [ ] Run frontend and backend once (e.g. `run.sh`)
- [ ] Open app and API in browser; no deep coding yet

### 4. Plan your calendar (≈10 min)
- [ ] Mark Day 1–7 and the gap day
- [ ] Block 1.5–2 hour slots for each bootcamp day

---

## Gap Day

No formal session. Optional: light recap of stack and APP Dev I (routing, Jinja, DB) if you want a head start for Day 1.

---

## Day 1 — Introduction, Plan Rest of Bootcamp, Revise APP Dev I  
**Duration:** 1.5–2 hours

**Goal:** Shared context, clear plan for Days 2–7, APP Dev I foundations refreshed.

### 1. Introduction (≈25 min)
- **Why MAD 2:** Monolith (Flask + Jinja) → decoupled frontend + API
- **What you’ll build:** Task app — separate frontend, API, tokens, caching, background jobs, reporting
- **Prerequisites:** APP Dev I (Flask, Jinja, SQLAlchemy); Node, Redis
- Map the coming days to concepts (see overview table)

### 2. Plan the rest of the bootcamp (≈20 min)
- **Day 2 (Module 1 first):** Vite, Vue 3 Options API, SFCs  
- **Day 3 (Module 2):** Reactivity, data(), computed, directives, events  
- **Day 4:** REST API, Flask-RESTful, CORS  
- **Day 5:** JWT, localStorage, protected routes  
- **Day 6:** Redis caching + Celery  
- **Day 7:** CSV, email, Celery Beat; state & UX polish  
- Fix time window and format (solo vs group, notes vs code-along)

### 3. Revise APP Dev I (≈45–60 min)
- **Flask routing:** `@app.route`, GET/POST, `request.form`, `redirect`, `url_for`
- **Jinja:** `{{ }}`, `{% for %}`, `{% if %}`, inheritance, blocks
- **SQLAlchemy:** Models, `db.session.add`/`commit`/`query`, relationships
- **Sessions:** `session['user_id']`, login/logout flow
- **Recap:** Re-read notes or build one tiny Flask+Jinja page (e.g. list from DB)

---

## Day 2 — Module 1 first: Vite, Vue 3 (Options API), SFCs, Client-Side Rendering  
**Duration:** 1.5–2 hours

**Concepts & tools:** Vite (build tool, dev server) · Vue 3 with **Options API** · Single File Components (.vue) · `export default { }` with `<template>`, `<style scoped>` · main.js, createApp, mount · client-side vs server-side · SPA (no full-page reloads)

### Practical
- [ ] Create minimal Vite + Vue 3 project (or use starter)
- [ ] One `.vue` component using Options API: message in `data()`, scoped style
- [ ] Run dev server, see hot reload

---

## Day 3 — Module 2: Reactivity, Computed, Directives, Events  
**Duration:** 1.5–2 hours

**Concepts & tools:** Reactive state · `data()` · **computed properties** (derived state, caching) · `v-model` (two-way binding) · `v-for` and `:key` · `v-if` · `@click` · `@submit.prevent` (forms without refresh) · client-side updates, API in background

**Learn more (Vue official guide):** [Computed Properties](https://vuejs.org/guide/essentials/computed.html) — when to use computed vs methods, caching, writable computed.

### Practical
- [ ] Task list in `data()`, render with `v-for`
- [ ] One **computed** (e.g. "Has tasks?" or filtered list)
- [ ] Form with `v-model` and `@submit.prevent` to add task (in-memory ok)
- [ ] `v-if` for “No tasks” when empty

---

## Day 4 — REST API, JSON, Flask-RESTful, CORS  
**Duration:** 1.5–2 hours

**Concepts & tools:** RESTful API · JSON as data format · Flask-RESTful · Resource classes · HTTP methods (GET, POST, PUT, DELETE) → CRUD · CORS (Same-Origin Policy, flask_cors) · frontend calling API (fetch/axios)

### Practical
- [ ] TaskResource (or similar) with GET and POST
- [ ] Enable CORS on Flask app
- [ ] From Vue: call API, show list, add item

---

## Day 5 — Stateless Auth, JWT, localStorage, Protected Routes  
**Duration:** 1.5–2 hours

**Concepts & tools:** Stateless API (no server session) · JWT (JSON Web Token) · Login → token → store → send on every request · `localStorage.setItem` / `getItem` · Authorization: Bearer &lt;token&gt; · flask_jwt_extended · `@jwt_required()` · identity in token

### Practical
- [ ] Login endpoint that returns JWT
- [ ] Save token in localStorage; send in header on later requests
- [ ] Protect one or more resources with `@jwt_required()`, test with/without token

---

## Day 6 — Redis Caching + Celery Background Tasks  
**Duration:** 1.5–2 hours

**Concepts & tools (first half):** Caching (when and why) · Redis as in-memory cache · Flask-Caching · `@cache.cached(timeout=…)` · when not to cache (user-specific, very dynamic data)

**Concepts & tools (second half):** Sync vs async · Celery · broker (Redis) · `@celery.task` · `.delay()` · ad-hoc vs periodic tasks

### Practical
- [ ] Add caching to one GET endpoint; observe behavior
- [ ] One Celery task (e.g. log or dummy email), trigger with `.delay()` from a route

---

## Day 7 — CSV, Email, Celery Beat; State & UX Polish  
**Duration:** 1.5–2 hours

**Concepts & tools (first half):** CSV generation (csv, StringIO) · SMTP, sending email (smtplib or library, MailHog for testing) · Celery Beat, crontab (scheduled tasks) · user-triggered export: button → API → Celery → email or download

**Concepts & tools (second half):** Shared state across pages · Pinia (or simple store) · frontend validation · loading spinners · success/error feedback · confirm before delete · separation of concerns (backend vs frontend)

### Practical
- [ ] One CSV export endpoint; one Celery task that “sends” report (or writes to file)
- [ ] Loading state + one success/error message; optional simple store for current user

---

## Learn more about Vue

Use the **official Vue.js guide** to go deeper. We use Vue 3 with the **Options API**, so focus on those sections.

- **Computed properties:** [https://vuejs.org/guide/essentials/computed.html](https://vuejs.org/guide/essentials/computed.html) — derived state, caching, when to use computed vs methods.
- **Vue 3 docs:** [https://vuejs.org/guide](https://vuejs.org/guide) — template syntax, reactivity, components, and more. Pick "Options API" where the guide offers a choice.

---

## After the bootcamp

- Revisit concepts: Pinia, Beat schedules, cache invalidation.
- Extend the app: more endpoints, file uploads, better UI.
- Keep glossary handy: SFC, REST, JWT, CORS, Redis, Celery, broker, stateless.
