---
title: "Module 1: The Modern Stack (Vite & Vue 3)"
layout: default
nav_order: 2
---

# Module 1: The Modern Stack (Vite & Vue 3)

**Goal:** Understand the shift from a monolith (Flask + Jinja) to a decoupled frontend using Vue 3 and Vite.

---

## 1. What is Vite?

In MAD 1, the browser requested a page, and Flask sent back the full HTML.
In **MAD 2**, we use **Vite**. It is a modern build tool that makes frontend development incredibly fast. It serves your code to the browser and handles all the complex "bundling" behind the scenes.

## 2. Single File Components (SFCs)

In Vue, we use `.vue` files. These are called **Single File Components**. Instead of having HTML, CSS, and JS in different places, everything for one component lives in one file.

### Structure of a `.vue` file:
```vue
{% raw %}
<script setup>
// This is the "Brain" (Logic)
const message = "Hello from Vue!"
</script>

<template>
  <!-- This is the "Body" (HTML) -->
  <h1>{{ message }}</h1>
</template>

<style scoped>
/* This is the "Beauty" (CSS) - scoped means it only affects this file! */
h1 {
  color: #42b983;
}
</style>
{% endraw %}
```

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

1. **Vite**: The "engine" that runs your frontend development.
2. **SFCs**: Combining Template, Script, and Style into one `.vue` file.
3. **Mounting**: How the Vue app attaches itself to the webpage.

---

[Next: Module 2 - The Interactive UI](module2-ui.html){: .btn .btn-primary }
