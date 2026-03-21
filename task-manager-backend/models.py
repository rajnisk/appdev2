"""Model: database schema (SQLAlchemy)."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    # "admin" | "employee" — only seeded admin or future tooling should set admin
    role = db.Column(db.String(20), nullable=False, default="employee")
    # Used for Flask-Mail reminders; optional for older rows
    email = db.Column(db.String(120), nullable=True)

    tasks = db.relationship("Task", backref="owner", lazy=True, cascade="all, delete-orphan")


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
        }
