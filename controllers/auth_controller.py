from flask import Blueprint, request, jsonify
from serializers.user_schema import UserSchema
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from models.user import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup/passenger', methods=['POST'])
def signup_passenger():
    return signup_user(role='passenger')

@auth_bp.route('/signup/driver', methods=['POST'])
def signup_driver():
    return signup_user(role='driver')

def signup_user(role):
    data = request.get_json()
    data['role'] = role  # Assign role based on the endpoint

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"message": "Email already in use."}), 409

    user_schema = UserSchema()

    try:
        user = user_schema.load(data, session=db.session)
        user.set_password(data['password'])  # Hash the password before saving
        db.session.add(user)
        db.session.commit()
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.verify_password(data['password']):
        access_token = create_access_token(identity=user.user_id, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401