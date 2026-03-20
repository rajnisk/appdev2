---
title: "Module 1: The Modern Stack (Vite & Vue 3)"
layout: default
nav_order: 2
---

# Module 1: The Modern Stack (Vite & Vue 3)

**Goal:** Create a **Vue 3 + Vite** project from scratch, pick the right tooling, and understand **Single File Components** and **local components**. We use the **Options API** (`export default { data(), methods, components }`).

By the end of Module 1 + Module 2, you should run **`npm run dev`**, open the SPA, and be ready to add **Vue Router**, **axios**, and Flask-backed screens.

---

## 1. What is Vite?

In MAD 1, the browser requested a page, and Flask sent back the full HTML.
In **MAD 2**, we use **Vite**. It is a modern build tool and dev server: it serves your `.vue` files to the browser and bundles them for production.

---

## 2. Create a new Vue project

From a terminal (Node.js installed):

```bash
npm create vue@latest task-manager-frontend
```

You can replace `task-manager-frontend` with any folder name (e.g. `my-first-vue-app`).

Then enter the folder and install dependencies:

```bash
cd task-manager-frontend
npm install
```

Start the dev server:

```bash
npm run dev
```

Vite prints a local URL (often `http://localhost:5173`). Open it in your browser.

---

## 3. Feature selection (`npm create vue@latest`)

When the wizard shows a **checkbox menu**, use **Space** to toggle options and **Enter** to continue.

**Suggested selection:**

| Option | Enable? |
|:---|:---|
| **Router** (SPA / `vue-router`) | Yes — we use Vue Router in Module 2 |
| **ESLint** | Yes — catches mistakes early |
| **Prettier** | Yes — consistent formatting |

Leave other extras (TypeScript, Pinia, Vitest, etc.) **off** unless you already know you want them.

**Experimental features:** Press **Enter** without selecting anything (skip).

**“Skip example code?”** Choose **No** — keep the starter example so you can learn from generated files, then replace or extend them.

{: .note }
If you already created the project **without** Router, add it later: `npm install vue-router@4` and follow Module 2’s router setup.

---

## 4. Install extra packages (HTTP + routing)

For the task-manager style app in Module 2, you typically need **axios** (HTTP) and **Vue Router** (if you did not enable Router in the wizard):

```bash
cd task-manager-frontend
npm install axios vue-router@4
```

---

## 5. Official guide: Vue + Vite

For the **full, up-to-date** steps (wizard options, TypeScript, etc.), use the official docs:

- **[Quick Start — Creating a Vue application](https://vuejs.org/guide/quick-start.html#creating-a-vue-application)** — `npm create vue@latest`, project structure, `npm run dev` / `npm run build`.

---

## 6. Single File Components (SFCs)

Each **`.vue`** file is a **Single File Component**: `<script>`, `<template>`, and optional `<style scoped>` in one place.

```vue
{% raw %}
<script>
export default {
  data() {
    return {
      message: 'Hello from Vue!'
    }
  }
}
</script>

<template>
  <h1>{{ message }}</h1>
</template>

<style scoped>
h1 {
  color: #42b983;
}
</style>
{% endraw %}
```

Add **`computed`**, **`methods`**, **`props`**, lifecycle hooks, and **`components`** in the same `export default { }` as you grow.

**Learn more:** [Creating an Application](https://vuejs.org/guide/essentials/application.html) · [Single-File Components](https://vuejs.org/guide/scaling-up/sfc.html)

---

## 7. Components (building blocks)

A **component** is a reusable UI piece. Your app is a **tree**: `App.vue` can contain children you **import** and register.

### Child (`components/TaskItem.vue`)

```vue
{% raw %}
<script>
export default {
  name: 'TaskItem'
}
</script>

<template>
  <li>Task row (add props in Module 2)</li>
</template>
{% endraw %}
```

### Parent (`App.vue`)

```vue
{% raw %}
<script>
import TaskItem from './components/TaskItem.vue'

export default {
  components: {
    TaskItem
  },
  data() {
    return {
      items: [
        { id: 1, title: 'Learn Vue' },
        { id: 2, title: 'Build API' }
      ]
    }
  }
}
</script>

<template>
  <ul>
    <TaskItem v-for="item in items" :key="item.id" />
  </ul>
</template>
{% endraw %}
```

- **`components: { TaskItem }`** registers the child **locally**.
- Template: **`<TaskItem />`** or **`<task-item />`**.

**Learn more:** [Components Basics](https://vuejs.org/guide/essentials/component-basics.html) · [Component Registration](https://vuejs.org/guide/components/registration.html)

---

## 8. The project entry point (`main.js`)

`main.js` creates the app and **mounts** it to `index.html`. With **Vue Router** (Module 2), you also **`app.use(router)`** before `mount`.

```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app')
```

`index.html` contains `<div id="app"></div>` and loads `/src/main.js` as a module — the scaffold from `create-vue` already does this.

---

## 9. Why the change?

| Feature | MAD 1 (Jinja) | MAD 2 (Vue) |
|:---|:---|:---|
| **Rendering** | Server-side (Flask) | Client-side (Browser) |
| **User Experience** | Multi-page (redirects) | Single Page App (no full reload) |
| **Logic** | Mostly Python | JavaScript in components |
| **UI structure** | Templates + includes | Components + routes |

---

## Key Takeaways

1. **`npm create vue@latest <name>`** → **`cd`** → **`npm install`** → **`npm run dev`**.
2. Enable **Router**, **ESLint**, and **Prettier** in the wizard; skip experimental; **do not** skip example code the first time.
3. Add **`axios`** and **`vue-router@4`** with **`npm install`** when needed.
4. **Vite** = dev server + production build; **SFCs** = one `.vue` file per component.
5. **Module 2** wires **Vue Router**, **axios**, sample **views**, and **parent ↔ child** patterns end-to-end.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) — choose **Options API** where the docs offer a choice.

---

[Next: Module 2 - The Interactive UI](module2-ui.html){: .btn .btn-primary }
