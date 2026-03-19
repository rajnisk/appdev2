---
title: "Module 2: The Interactive UI (Directives & Props)"
layout: default
nav_order: 3
---

# Module 2: The Interactive UI (Directives & Props)

**Goal:** Learn how to make your webpage reactive—where the UI changes instantly when data changes.

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

## 2. Directives (The "v-" logic)

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

## 3. Event Handling (`@`)

Instead of `onclick`, Vue uses `@`.

- **`@click`**: React to a mouse click.
- **`@submit.prevent`**: Handle a form submission and stop the page from refreshing (very important in MAD 2!).

```html
<form @submit.prevent="addTask">
    <button type="submit">Add Task</button>
</form>
```

---

## 4. Why no Refreshes?

In MAD 1, every button click usually caused a page reload. In MAD 2, we stay on the same page. We send data to the server in the background, and Vue updates only the parts of the page that changed.

---

## Key Takeaways

1. **`data()`**: The container for all your dynamic information.
2. **`v-model`**: Essential for forms and user input.
3. **`@submit.prevent`**: The standard way to handle form logic without reloading.

---

[Previous: Module 1](module1-stack.html){: .btn } [Next: Module 3 - The API Bridge](module3-api.html){: .btn .btn-primary }
