---
title: "Module 4: The Session Switch (JWT Auth)"
layout: default
nav_order: 5
---

# Module 4: The Session Switch (JWT Auth)

**Goal:** Understand how to keep users logged in when your Backend is a separate "Grocery Store" (API).

---

## 1. Why skip Sessions?

In MAD 1, Flask used a "Secret Cookie" (Session) to remember you. But in MAD 2, the API is **Stateless**. It is like a store that doesn't remember your face; you must show your ID (Token) every single time you buy something.

## 2. What is a JWT?

**JWT** stands for **JSON Web Token**. It is a long, encoded string that proves who you are.

- **Frontend**: "Here is my username/password."
- **Backend**: "Looks good! Here is a Token. Keep it safe."
- **Frontend**: (Saves token). "I want to see my tasks. Here is my Token."
- **Backend**: "Token is valid. Here are your tasks."

---

## 3. Storing tokens on the Frontend

In Vue, we often use `localStorage` to save the token so the user stays logged in even if they refresh the page.

```javascript
// Saving the token after login
localStorage.setItem('access_token', resp.data.token);

// Getting the token for an API call
const token = localStorage.getItem('access_token');
```

---

## 4. Protecting Routes on the Backend

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

## 5. Sending the Token (The Header)

Whenever the frontend talks to the backend, it sends the token in the **Authorization Header**. It looks like this:
`Authorization: Bearer <your_jwt_token>`

---

## Key Takeaways

1. **Tokens**: Portable "IDs" that the frontend carries.
2. **Stateless**: The server doesn't remember "State"; it only trusts the Token.
3. **localStorage**: A simple way to persist data in the browser.

---

[Previous: Module 3](module3-api.html){: .btn } [Next: Module 5 - The Speed Boost (Redis Caching)](module5-caching.html){: .btn .btn-primary }
