---
title: "Module 6: The Background Worker (Celery & Redis)"
layout: default
nav_order: 7
---

# Module 6: The Background Worker (Celery & Redis)

**Goal:** Understand how to perform heavy tasks (like sending emails) without making the user wait for the page to load.

---

## 1. Async vs. Sync

Imagine a Restaurant:
- **Sync (Waiter)**: You order a steak. The waiter stands at your table and doesn't move until the chef cooks the steak. You can't ask for water, and the waiter can't help others. This is slow!
- **Async (Chef)**: You order a steak. The waiter gives the order to the chef (the "Worker") and immediately comes back to help you or other guests. When the steak is ready, it is brought to you.

## 2. Why use Celery?

Celery is the "Chef" for your Flask app. It handles tasks in the background so your API remains fast and responsive.

### The Ingredients
1. **Flask**: The Waiter (takes the order).
2. **Celery**: The Chef (does the work).
3. **Redis**: The Ticket Rack (stores the list of jobs to do).

---

## 3. Creating a Background Task

We use the `@celery.task` decorator.

```python
from celery import Celery

celery = Celery(app.name, broker='redis://localhost:6379/0')

@celery.task
def send_welcome_email(user_email):
    # This might take 5 seconds to run...
    print(f"Sending email to {user_email}")
    return "Done"
```

---

## 4. Running the Task

Instead of calling the function normally, we use `.delay()`.

```python
@app.route('/register', methods=['POST'])
def register():
    # ... create user logic ...
    
    # Don't make the user wait for the email to send!
    send_welcome_email.delay(email) 
    
    return {"message": "User registered. Check your email soon!"}
```

---

## 5. Periodic vs. Ad-hoc Tasks

- **Ad-hoc**: Triggered by a user action (like clicking "Register").
- **Periodic**: Triggered by a schedule (like sending a reminder every morning at 8 AM).

---

## Key Takeaways

1. **`.delay()`**: The magic word that sends a task to the background.
2. **Broker (Redis)**: The middleman that passes messages between Flask and Celery.
3. **Responsive UI**: Users get a "Success" message immediately, even if the work is still happening.

---

[Previous: Module 5](module5-caching.html){: .btn } [Next: Module 7 - The Visual Report (CSV & Mail)](module7-reports.html){: .btn .btn-primary }
