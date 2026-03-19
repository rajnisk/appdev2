---
title: "Module 1: The Modern Stack (Vite & Vue 3)"
layout: default
nav_order: 2
---

# Module 1: The Modern Stack (Vite & Vue 3)

**Goal:** Understand the shift from a monolith (Flask + Jinja) to a decoupled frontend using Vue 3 and Vite. We use **Vue 3 with the Options API** (`export default { data(), computed, methods }` in `.vue` files).

---

## 1. What is Vite?

In MAD 1, the browser requested a page, and Flask sent back the full HTML.
In **MAD 2**, we use **Vite**. It is a modern build tool that makes frontend development incredibly fast. It serves your code to the browser and handles all the complex "bundling" behind the scenes.

## 2. Single File Components (SFCs)

In Vue, we use `.vue` files. These are called **Single File Components**. Instead of having HTML, CSS, and JS in different places, everything for one component lives in one file.

### Structure of a `.vue` file (Options API):
```vue
{% raw %}
<script>
// This is the "Brain" (Logic) — Options API
export default {
  data() {
    return {
      message: 'Hello from Vue!'
    }
  }
}
</script>

<template>
  <!-- This is the "Body" (HTML) -->
  <h1>{{ message }}</h1>
</template>

<style scoped>
/* This is the "Beauty" (CSS) — scoped means it only affects this file! */
h1 {
  color: #42b983;
}
</style>
{% endraw %}
```

Later you will add **`computed`**, **`methods`**, and lifecycle hooks in the same `export default { }` block. See [Creating an Application](https://vuejs.org/guide/essentials/application.html) and [Single-File Components](https://vuejs.org/guide/scaling-up/sfc.html) in the Vue guide.

---

## 3. The Project Entry Point

Every Vue app starts at `main.js`. It takes your root component (usually `App.vue`) and "mounts" it into a specific div in your `index.html`.

### `main.js`
```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app') // Connects to <div id="app"> in index.html
```

---

## 4. Why the change?

| Feature | MAD 1 (Jinja) | MAD 2 (Vue) |
|:---|:---|:---|
| **Rendering** | Server-side (Flask) | Client-side (Browser) |
| **User Experience** | Multi-page (Redirects) | Single Page (No refreshes) |
| **Logic** | Mostly Python | Fast Javascript |

---

## Key Takeaways

1. **Vite**: The "engine" that runs your frontend development (dev server + build).
2. **SFCs**: One `.vue` file with `<script>`, `<template>`, and `<style scoped>`.
3. **Options API**: Use `export default { data() { return { ... } } }` for reactive state in each component.
4. **Mounting**: `main.js` calls `createApp(App).mount('#app')` to attach the root component to the page.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) — choose **Options API** where the docs offer a choice.

---

[Next: Module 2 - The Interactive UI](module2-ui.html){: .btn .btn-primary }
