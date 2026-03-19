---
title: "Module 2: The Interactive UI (Directives & Props)"
layout: default
nav_order: 3
---

# Module 2: The Interactive UI (Directives & Props)

**Goal:** Learn how to make your webpage reactive—where the UI changes instantly when data changes. We use **Vue 3 with the Options API** (`data()`, `computed`, `methods` in `export default { }`).

---

## 1. The Reactivity (data)

In Vue, we store our "State" inside a `data()` function. Any variable here is "reactive"—if you change it in Javascript, the browser updates automatically.

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

## 2. Computed Properties (derived state)

When you need a value that **depends on your data** (e.g. "are there any tasks?", a filtered list), use **computed**. Vue caches the result and only recomputes when the underlying data changes.

```javascript
export default {
    data() {
        return {
            tasks: []
        }
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

In the template: `{{ hasTasks ? 'Yes' : 'No' }}` or `{{ completedCount }}`. Prefer computed over putting complex logic in the template or calling a method repeatedly.

**Learn more:** [Computed Properties \| Vue.js](https://vuejs.org/guide/essentials/computed.html) — caching, when to use computed vs methods, writable computed.

---

## 3. Directives (The "v-" logic)

Vue uses special attributes called **Directives** to add logic to your HTML.

### `v-model`: The Two-Way Connection
Used primarily for forms. It links an input field to a variable in your `data`.
```html
{% raw %}
<input type="text" v-model="username">
<p>Hello, {{ username }}</p> 
<!-- Type in the box, and the text above changes instantly! -->
{% endraw %}
```

### `v-for`: The List Maker
Used to display arrays (like lists of tasks).
```html
{% raw %}
<ul>
    <li v-for="task in tasks" :key="task.id">
        {{ task.title }}
    </li>
</ul>
{% endraw %}
```

### `v-if`: The Logic Gate
Only shows an element if a condition is true.
```html
<p v-if="tasks.length === 0">No tasks found. Relax!</p>
```

---

## 4. Event Handling (`@`)

Instead of `onclick`, Vue uses `@`.

- **`@click`**: React to a mouse click.
- **`@submit.prevent`**: Handle a form submission and stop the page from refreshing (very important in MAD 2!).

```html
<form @submit.prevent="addTask">
    <button type="submit">Add Task</button>
</form>
```

---

## 5. Why no Refreshes?

In MAD 1, every button click usually caused a page reload. In MAD 2, we stay on the same page. We send data to the server in the background, and Vue updates only the parts of the page that changed.

---

## Key Takeaways

1. **`data()`**: The container for all your dynamic information.
2. **`computed`**: Use for derived state (e.g. "has tasks?", counts); Vue caches and only recomputes when dependencies change.
3. **`v-model`**: Essential for forms and user input.
4. **`@submit.prevent`**: The standard way to handle form logic without reloading.

For more on Vue (Options API, reactivity, components), see the [Vue.js Guide](https://vuejs.org/guide).

---

[Previous: Module 1](module1-stack.html){: .btn } [Next: Module 3 - The API Bridge](module3-api.html){: .btn .btn-primary }
