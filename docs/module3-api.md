---
title: "Module 3: The API Bridge (Flask-RESTful)"
layout: default
nav_order: 4
---

# Module 3: The API Bridge (Flask-RESTful)

**Goal:** Turn your Flask app into a "Data Server" using Flask-RESTful.

---

## 1. What is a RESTful API?

In MAD 1, Flask was a "Delivery Driver" bringing you a full meal (HTML).
In **MAD 2**, Flask is a "Grocery Store". The frontend (Vue) comes to the store, asks for specific items using **JSON**, and then cooks the meal itself.

## 2. Flask-RESTful Resources

Instead of routes with `@app.route`, we use **Resources**. Each Resource handles different actions (GET, POST, etc.) for a specific type of data (like Tasks).

```python
from flask_restful import Resource

class TaskResource(Resource):
    def get(self):
        # Logic to "Read" tasks
        return {"id": 1, "title": "Buy Milk"}

    def post(self):
        # Logic to "Create" a task
        return {"message": "Created!"}, 201
```

---

## 3. Mapping HTTP Methods to CRUD

| Action | HTTP Method | Flask-RESTful Function |
|:---|:---|:---|
| **Create** | POST | `def post(self):` |
| **Read** | GET | `def get(self):` |
| **Update** | PUT / PATCH | `def put(self):` |
| **Delete** | DELETE | `def delete(self):` |

---

## 4. The CORS Problem (The Security Guard)

By default, a browser won't let a website at `localhost:5173` (Vue) talk to a server at `localhost:5001` (Flask). This is a security feature called **Same-Origin Policy**.

To fix this, we use **CORS** (Cross-Origin Resource Sharing).
```python
from flask_cors import CORS
CORS(app) # Tells Flask: "It's okay to talk to other domains!"
```

---

## 5. JSON: The Universal Language

The API doesn't send HTML. It sends **JSON** (Javascript Object Notation). It looks like a Python dictionary:
```json
{
    "title": "Complete MAD 2",
    "completed": false
}
```

---

## 6. Calling the API from Vue

From your Vue app (e.g. in a `methods` block with the Options API), you call the Flask backend using `fetch` or a library like **axios**. CORS allows the browser to accept responses from a different origin (e.g. Vue on `localhost:5173`, Flask on `localhost:5001`).

**GET (read tasks):**
```javascript
methods: {
    async fetchTasks() {
        const resp = await fetch('http://localhost:5001/api/tasks')
        const data = await resp.json()
        this.tasks = data.tasks  // or data, depending on your API shape
    }
}
```

**POST (create task):**
```javascript
methods: {
    async addTask() {
        const resp = await fetch('http://localhost:5001/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title: this.newTitle, completed: false })
        })
        const data = await resp.json()
        this.tasks.push(data)  // or refresh the list
    }
}
```

Call `fetchTasks()` when the component loads (e.g. in a lifecycle hook) and wire `addTask` to your form's `@submit.prevent`. Once CORS is enabled on Flask, the Vue app and the API work together as one "bridge."

---

## Key Takeaways

1. **Resources**: Classes that organize your API logic (GET, POST, PUT, DELETE).
2. **HTTP Methods**: Standardized ways to tell the server what you want to do (CRUD).
3. **CORS**: The vital setting that enables the Vue app to call the Flask API from another origin.
4. **JSON**: The API speaks JSON; the frontend uses `fetch` (or axios) to send and receive it.

---

[Previous: Module 2](module2-ui.html){: .btn } [Next: Module 4 - The Session Switch (JWT Auth)](module4-jwt.html){: .btn .btn-primary }
