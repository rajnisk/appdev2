"""
Celery app + scheduled tasks (daily employee reminders, monthly admin report)
and on-demand admin report email.
"""
import os
from io import StringIO
import csv

from celery import Celery
from celery.schedules import crontab
from flask_mail import Message

from extensions import mail

celery = Celery(__name__)


def _flask_app_context():
    """Late import so app module is fully initialized (worker / beat)."""
    import app as app_module

    return app_module.app.app_context()


def init_celery(app):
    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config.get("CELERY_RESULT_BACKEND", app.config["CELERY_BROKER_URL"]),
        timezone=app.config.get("CELERY_TIMEZONE", "UTC"),
        beat_schedule={
            "daily-employee-reminder": {
                "task": "celery_worker.daily_employee_reminder",
                "schedule": crontab(
                    hour=int(os.getenv("DAILY_REMINDER_HOUR", "9")),
                    minute=int(os.getenv("DAILY_REMINDER_MINUTE", "0")),
                ),
            },
            "monthly-admin-report": {
                "task": "celery_worker.monthly_admin_report",
                "schedule": crontab(
                    day_of_month=int(os.getenv("MONTHLY_REPORT_DAY", "1")),
                    hour=int(os.getenv("MONTHLY_REPORT_HOUR", "8")),
                    minute=int(os.getenv("MONTHLY_REPORT_MINUTE", "0")),
                ),
            },
        },
    )
    app.extensions["celery"] = celery
    return celery


def _build_report_csv():
    """Return (csv_string, summary_dict) for all tasks."""
    from models import Task, User, db

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["task_id", "title", "status", "priority", "user_id", "username"])
    rows = (
        db.session.query(Task, User.username)
        .join(User, Task.user_id == User.id)
        .order_by(Task.id)
        .all()
    )
    for task, username in rows:
        writer.writerow(
            [task.id, task.title, task.status, task.priority, task.user_id, username]
        )
    total = Task.query.count()
    by_status = {}
    for s in ["Pending", "In Progress", "Completed"]:
        by_status[s] = Task.query.filter_by(status=s).count()
    summary = {
        "total_tasks": total,
        "by_status": by_status,
        "total_users": User.query.count(),
    }
    return output.getvalue(), summary


@celery.task(name="celery_worker.daily_employee_reminder")
def daily_employee_reminder():
    """Email each employee (with an email on file) a short pending-task reminder."""
    with _flask_app_context():
        from models import User, Task

        employees = User.query.filter_by(role="employee").all()
        notified = 0
        for u in employees:
            if not u.email:
                continue
            pending = (
                Task.query.filter_by(user_id=u.id)
                .filter(Task.status != "Completed")
                .count()
            )
            body = (
                f"Hi {u.username},\n\n"
                f"You have {pending} task(s) not marked Completed.\n"
                f"Please check the Task Manager app.\n"
            )
            msg = Message(
                subject="Daily task reminder",
                recipients=[u.email],
                body=body,
            )
            mail.send(msg)
            notified += 1
        return {"employees_notified": notified}


@celery.task(name="celery_worker.monthly_admin_report")
def monthly_admin_report():
    """Scheduled: email all admins a CSV report + short summary."""
    with _flask_app_context():
        from models import User

        csv_text, summary = _build_report_csv()
        admins = User.query.filter_by(role="admin").all()
        admin_emails = [a.email for a in admins if a.email]
        if not admin_emails:
            return {"msg": "no admin emails configured"}

        body = (
            "Monthly Task Manager report\n\n"
            f"Total tasks: {summary['total_tasks']}\n"
            f"Users: {summary['total_users']}\n"
            f"By status: {summary['by_status']}\n\n"
            "See attached tasks.csv\n"
        )
        msg = Message(
            subject="Monthly task report (all users)",
            recipients=admin_emails,
            body=body,
        )
        msg.attach("tasks.csv", "text/csv", csv_text.encode("utf-8"))
        mail.send(msg)
        return {"admins": len(admin_emails)}


@celery.task(name="celery_worker.email_admin_report_async")
def email_admin_report_async(admin_id: int):
    """
    On-demand (admin button): email the requesting admin a CSV report.
    Runs asynchronously in a Celery worker.
    """
    with _flask_app_context():
        from models import User

        admin = User.query.get(admin_id)
        if not admin or admin.role != "admin" or not admin.email:
            return {"msg": "invalid admin or missing admin email"}

        csv_text, summary = _build_report_csv()
        body = (
            f"Hi {admin.username},\n\n"
            "Here is your requested Task Manager report.\n\n"
            f"Total tasks: {summary['total_tasks']}\n"
            f"Users: {summary['total_users']}\n"
            f"By status: {summary['by_status']}\n"
        )
        msg = Message(
            subject="Task Manager — admin report",
            recipients=[admin.email],
            body=body,
        )
        msg.attach("tasks.csv", "text/csv", csv_text.encode("utf-8"))
        mail.send(msg)
        return {"msg": "sent", "to": admin.email}
