---
title: "Module 3: The API Bridge (Flask-RESTful)"
layout: default
nav_order: 4
---

# Module 3: The API Bridge (Flask-RESTful)

**Goal:** Turn your Flask app into a "Data Server" using Flask-RESTful.

## Install Packages

Run this once in the backend folder to install the Flask packages used in this module:

```bash
pip install flask flask-restful flask-cors
```

If you want to use axios in the frontend examples below, install it in the Vue app too:

```bash
npm install axios
```

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
        return {"tasks": [{"id": 1, "title": "Buy Milk", "completed": False}]}

    def post(self):
        # Logic to "Create" a task
        return {"message": "Created!"}, 201

    def put(self):
        # Logic to "Update" a task
        return {"message": "Updated!"}, 200

    def delete(self):
        # Logic to "Delete" a task
        return {"message": "Deleted!"}, 200
```

For a single task, you usually accept an id in the URL:

```python
from flask_restful import Resource

class TaskDetailResource(Resource):
    def get(self, task_id):
        return {"id": task_id, "title": "Buy Milk", "completed": False}

    def post(self, task_id):
        return {"message": f"Created task {task_id}"}, 201

    def delete(self, task_id):
        return {"message": f"Deleted task {task_id}"}, 200
```

Example route registration:

```python
api.add_resource(TaskResource, '/api/tasks')
api.add_resource(TaskDetailResource, '/api/tasks/<int:task_id>')
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

### Using axios

If your Vue app already has axios installed, the calls below are a simple pattern to follow.

**GET (read tasks):**
```javascript
methods: {
    async fetchTasks() {
        const response = await axios.get('http://localhost:5001/api/tasks')
        this.tasks = response.data.tasks  // or response.data, depending on your API shape
    }
}
```

**POST (create task):**
```javascript
methods: {
    async addTask() {
        const response = await axios.post('http://localhost:5001/api/tasks', {
            title: this.newTitle,
            completed: false
        })
        this.tasks.push(response.data)  // or refresh the list
    }
}
```

**DELETE (remove task):**

```javascript
methods: {
    async removeTask(taskId) {
        await axios.delete(`http://localhost:5001/api/tasks/${taskId}`)
        this.tasks = this.tasks.filter(task => task.id !== taskId)
    }
}
```

You can still use `fetch` if you want, but axios keeps the request and response handling a little cleaner for these examples.

Call `fetchTasks()` when the component loads (e.g. in a lifecycle hook) and wire `addTask` to your form's `@submit.prevent`. Once CORS is enabled on Flask, the Vue app and the API work together as one "bridge."

---

## Key Takeaways

1. **Resources**: Classes that organize your API logic (GET, POST, PUT, DELETE).
2. **HTTP Methods**: Standardized ways to tell the server what you want to do (CRUD).
3. **CORS**: The vital setting that enables the Vue app to call the Flask API from another origin.
4. **JSON**: The API speaks JSON; the frontend uses `fetch` (or axios) to send and receive it.

---

[Previous: Module 2](module2-ui.html){: .btn } [Next: Module 4 - The Session Switch (JWT Auth)](module4-jwt.html){: .btn .btn-primary }
