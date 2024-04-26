import os
import logging
from flask_bcrypt import Bcrypt
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.environment import db_URI
from config.environment import secret
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)


@app.before_request
def log_request_info():
    app.logger.debug('Headers: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

# Example route to test the basic setup
@app.route('/')
def hello():
    print(f"Access the Hello World endpoint at: {request.url_root}")
    return "Hello World!"

@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def internal_server_error(e):
    return jsonify(error="Internal Server Error"), 500


app.config["SQLALCHEMY_DATABASE_URI"] = db_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret 
db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

from controllers.admin_controller import admin_bp
from controllers.auth_controller import auth_bp
from controllers.driver_controller import driver_bp
from controllers.passenger_controller import passenger_bp

app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(driver_bp, url_prefix='/api/driver')
app.register_blueprint(passenger_bp, url_prefix='/api/passenger')

if __name__ == "__main__":
    app.run(debug=True, port=8080, use_reloader=False)

