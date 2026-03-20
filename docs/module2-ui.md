---
title: "Module 2: The Interactive UI (Components, Router & Hooks)"
layout: default
nav_order: 3
---

# Module 2: The Interactive UI (Components, Router & Hooks)

**Goal:** Wire **Vue Router**, **axios**, and the **Options API** into a small SPA: multiple **views**, a **child component** (`props` + `$emit`), **lifecycle hooks**, and **template directives**. Together with Module 1, this is enough to build simple apps before Flask-RESTful (Module 3).

{: .note }
Examples use `http://127.0.0.1:5000/...`. **Change host, port, and paths** to match your Flask API. Enable **CORS** on Flask when the Vue dev server runs on another origin (e.g. port 5173).

---

## 1. Reactivity (`data`)

```javascript
export default {
    data() {
        return {
            username: 'Guest',
            tasks: []
        }
    }
}
```

---

## 2. Computed properties

```javascript
computed: {
    hasTasks() {
        return this.tasks.length > 0
    }
}
```

**Learn more:** [Computed Properties](https://vuejs.org/guide/essentials/computed.html)

---

## 3. Methods (`methods`)

Use **`methods`** for clicks, submits, and **axios** calls. Prefer **`@submit.prevent`** on `<form>` so the page does not reload.

---

## 4. Vue Router + minimal project layout

After **`npm create vue@latest`** (with **Router** enabled) or after **`npm install vue-router@4`**, your **src** tree can look like this:

```
task-manager-frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.js
    ├── App.vue
    ├── router/
    │   └── index.js
    ├── views/
    │   ├── HomeView.vue
    │   ├── LoginView.vue
    │   └── SignUp.vue
    └── components/
        └── CompA.vue
```

{: .note }
The scaffold maps **`@`** to **`src/`** (see `vite.config.js`). You can write `import X from '@/components/CompA.vue'` or use relative paths like `'../components/CompA.vue'`.

### `index.html` (typical Vite root)

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Vite App</title>
  </head>
  <body>
    <div id="app"></div>
    <script type="module" src="/src/main.js"></script>
  </body>
</html>
```

### `src/main.js`

```javascript
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).mount('#app')
```

### `src/App.vue` (router outlet only)

```vue
{% raw %}
<template>
  <RouterView />
</template>
{% endraw %}
```

Add `<nav>` with `<router-link>` here if you want global navigation.

### `src/router/index.js`

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/HomeView.vue'
import Login from '../views/LoginView.vue'
import Signup from '../views/SignUp.vue'

export default createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'home', component: Home },
    { path: '/login', name: 'login', component: Login },
    { path: '/signup', name: 'signup', component: Signup }
  ]
})
```

**Learn more:** [Vue Router — Getting Started](https://router.vuejs.org/guide/)

---

## 5. Example views and child component

### `src/views/HomeView.vue`

Parent passes **`msg`** to **`CompA`** and listens for **`@send-data`**. Adjust **`hello()`** to hit a real Flask route (the sample below mirrors a common class exercise pattern).

```vue
{% raw %}
<template>
  <div>
    <h1>Welcome to the Home View</h1>

    <CompA :msg="data" @send-data="onChildData" />

    <p>Child says: {{ dataA }}</p>

    <button type="button" @click="popAlert">alert</button>
    <button type="button" @click="hello">fetch (example API)</button>
  </div>
</template>

<script>
import axios from 'axios'
import CompA from '@/components/CompA.vue'

export default {
  components: {
    CompA
  },
  data() {
    return {
      data: 'data value',
      dataA: 'waiting…',
      users: {}
    }
  },
  methods: {
    popAlert() {
      alert('Hello world! ' + this.data)
    },
    async hello() {
      const token = localStorage.getItem('token')
      const response = await axios.get('http://127.0.0.1:5000/register', {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      })
      console.log(response)
      this.users = response.data.user
      alert(response.data.msg)
    },
    onChildData(payload) {
      alert('received from child: ' + payload)
      this.dataA = payload
    }
  },
  mounted() {
    // Optional: auto-call API when view loads — remove if you prefer manual click only
    // this.hello()
  }
}
</script>

<style scoped>
</style>
{% endraw %}
```

### `src/components/CompA.vue`

```vue
{% raw %}
<template>
  <div class="comp-a">
    <h2>Component A</h2>
    <p>Prop from parent: {{ msg }}</p>
    <button type="button" @click="sendToParent">send data to parent</button>
  </div>
</template>

<script>
export default {
  props: {
    msg: String
  },
  data() {
    return {
      data: 'data from child'
    }
  },
  methods: {
    sendToParent() {
      this.$emit('send-data', this.data)
    }
  }
}
</script>
{% endraw %}
```

### `src/views/LoginView.vue`

Use **`@submit.prevent`** on the form so **Enter** in an input does not reload the page.

```vue
{% raw %}
<template>
  <div>
    <h1>Login</h1>
    <form @submit.prevent="login">
      <input v-model="form.username" type="text" placeholder="username" />
      <input v-model="form.password" type="password" placeholder="password" />
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async login() {
      const response = await axios.post('http://127.0.0.1:5000/login', this.form)
      alert(response.data.msg)
      const token = response.data.token
      if (token) {
        localStorage.setItem('token', token)
      }
    }
  }
}
</script>
{% endraw %}
```

### `src/views/SignUp.vue`

```vue
{% raw %}
<template>
  <div>
    <h1>Signup</h1>
    <form @submit.prevent="register">
      <input v-model="form.username" type="text" placeholder="username" />
      <input v-model="form.email" type="email" placeholder="email" />
      <input v-model="form.phone_number" type="text" placeholder="phone number" />
      <input v-model="form.password" type="password" placeholder="password" />
      <button type="submit">Register</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
        phone_number: '',
        password: ''
      }
    }
  },
  methods: {
    async register() {
      const response = await axios.post('http://127.0.0.1:5000/register', this.form)
      console.log(response)
      alert(response.data.msg)
    }
  }
}
</script>
{% endraw %}
```

---

## 6. Props (parent → child) and `$emit` (child → parent)

| Direction | Mechanism |
|:---|:---|
| Parent → child | **Props**: `:msg="data"` |
| Child → parent | **`this.$emit('event-name', payload)`** and **`@event-name="handler"`** on the child tag |

See **`CompA`** + **`HomeView`** above for a full example.

**Learn more:** [Props](https://vuejs.org/guide/components/props.html) · [Component Events](https://vuejs.org/guide/components/events.html)

---

## 7. Template directives (quick reference)

### `v-if` / `v-else-if` / `v-else`

```html
{% raw %}
<div>
  <p v-if="items.length === 0">No items</p>
  <p v-else-if="loading">Loading…</p>
  <p v-else>Found {{ items.length }} items</p>
</div>
{% endraw %}
```

### `v-show`

Element stays in the DOM; toggles visibility with CSS.

```html
{% raw %}
<div v-show="isVisible">Toggled with v-show</div>
{% endraw %}
```

### `v-for` (lists)

Always use a stable **`:key`** (e.g. `id`).

```html
{% raw %}
<ul>
  <li v-for="item in items" :key="item.id">
    {{ item.title }}
  </li>
</ul>
{% endraw %}
```

### `v-bind` and `v-on` shorthands

- **`:title="expr"`** is short for **`v-bind:title="expr"`**
- **`@click="fn"`** is short for **`v-on:click="fn"`**

**Learn more:** [Template Syntax](https://vuejs.org/guide/essentials/template-syntax.html) · [Conditional Rendering](https://vuejs.org/guide/essentials/conditional.html) · [List Rendering](https://vuejs.org/guide/essentials/list.html)

---

## 8. Lifecycle hooks (examples)

```javascript
export default {
  data() {
    return { items: [] }
  },
  created() {
    // Before mount — good for setup that does not need the DOM
    // this.fetchItems()
  },
  mounted() {
    // DOM is ready — APIs, focus, third-party widgets
    console.log('component mounted')
  },
  beforeUnmount() {
    // Cleanup: timers, listeners
  },
  methods: {
    async fetchItems() {
      /* ... */
    }
  }
}
```

**Learn more:** [Lifecycle Hooks](https://vuejs.org/guide/essentials/lifecycle.html)

---

## 9. Axios patterns (`methods`)

### `data()` shape

```javascript
data() {
  return {
    items: [],
    loading: false,
    form: { title: '', body: '' }
  }
}
```

### Register local components

```javascript
import ChildComp from '@/components/ChildComp.vue'

export default {
  components: { ChildComp }
}
```

### CRUD-style methods

```javascript
methods: {
  async fetchItems() {
    this.loading = true
    try {
      const res = await axios.get('http://127.0.0.1:5000/api/items')
      this.items = res.data
    } finally {
      this.loading = false
    }
  },
  async createItem(payload) {
    const res = await axios.post('http://127.0.0.1:5000/api/items', payload)
    return res.data
  },
  async removeItem(id) {
    await axios.delete(`http://127.0.0.1:5000/api/items/${id}`)
    this.items = this.items.filter(i => i.id !== id)
  }
}
```

### Standalone axios calls

```javascript
await axios.get('http://127.0.0.1:5000/api/items')
await axios.post('http://127.0.0.1:5000/api/items', { title: 'hello' })
await axios.delete('http://127.0.0.1:5000/api/items/123')
```

### Parent / child summary

```html
{% raw %}
<ChildComp :item="selectedItem" @update-item="onUpdateItem" />
{% endraw %}
```

```javascript
methods: {
  onUpdateItem(newData) {
    this.selectedItem = newData
  }
}
```

Child:

```javascript
props: ['item'],
methods: {
  sendUpdate() {
    const payload = { ...this.item, updatedAt: Date.now() }
    this.$emit('update-item', payload)
  }
}
```

---

## 10. Navigation (`router-link` / `$router`)

In any component template:

```html
{% raw %}
<router-link to="/">Home</router-link>
<router-link to="/login">Login</router-link>
{% endraw %}
```

In **methods**:

```javascript
this.$router.push('/login')
```

Read URL params / query: **`this.$route.params`**, **`this.$route.query`**.

---

## 11. Why no full page refreshes?

Vue updates the DOM in place; **Vue Router** swaps views. Flask serves **JSON**; the browser does not reload the whole HTML page for each action (as long as you use **`@submit.prevent`** and client-side navigation).

---

## Key Takeaways

1. **`main.js`**: `createApp(App).use(router).mount('#app')`.
2. **`router/index.js`**: `createWebHistory`, **`routes`**, export **`createRouter`**.
3. **`App.vue`**: **`RouterView`** (and optional **`router-link`** nav).
4. **Forms**: **`@submit.prevent`** + **`type="submit"`** on the button.
5. **axios** + **`localStorage`** for tokens; **props** + **`$emit`** for parent/child.
6. **Directives**: `v-if` / `v-else`, **`v-show`**, **`v-for` + `:key`**, **`:prop`** and **`@event`** shorthands.
7. **Lifecycle**: e.g. **`mounted`** for API calls and DOM setup.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) (Options API) · [Vue Router](https://router.vuejs.org/)

---

[Previous: Module 1](module1-stack.html){: .btn } [Next: Module 3 - The API Bridge](module3-api.html){: .btn .btn-primary }
