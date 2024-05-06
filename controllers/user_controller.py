from flask import Blueprint, jsonify
from middleware.secure_route import secure_route
from serializers.user_schema import UserSchema
from app import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/me', methods=['GET'])
@secure_route()
def get_current_user():
    user = g.current_user
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user)), 200