# בס"ד - routes/auth_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user, error = AuthService.register_user(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "User registered successfully!"}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user, token = AuthService.login_user(data)
    if user:
        return jsonify({
            "token": token,
            "user": {
                "id": user.id,
                "user_name": user.user_name,
                "email": user.email,
                "role": user.role,
                "is_approved": user.is_approved_uploader,
                "has_requested": user.has_requested_upgrade
            }
        }), 200
    return jsonify({"error": "Invalid credentials"}), 401


@auth_bp.route('/user_status/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_status(user_id):
    user = AuthService.get_status(user_id)
    if user:
        return jsonify({
            "user_name": user.user_name,
            "is_approved": user.is_approved_uploader,
            "has_requested": user.has_requested_upgrade,
            "role": user.role
        }), 200
    return jsonify({"error": "Not found"}), 404


@auth_bp.route('/request_upgrade', methods=['POST'])
@jwt_required()
def request_upgrade():
    data = request.json
    if AuthService.request_upgrade(data.get('user_id')):
        return jsonify({"message": "Request sent"}), 200
    return jsonify({"error": "User not found"}), 404


# --- נתיבי מנהל (Admin) ---

@auth_bp.route('/admin/users', methods=['GET'])
@jwt_required()
def get_all_users():
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Admin access required"}), 403

    users = AuthService.get_all_users()
    return jsonify([{
        "id": u.id,
        "user_name": u.user_name,
        "email": u.email,
        "role": u.role,
        "is_approved": u.is_approved_uploader
    } for u in users])


@auth_bp.route('/admin/requests', methods=['GET'])
@jwt_required()
def get_upgrade_requests():
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Admin access required"}), 403
    users = AuthService.get_pending_upgrades()
    return jsonify([{"id": u.id, "user_name": u.user_name, "email": u.email} for u in users])


@auth_bp.route('/admin/approve_user/<int:user_id>', methods=['POST'])
@jwt_required()
def approve_user(user_id):
    claims = get_jwt()
    if claims.get("role") != "Admin":
        return jsonify({"error": "Admin access required"}), 403
    if AuthService.approve_user_upgrade(user_id):
        return jsonify({"message": "User approved"}), 200
    return jsonify({"error": "User not found"}), 404