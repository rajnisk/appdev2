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

If you want the modular Flask example below, install the backend dependencies with:

```bash
pip install flask flask-restful flask-sqlalchemy flask-cors
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

## 2.1 Modular Flask example

The example below splits the app into small files so each file has one job:

- `extensions.py` creates shared objects like `db`
- `models.py` defines database models
- `routes.py` keeps the request handlers
- `app.py` is the entry point that starts the app

This version is intentionally small and copy-pasteable. It gives you one `GET` route and one `POST` route.

### `extensions.py`

```python
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
```

### `models.py`

```python
from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # "admin" | "employee" — only seeded admin or future tooling should set admin
    role = db.Column(db.String(20), nullable=False, default="employee")
    # Used for Flask-Mail reminders; optional for older rows
    email = db.Column(db.String(120), nullable=True)

    tasks = db.relationship(
        "Task",
        backref="owner",
        lazy=True,
        cascade="all, delete-orphan",
    )


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, default="")
    status = db.Column(db.String(40), default="Pending")
    priority = db.Column(db.String(20), default="Medium")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "user_id": self.user_id,
        }
```

### `routes.py`

```python
from flask import jsonify, request
from flask_restful import Api, Resource

from extensions import db
from models import Task


def register_routes(app):
    api = Api(app)

    class TaskListResource(Resource):
        def get(self):
            tasks = Task.query.order_by(Task.id.desc()).all()
            return jsonify({"tasks": [task.to_dict() for task in tasks]})

        def post(self):
            data = request.get_json() or {}
            title = (data.get("title") or "").strip()

            if not title:
                return jsonify({"msg": "title required"}), 400

            task = Task(
                title=title,
                description=data.get("description") or "",
                status=data.get("status") or "Pending",
                priority=data.get("priority") or "Medium",
                user_id=data.get("user_id") or 1,
            )
            db.session.add(task)
            db.session.commit()
            return jsonify({"task": task.to_dict(), "msg": "Task created"}), 201

    api.add_resource(TaskListResource, "/api/tasks")
```

### `app.py`

```python
from flask import Flask
from flask_cors import CORS

from extensions import db
from models import User
from routes import register_routes


def seed_default_user():
    if User.query.first():
        return

    user = User(
        username="admin",
        password_hash="demo-password-hash",
        role="employee",
        email=None,
    )
    db.session.add(user)
    db.session.commit()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taskmanager.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    CORS(app)
    register_routes(app)

    with app.app_context():
        db.create_all()
        seed_default_user()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
```

If you want a startup route for checking that the server is running, add this to `routes.py` inside `register_routes(app)`:

```python
    @app.route("/")
    def home():
        return {"msg": "Flask API is running"}
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
