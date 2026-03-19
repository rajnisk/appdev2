---
title: "Module 1: The Modern Stack (Vite & Vue 3)"
layout: default
nav_order: 2
---

# Module 1: The Modern Stack (Vite & Vue 3)

**Goal:** Set up the **Vite + Vue 3** workflow and learn how to split the UI into **components** so you can build simple multi-part screens. We use **Vue 3 with the Options API** (`export default { data(), methods, components }` in `.vue` files).

By the end of Module 1 + Module 2 together, you should be able to build a **small SPA**: multiple views, reusable pieces, forms, lists, and data loading.

---

## 1. What is Vite?

In MAD 1, the browser requested a page, and Flask sent back the full HTML.
In **MAD 2**, we use **Vite**. It is a modern build tool that makes frontend development incredibly fast. It serves your code to the browser and handles all the complex "bundling" behind the scenes.

---

## 2. Single File Components (SFCs)

In Vue, we use `.vue` files. These are called **Single File Components**. Instead of having HTML, CSS, and JS in different places, everything for one component lives in one file.

### Structure of a `.vue` file (Options API):
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

You will add **`computed`**, **`methods`**, **`props`**, lifecycle hooks, and **`components`** in the same `export default { }` block as you grow.

**Learn more:** [Creating an Application](https://vuejs.org/guide/essentials/application.html) · [Single-File Components](https://vuejs.org/guide/scaling-up/sfc.html)

---

## 3. Components (building blocks)

A **component** is a reusable piece of UI (like a card, a navbar item, or one row in a list). Your app is a **tree**: `App.vue` contains smaller components, which can contain even smaller ones.

### Child component (`components/TaskItem.vue`)
A minimal child only needs a template (and optional `name`). In **Module 2** you will add **props** so the parent can pass each row’s data.

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

### Parent uses the child (`App.vue`)
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

*(Same list with **`:title="item.title"`** once you learn **props** in Module 2.)*

- **`import TaskItem from '...'`** then **`components: { TaskItem }`** registers it **locally** for this file only.
- In the template you can write **`<TaskItem />`** (PascalCase) or **`<task-item />`** (kebab-case).

**Learn more:** [Components Basics](https://vuejs.org/guide/essentials/component-basics.html) · [Component Registration](https://vuejs.org/guide/components/registration.html)

---

## 4. The Project Entry Point

Every Vue app starts at `main.js`. It creates the app, optionally adds **plugins** (e.g. Vue Router in Module 2), and **mounts** the root component into `index.html`.

### `main.js` (simple app, no router yet)
```javascript
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)
app.mount('#app') // Connects to <div id="app"> in index.html
```

---

## 5. Why the change?

| Feature | MAD 1 (Jinja) | MAD 2 (Vue) |
|:---|:---|:---|
| **Rendering** | Server-side (Flask) | Client-side (Browser) |
| **User Experience** | Multi-page (Redirects) | Single Page (No refreshes) |
| **Logic** | Mostly Python | Fast Javascript |
| **UI structure** | Templates + includes | Components + (later) routes |

---

## Key Takeaways

1. **Vite**: Dev server + build for your Vue project.
2. **SFCs**: One file = `<script>` + `<template>` + `<style scoped>`.
3. **Components**: Import child `.vue` files and register them in `components: { }` to compose the UI.
4. **Options API**: `export default { data(), components: { } }` is the shape of each component.
5. **Mounting**: `createApp(App).mount('#app')` attaches the app to the page.

**Next (Module 2):** Props, events (`$emit`), `methods`, directives, **computed**, **lifecycle hooks**, and **Vue Router** so you can navigate between pages and load data.

**Learn more:** [Vue.js Guide](https://vuejs.org/guide) — choose **Options API** where the docs offer a choice.

---

[Next: Module 2 - The Interactive UI](module2-ui.html){: .btn .btn-primary }
