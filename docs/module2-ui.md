---
title: "Module 2: The Interactive UI (Components, Router & Hooks)"
layout: default
nav_order: 3
---

# Module 2: The Interactive UI (Components, Router & Hooks)

**Goal:** Master the **Vue 3 Options API** pieces you need for **simple apps**: reactive **data**, **computed**, **methods**, **directives**, **props**, **events**, **lifecycle hooks**, and **Vue Router** for multiple “pages” in one SPA.

Together with Module 1, this covers the **basics of Vue 3** before you connect the app to Flask (Module 3).

---

## 1. The Reactivity (`data`)

Store UI state in **`data()`**. Anything returned here is **reactive**—when you change it in JavaScript, the template updates.

```javascript
export default {
    data() {
        return {
            username: "Guest",
            tasks: []
        }
    }
}
```

---

## 2. Computed properties (derived state)

Use **`computed`** when a value is **derived** from `data` (counts, filters, “has items?”). Vue **caches** the result until dependencies change.

```javascript
export default {
    data() {
        return { tasks: [] }
    },
    computed: {
        hasTasks() {
            return this.tasks.length > 0
        },
        completedCount() {
            return this.tasks.filter(t => t.completed).length
        }
    }
}
```

**Learn more:** [Computed Properties](https://vuejs.org/guide/essentials/computed.html)

---

## 3. Methods (`methods`)

Put **functions** that respond to clicks, form submit, or API calls in **`methods`**. Call them from the template with `@click="save"` or `@submit.prevent="addTask"`.

```javascript
export default {
    data() {
        return { newTitle: '', tasks: [] }
    },
    methods: {
        addTask() {
            if (!this.newTitle.trim()) return
            this.tasks.push({
                id: Date.now(),
                title: this.newTitle,
                completed: false
            })
            this.newTitle = ''
        }
    }
}
```

**Computed vs methods:** Use **computed** for pure “calculate a value from state.” Use **methods** for actions and anything with side effects.

---

## 4. Props (parent → child)

The **parent** passes data down with **props**. The **child** declares them (good practice: use an object with `type`).

**Child (`TaskItem.vue`):**
```javascript
export default {
    props: {
        title: { type: String, required: true },
        done: { type: Boolean, default: false }
    }
}
```

**Parent:**
```html
{% raw %}
<TaskItem
  v-for="task in tasks"
  :key="task.id"
  :title="task.title"
  :done="task.completed"
/>
{% endraw %}
```

**Learn more:** [Props](https://vuejs.org/guide/components/props.html)

---

## 5. Events (`$emit`, child → parent)

Children should not mutate props. Instead, the child **emits** an event; the parent listens and updates **its** `data`.

**Child:**
```html
{% raw %}
<button type="button" @click="$emit('toggle', id)">Toggle</button>
{% endraw %}
```

**Parent:**
```html
{% raw %}
<TaskItem
  v-for="task in tasks"
  :key="task.id"
  :title="task.title"
  @toggle="onToggle"
/>
{% endraw %}
```

```javascript
methods: {
    onToggle(id) {
        const t = this.tasks.find(x => x.id === id)
        if (t) t.completed = !t.completed
    }
}
```

**Learn more:** [Component Events](https://vuejs.org/guide/components/events.html)

---

## 6. Directives (the `v-` and `@` syntax)

### `v-model`
Two-way binding on inputs.

```html
{% raw %}
<input type="text" v-model="username">
<p>Hello, {{ username }}</p>
{% endraw %}
```

### `v-for` and `:key`
Lists—always provide a **stable** `:key` (e.g. `id`).

```html
{% raw %}
<ul>
  <li v-for="task in tasks" :key="task.id">{{ task.title }}</li>
</ul>
{% endraw %}
```

### `v-if` / `v-else`
Show or hide blocks (DOM is not rendered when false).

```html
<p v-if="tasks.length === 0">No tasks yet.</p>
```

### `v-show`
Toggle visibility with CSS (`display`); use when you toggle often and the element is cheap to keep in the DOM.

### Event handling
- **`@click`**, **`@submit.prevent`** (prevent default form navigation—important for SPAs!)

```html
{% raw %}
<form @submit.prevent="addTask">
  <input v-model="newTitle" />
  <button type="submit">Add</button>
</form>
{% endraw %}
```

**Learn more:** [Template Syntax](https://vuejs.org/guide/essentials/template-syntax.html) · [Event Handling](https://vuejs.org/guide/essentials/event-handling.html) · [Form Bindings](https://vuejs.org/guide/essentials/forms.html)

---

## 7. Lifecycle hooks (when things run)

Use hooks to run code at specific times in a component’s life (e.g. **fetch data when the view appears**).

| Hook (Options API) | Typical use |
|:---|:---|
| **`created`** | Setup that does not need the DOM yet. |
| **`mounted`** | Access DOM, **call APIs**, start timers, third-party widgets. |
| **`beforeUnmount`** | Cleanup (cancel requests, clear intervals). |

Example: load tasks when the component is mounted.

```javascript
export default {
    data() {
        return { tasks: [], loading: false }
    },
    async mounted() {
        this.loading = true
        try {
            const res = await fetch('/api/tasks')
            this.tasks = await res.json()
        } finally {
            this.loading = false
        }
    }
}
```

**Learn more:** [Lifecycle Hooks](https://vuejs.org/guide/essentials/lifecycle.html)

---

## 8. Vue Router (multiple “pages” in one app)

**Vue Router** maps **URLs** to **components** so users can bookmark `/tasks` vs `/about` without Flask rendering each HTML page.

### Install
```bash
npm install vue-router@4
```

### `router/index.js` (example)
```javascript
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import TasksView from '../views/TasksView.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/tasks', name: 'tasks', component: TasksView }
]

export default createRouter({
  history: createWebHistory(),
  routes
})
```

### `main.js`
```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

const app = createApp(App)
app.use(router)
app.mount('#app')
```

### `App.vue` — links and outlet
```html
{% raw %}
<nav>
  <router-link to="/">Home</router-link> |
  <router-link to="/tasks">Tasks</router-link>
</nav>
<router-view />
{% endraw %}
```

Inside any component you can use **`this.$router.push('/tasks')`** for programmatic navigation and **`this.$route.params`** / **`this.$route.query`** for URL data.

**Learn more:** [Vue Router](https://router.vuejs.org/) · [Getting Started](https://router.vuejs.org/guide/)

---

## 9. Why no full page refreshes?

In MAD 1, many actions reload the whole page. In MAD 2, **Vue** updates only what changed; **Vue Router** swaps views without a round-trip to Flask for HTML. Flask later becomes a **JSON API** (Module 3).

---

## Key Takeaways

1. **`data()`** — reactive state; **`computed`** — derived state; **`methods`** — actions.
2. **`props` / `$emit`** — data down, events up between parent and child.
3. **Directives** — `v-model`, `v-for` + `:key`, `v-if` / `v-show`, `@click`, `@submit.prevent`.
4. **Lifecycle** — e.g. **`mounted`** for API calls and DOM-related setup.
5. **Vue Router** — `routes`, **`<router-view />`**, **`<router-link>`**, `this.$router` / `this.$route`.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) (Options API) + [Vue Router docs](https://router.vuejs.org/).

---

[Previous: Module 1](module1-stack.html){: .btn } [Next: Module 3 - The API Bridge](module3-api.html){: .btn .btn-primary }
