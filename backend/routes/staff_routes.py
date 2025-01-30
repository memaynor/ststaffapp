from flask import Blueprint, request, jsonify
from datetime import datetime

staff_bp = Blueprint("staff_bp", __name__)

# Lazy import inside the function to avoid circular import
def get_db():
    from backend.models import db  # ✅ Import inside function
    return db

# Lazy import for Staff model
def get_staff_model():
    from backend.models.staff import Staff  # ✅ Import inside function
    return Staff

# Create a staff member
@staff_bp.route("/", methods=["POST"])
def add_staff():
    Staff = get_staff_model()  # Lazy import
    db = get_db()

    data = request.json
    if "name" not in data or "username" not in data:
        return jsonify({"message": "Name and username are required"}), 400
    
    existing_user = Staff.query.filter_by(username=data["username"]).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_staff = Staff(name=data["name"], username=data["username"], notes=data.get("notes", ""))
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"message": "Staff added", "staff": data}), 201

# Get all staff members
@staff_bp.route("/", methods=["GET"])
def get_staff():
    Staff = get_staff_model()
    db = get_db()

    staff_list = Staff.query.all()
    result = [
        {"id": s.id, "name": s.name, "username": s.username, "notes": s.notes, "last_login": s.last_login, "total_time_online": s.total_time_online}
        for s in staff_list
    ]
    return jsonify(result)

# Log a staff login
@staff_bp.route("/login/<string:username>", methods=["POST"])
def log_login(username):
    Staff = get_staff_model()
    db = get_db()

    staff = Staff.query.filter_by(username=username).first()
    if staff:
        staff.last_login = datetime.utcnow()
        db.session.commit()
        return jsonify({"message": f"{staff.name} ({staff.username}) logged in", "last_login": staff.last_login}), 200
    return jsonify({"message": "Staff not found"}), 404

# Delete a staff profile
@staff_bp.route("/<int:staff_id>", methods=["DELETE"])
def delete_staff(staff_id):
    Staff = get_staff_model()
    db = get_db()

    staff = Staff.query.get(staff_id)
    if staff:
        db.session.delete(staff)
        db.session.commit()
        return jsonify({"message": "Staff deleted"}), 200
    return jsonify({"message": "Staff not found"}), 404

# Get staff by username
@staff_bp.route("/username/<string:username>", methods=["GET"])
def get_staff_by_username(username):
    Staff = get_staff_model()

    staff = Staff.query.filter_by(username=username).first()
    if staff:
        result = {
            "id": staff.id,
            "name": staff.name,
            "username": staff.username,
            "notes": staff.notes,
            "last_login": staff.last_login,
            "total_time_online": staff.total_time_online,
        }
        return jsonify(result)
    return jsonify({"message": "Staff not found"}), 404

# Update staff profile
@staff_bp.route("/<int:staff_id>", methods=["PUT"])
def update_staff(staff_id):
    Staff = get_staff_model()
    db = get_db()

    staff = Staff.query.get(staff_id)
    if not staff:
        return jsonify({"message": "Staff not found"}), 404

    data = request.json
    if "username" in data:
        # Ensure new username isn't taken by another staff member
        existing_user = Staff.query.filter_by(username=data["username"]).first()
        if existing_user and existing_user.id != staff_id:
            return jsonify({"message": "Username already exists"}), 400

    staff.name = data.get("name", staff.name)
    staff.username = data.get("username", staff.username)
    staff.notes = data.get("notes", staff.notes)

    db.session.commit()
    return jsonify({"message": "Staff updated"}), 200
