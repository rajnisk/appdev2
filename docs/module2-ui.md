---
title: "Module 2: The Interactive UI (Components, Router & Hooks)"
layout: default
nav_order: 3
---

# Module 2: The Interactive UI (Backend Integration)

**Goal:** Connect your Vue frontend to a Flask backend using **axios** or **fetch**, pass data between **parent** and **child** components, and store/retrieve auth tokens with **localStorage**.

{: .note }
Examples use `http://127.0.0.1:5000/...`. **Change host, port, and paths** to match your Flask API. Enable **CORS** on Flask when the Vue dev server runs on another origin (e.g. port 5173).

---

## 1. What this module focuses on

Module 1 already covered the Vue basics. In this module, we use those basics to build the bridge between Vue and Flask.

The main ideas here are:

- calling backend APIs with **axios** or **fetch**
- sending data from **parent to child** with props
- sending data from **child to parent** with `$emit`
- storing a token in **localStorage** after login
- reading the token back from **localStorage** when making API calls

---

## 2. Backend API calls with axios and fetch

Use **axios** or **fetch** inside component methods when you need to talk to Flask.

```javascript
methods: {
  async loadTasks() {
    const token = localStorage.getItem('access_token')

    const response = await axios.get('http://127.0.0.1:5000/api/tasks', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })

    this.tasks = response.data
  },

  async loadTasksWithFetch() {
    const token = localStorage.getItem('access_token')

    const response = await fetch('http://127.0.0.1:5000/api/tasks', {
      headers: token ? { Authorization: `Bearer ${token}` } : {}
    })

    const data = await response.json()
    this.tasks = data
  }
}
```

For forms, keep `@submit.prevent` so the page does not reload.

---

## 3. Vue Router + minimal project layout

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

## 4. Example views, API calls, and child component

### `src/views/HomeView.vue`

Parent passes **`msg`** to **`CompA`** and listens for **`@send-data`**. The view below also shows how to call a backend API with **axios** and how to read a token from **localStorage**.

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
      const token = localStorage.getItem('access_token')
      const response = await axios.get('http://127.0.0.1:5000/api/tasks', {
        headers: token ? { Authorization: `Bearer ${token}` } : {}
      })
      console.log(response)
      this.users = response.data
      alert('Tasks loaded')
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

Use **`@submit.prevent`** on the form so **Enter** in an input does not reload the page. Save the token in **localStorage** after a successful login.

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
        localStorage.setItem('access_token', token)
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

## 5. Props (parent → child) and `$emit` (child → parent)

| Direction | Mechanism |
|:---|:---|
| Parent → child | **Props**: `:msg="data"` |
| Child → parent | **`this.$emit('event-name', payload)`** and **`@event-name="handler"`** on the child tag |

See **`CompA`** + **`HomeView`** above for a full example.

**Learn more:** [Props](https://vuejs.org/guide/components/props.html) · [Component Events](https://vuejs.org/guide/components/events.html)

---

## 6. Token storage and retrieval with localStorage

Use localStorage to keep the token after login, then read it back whenever you call a protected API.

```javascript
// save token after login
localStorage.setItem('access_token', token)

// read token before API calls
const token = localStorage.getItem('access_token')
```

```javascript
methods: {
  logout() {
    localStorage.removeItem('access_token')
  }
}
```

---

## 7. Axios patterns (`methods`)

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

### Fetch pattern

```javascript
const response = await fetch('http://127.0.0.1:5000/api/items')
const data = await response.json()
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

## 8. Navigation (`router-link` / `$router`)

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

## 9. Why no full page refreshes?

Vue updates the DOM in place; **Vue Router** swaps views. Flask serves **JSON**; the browser does not reload the whole HTML page for each action (as long as you use **`@submit.prevent`** and client-side navigation).

---

## Key Takeaways

1. Module 1 covers the Vue basics; Module 2 focuses on wiring the frontend to the backend.
2. Use **axios** or **fetch** to call Flask APIs from Vue components.
3. Store auth tokens in **localStorage** after login and read them back for protected requests.
4. Use **props** to send data from parent to child and **`$emit`** to send data back.
5. `router-link` and `$router` handle navigation when you need route changes.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) (Options API) · [Vue Router](https://router.vuejs.org/)

---

[Previous: Module 1](module1-stack.html){: .btn } [Next: Module 3 - The API Bridge](module3-api.html){: .btn .btn-primary }
