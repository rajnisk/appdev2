---
title: "Module 5: The Speed Boost (Redis Caching)"
layout: default
nav_order: 6
---

# Module 5: The Speed Boost (Redis Caching)

**Goal:** Make your API lightning fast by remembering the results of expensive operations.

Install the required backend packages with:

```bash
pip install flask-caching redis
```

---

## 1. What is Caching?

Imagine you are a Chef. Every time a customer asks for a salad, you have to go to the garden, pick the vegetables, wash them, and chop them. This is slow!

**Caching** is like having a bowl of pre-chopped salad ready in the fridge. When someone asks, you just hand it over. It is much faster!

## 2. Why use Redis?

In MAD 1, everything lived in the SQL database (the "Garden").
In **MAD 2**, we use **Redis**. Redis is an "In-Memory" database. It stores data in RAM, not on a slow hard drive. It is perfect for storing "pre-chopped" API results.

---

## 3. Implementing Caching in Flask

We typically use the `Flask-Caching` library.

### Basic Setup
```python
from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': 'redis://localhost:6379/1'})
cache.init_app(app)
```

### Caching and clearing data

You can also cache a value manually, read it later, and clear it when the data changes.

```python
# Save something in cache
cache.set('task_count', 25, timeout=60)

# Read it back
count = cache.get('task_count')

# Clear one cached value or clear everything
cache.delete('task_count')
cache.clear()
```

### The Magic Decorator: `@cache.cached`
You can tell Flask to remember the result of an API call for a specific amount of time (e.g., 60 seconds).

```python
class TaskResource(Resource):
    @cache.cached(timeout=60)
    def get(self):
        # This code only runs ONCE every 60 seconds!
        # Everyone else gets the "pre-chopped" result from Redis.
        return Task.query.all()
```

When a task is created, updated, or deleted, clear the cached task list so the next request gets fresh data.

```python
class TaskResource(Resource):
    def post(self):
        # create task here
        cache.clear()
        return {"message": "Task created"}, 201

    def delete(self):
        # delete task here
        cache.clear()
        return {"message": "Task deleted"}, 200
```

---

## 4. When to NOT cache?

- **User Data**: Don't cache the profile page of User A and show it to User B!
- **Frequently Changing Data**: If a task list changes every second, a 60-second cache might be too long.

---

## Key Takeaways

1. **Redis**: The "Fridge" where we store pre-prepared data.
2. **Performance**: Caching reduces the load on your main database.
3. **Timeouts**: Always set an expiration time so data doesn't get "stale".

---

[Previous: Module 4](module4-jwt.html){: .btn } [Next: Module 6 - The Background Worker (Celery & Redis)](module6-celery.html){: .btn .btn-primary }
