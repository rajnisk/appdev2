"""
HTTP routes (no Blueprints): plain @app.route handlers.
"""
from functools import wraps

from flask import jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from models import db, User, Task
from extensions import cache
from celery_worker import email_admin_report_async


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        uid = get_jwt_identity()
        if uid is None:
            return jsonify({"msg": "unauthorized"}), 401
        user = User.query.get(int(uid))
        if not user or user.role != "admin":
            return jsonify({"msg": "admin only"}), 403
        return fn(*args, **kwargs)

    return wrapper


def register_routes(app):
    @app.route("/register", methods=["POST"])
    def register():
        data = request.get_json() or {}
        username = (data.get("username") or "").strip()
        password = data.get("password") or ""
        email = (data.get("email") or "").strip() or None
        if not username or not password:
            return jsonify({"msg": "username and password required"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "Username already taken"}), 409
        user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="employee",
            email=email,
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Account created"}), 201

    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json() or {}
        user = User.query.filter_by(username=(data.get("username") or "")).first()
        if not user or not check_password_hash(user.password_hash, data.get("password") or ""):
            return jsonify({"msg": "Invalid credentials"}), 401
        token = create_access_token(identity=str(user.id))
        return jsonify(
            {
                "msg": "ok",
                "token": token,
                "username": user.username,
                "role": user.role,
            }
        )

    @app.route("/tasks", methods=["GET"])
    @jwt_required()
    def list_tasks():
        uid = int(get_jwt_identity())
        rows = Task.query.filter_by(user_id=uid).order_by(Task.id.desc()).all()
        return jsonify([t.to_dict() for t in rows])

    @app.route("/tasks", methods=["POST"])
    @jwt_required()
    def create_task():
        uid = int(get_jwt_identity())
        data = request.get_json() or {}
        title = (data.get("title") or "").strip()
        if not title:
            return jsonify({"msg": "title required"}), 400
        t = Task(
            title=title,
            description=data.get("description") or "",
            status=data.get("status") or "Pending",
            priority=data.get("priority") or "Medium",
            user_id=uid,
        )
        db.session.add(t)
        db.session.commit()
        return jsonify(t.to_dict()), 201

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    @jwt_required()
    def update_task(task_id):
        uid = int(get_jwt_identity())
        t = Task.query.get_or_404(task_id)
        if t.user_id != uid:
            return jsonify({"msg": "forbidden"}), 403
        data = request.get_json() or {}
        if "title" in data:
            t.title = (data["title"] or "").strip() or t.title
        if "description" in data:
            t.description = data["description"] or ""
        if "status" in data:
            t.status = data["status"]
        if "priority" in data:
            t.priority = data["priority"]
        db.session.commit()
        return jsonify(t.to_dict())

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    @jwt_required()
    def delete_task(task_id):
        uid = int(get_jwt_identity())
        t = Task.query.get_or_404(task_id)
        if t.user_id != uid:
            return jsonify({"msg": "forbidden"}), 403
        db.session.delete(t)
        db.session.commit()
        return jsonify({"msg": "deleted"})

    @app.route("/admin/summary", methods=["GET"])
    @jwt_required()
    @admin_required
    @cache.cached(timeout=60, key_prefix="admin_summary")  # innermost: runs after auth
    def admin_summary():
        """Cached snapshot for admin dashboard (invalidate via /admin/cache-clear)."""
        total_tasks = Task.query.count()
        total_users = User.query.count()
        employees = User.query.filter_by(role="employee").count()
        admins = User.query.filter_by(role="admin").count()
        by_status = {}
        for status in ["Pending", "In Progress", "Completed"]:
            by_status[status] = Task.query.filter_by(status=status).count()
        return jsonify(
            {
                "total_tasks": total_tasks,
                "total_users": total_users,
                "employees": employees,
                "admins": admins,
                "tasks_by_status": by_status,
            }
        )

    @app.route("/admin/email-report", methods=["POST"])
    @jwt_required()
    @admin_required
    def admin_email_report():
        """Queue async Celery task — admin receives CSV report by email."""
        uid = int(get_jwt_identity())
        email_admin_report_async.delay(uid)
        return jsonify(
            {
                "msg": "Report is being generated and will be emailed to you shortly.",
            }
        )

    @app.route("/admin/cache-clear", methods=["POST"])
    @jwt_required()
    @admin_required
    def admin_cache_clear():
        cache.clear()
        return jsonify({"msg": "Cache cleared (e.g. admin summary will refresh)."})
