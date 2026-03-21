# Task Manager — Frontend (MAD 2)

**Vue 3 + Vite** SPA: one **`NavBar`** component; everything else is in **`views/`**.

## Layout

```
task-manager-frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.js
    ├── App.vue
    ├── router/index.js
    ├── components/
    │   └── NavBar.vue
    └── views/
        ├── HomeView.vue
        ├── AdminView.vue    # admin-only: summary, email report, clear cache
        ├── LoginView.vue
        └── RegisterView.vue
```

## Setup

```bash
cd task-manager-frontend
npm install
npm run dev
```

API base URL: **`http://127.0.0.1:5000`** (see each view’s `API` constant).

## Auth & roles

`localStorage`: **`token`**, **`username`**, **`role`** (`admin` or `employee`).  
**Admin** link appears only for admins. Route **`/admin`** is blocked for non-admins.
