from flask import request, jsonify, g
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError, CSRFError
from jwt.exceptions import PyJWTError
from http import HTTPStatus
from functools import wraps
from models.user import User

# def secure_route(required_roles=None):
#     if required_roles is None:
#         required_roles = []




#     def wrapper(func):
#         @wraps(func)
#         def decorated_function(*args, **kwargs):
#             try:
#                 verify_jwt_in_request()
#                 current_user_id = get_jwt_identity()
#                 current_user = User.query.get(current_user_id)

#                 if current_user is None:
#                     return jsonify({"msg": "User not found."}), HTTPStatus.NOT_FOUND

#                 g.current_user = current_user

#                 if required_roles and current_user.role.lower() not in (role.lower() for role in required_roles):
#                     return jsonify({"msg": "You do not have permission to access this resource."}), HTTPStatus.FORBIDDEN

#             except (NoAuthorizationError, CSRFError, PyJWTError) as e:
#                 return jsonify({"msg": "Unauthorized: " + str(e)}), HTTPStatus.UNAUTHORIZED
#             except Exception as e:
#                 return jsonify({"msg": "Unauthorized: " + str(e)}), HTTPStatus.UNAUTHORIZED

#             return func(*args, **kwargs)
#         return decorated_function
#     return wrapper



def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return user

def secure_route(required_roles=None):
    if required_roles is None:
        required_roles = []

    def wrapper(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user = get_current_user()

                if current_user is None:
                    return jsonify({"msg": "User not found."}), HTTPStatus.NOT_FOUND

                g.current_user = current_user

                if required_roles and current_user.role.lower() not in (role.lower() for role in required_roles):
                    return jsonify({"msg": "You do not have permission to access this resource."}), HTTPStatus.FORBIDDEN

            except (NoAuthorizationError, CSRFError, PyJWTError) as e:
                return jsonify({"msg": "Unauthorized: " + str(e)}), HTTPStatus.UNAUTHORIZED
            except Exception as e:
                return jsonify({"msg": "Unauthorized: " + str(e)}), HTTPStatus.UNAUTHORIZED

            return func(*args, **kwargs)
        return decorated_function
    return wrapper