---
title: "Module 7: The Visual Report (CSV & Mail)"
layout: default
nav_order: 8
---

# Module 7: The Visual Report (CSV & Mail)

**Goal:** Automate regular reporting and communication using scheduled tasks and standard file formats.

---

## 1. Automated Reports (CSV)

In MAD 2, you are expected to provide "Exports". The simplest is **CSV** (Comma Separated Values).

### Generating a CSV in Flask
```python
import csv
from io import StringIO

def generate_report():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Task Title', 'Status', 'Created At'])
    
    tasks = Task.query.all()
    for t in tasks:
        writer.writerow([t.title, t.status, t.created_at])
    
    return output.getvalue()
```

---

## 2. Sending Emails

We use Python's built-in `smtplib` or higher-level libraries to send automated alerts.

```python
import smtplib
from email.message import EmailMessage

def send_mail(to, subject, content):
    msg = EmailMessage()
    msg.set_content(content)
    msg['Subject'] = subject
    msg['From'] = "admin@taskmaster.com"
    msg['To'] = to

    # Connect to a local SMTP server (like MailHog for testing)
    with smtplib.SMTP('localhost', 1025) as s:
        s.send_message(msg)
```

---

## 3. Scheduled Tasks (Celery Beat)

What if you want to send a report **every Monday at 8 AM**?
We use **Celery Beat**. It acts as a "Scheduler" that tells Celery when to run specific tasks.

### The Config
```python
celery.conf.beat_schedule = {
    'send-weekly-report': {
        'task': 'tasks.send_report',
        'schedule': crontab(day_of_week=1, hour=8, minute=0),
    },
}
```

---

## 4. User-Triggered Exports

Sometimes a user clicks a button: "**Export my Tasks to CSV**".
1. User clicks button.
2. Frontend sends request to API.
3. API starts a Celery task to generate the CSV.
4. Celery emails the CSV to the user when finished.

---

## Key Takeaways

1. **CSV**: The most compatible way to share data with Excel.
2. **SMTP**: The standard protocol for sending emails.
3. **Beat**: The scheduler that handles repetitive "maintenance" tasks.

---

[Previous: Module 6](module6-celery.html){: .btn } [Next: Module 8 - Final Polish (State Management)](module8-polish.html){: .btn .btn-primary }
