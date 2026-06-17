---
title: "Module 4: The Session Switch (JWT Auth)"
layout: default
nav_order: 5
---

# Module 4: The Session Switch (JWT Auth)

**Goal:** Understand how to keep users logged in when your Backend is a separate "Grocery Store" (API).

Install the required backend packages with:

```bash
pip install flask flask-restful flask-cors flask-jwt-extended
```

---

## 1. Creating and sending the access token during login

When the user logs in successfully, the backend creates an **access token** and sends it back in the response. In Flask, this is usually done with `create_access_token()` from `flask_jwt_extended`.

```python
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Replace this with real user lookup and password checking
        if username == 'admin' and password == 'admin123':
            token = create_access_token(identity=username)
            return {
                "access_token": token,
                "message": "Login successful"
            }, 200

        return {"message": "Invalid credentials"}, 401
```

Example login route registration:

```python
api.add_resource(LoginResource, '/api/login')
```

From the frontend, the login request sends username and password, then stores the returned token.

```javascript
import axios from 'axios'

methods: {
    async login() {
        const response = await axios.post('http://localhost:5001/api/login', {
            username: this.form.username,
            password: this.form.password
        })

        localStorage.setItem('access_token', response.data.access_token)
        alert(response.data.message)
    }
}
```

---

## 2. Why skip Sessions?

In MAD 1, Flask used a "Secret Cookie" (Session) to remember you. But in MAD 2, the API is **Stateless**. It is like a store that doesn't remember your face; you must show your ID (Token) every single time you buy something.

## 3. What is a JWT?

**JWT** stands for **JSON Web Token**. It is a long, encoded string that proves who you are.

- **Frontend**: "Here is my username/password."
- **Backend**: "Looks good! Here is a Token. Keep it safe."
- **Frontend**: (Saves token). "I want to see my tasks. Here is my Token."
- **Backend**: "Token is valid. Here are your tasks."

---

## 4. Storing tokens on the Frontend

In Vue, we often use `localStorage` to save the token so the user stays logged in even if they refresh the page.

```javascript
// Saving the token after login
localStorage.setItem('access_token', response.data.access_token);

// Getting the token for an API call
const token = localStorage.getItem('access_token');
```

---

## 5. Protecting Routes on the Backend

We use the `@jwt_required()` decorator in Flask to only allow users with a valid token to access certain resources.

```python
from flask_jwt_extended import jwt_required

class TaskResource(Resource):
    @jwt_required()
    def get(self):
        # Only logged-in users see this!
        return {"tasks": [...]}
```

---

## 6. Sending the Token (The Header)

Whenever the frontend talks to the backend, it sends the token in the **Authorization Header**. It looks like this:
`Authorization: Bearer <your_jwt_token>`

---

## Key Takeaways

1. **Tokens**: Portable "IDs" that the frontend carries.
2. **Stateless**: The server doesn't remember "State"; it only trusts the Token.
3. **localStorage**: A simple way to persist data in the browser.

---

[Previous: Module 3](module3-api.html){: .btn } [Next: Module 5 - The Speed Boost (Redis Caching)](module5-caching.html){: .btn .btn-primary }
