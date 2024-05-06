# controllers/admin_controller.py
from flask import Blueprint, jsonify, request
from models.user import User
from models.booking import Booking
from models.driver import Driver
from middleware.secure_route import secure_route
from serializers.driver_schema import DriverSchema
from app import db
from sqlalchemy import func
from models.review import Review
from serializers.user_schema import UserSchema
from serializers.booking_schema import BookingSchema
from serializers.driver_schema import DriverSchema
from flask_jwt_extended import get_jwt_identity



admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/drivers', methods=['GET'])
@secure_route(required_roles=['admin'])
def list_drivers():
    drivers = Driver.query.all()
    driver_schema = DriverSchema(many=True)
    return driver_schema.dump(drivers), 200

@admin_bp.route('/drivers', methods=['POST'])
@secure_route(required_roles=['admin'])
def add_driver():
    data = request.get_json()
    driver_schema = DriverSchema(session=db.session) 
    try:
        driver = driver_schema.load(data)
        db.session.add(driver)
        db.session.commit()
        return driver_schema.dump(driver), 201
    except Exception as e:
        db.session.rollback()  
        return jsonify({'msg': str(e)}), 400

@admin_bp.route('/drivers/<int:driver_id>', methods=['PUT'])
@secure_route(required_roles=['admin'])
def update_driver(driver_id):
    try:
        driver = Driver.query.get(driver_id)
        if not driver:
            return jsonify({'msg': 'Driver not found'}), 404
        
        data = request.get_json()
        for key, value in data.items():
            setattr(driver, key, value)
        db.session.commit()
        return jsonify({'msg': 'Driver updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400

@admin_bp.route('/drivers/<int:driver_id>', methods=['DELETE'])
@secure_route(required_roles=['admin'])
def remove_driver(driver_id):
    try:
        driver = Driver.query.get(driver_id)
        if not driver:
            return jsonify({'msg': 'Driver not found'}), 404
        
        db.session.delete(driver)
        db.session.commit()
        return jsonify({'msg': 'Driver removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400

@admin_bp.route('/reports', methods=['GET'])
@secure_route(required_roles=['admin'])
def generate_reports():
    try:
        # Total Bookings
        total_bookings = db.session.query(func.count(Booking.booking_id)).scalar()

        # Total Revenue
        total_revenue = db.session.query(func.sum(Booking.fare)).scalar()

        # Driver Performance Metrics (example: average rating per driver)
        driver_performance = db.session.query(
            Driver.driver_id,
            User.name,
            func.avg(Review.rating).label('average_rating')
        ).select_from(Driver) \
        .join(User, Driver.user_id == User.user_id) \
        .outerjoin(Review, Review.driver_id == Driver.driver_id) \
        .group_by(Driver.driver_id, User.name).all()

        # Common Routes
        common_routes = db.session.query(
            Booking.start_location,
            Booking.end_location,
            func.count(Booking.booking_id).label('route_count')
        ).group_by(Booking.start_location, Booking.end_location) \
         .order_by(func.count(Booking.booking_id).desc()).limit(5).all()

        report_data = {
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue) if total_revenue else 0,
            'driver_performance': [{'driver_id': dp[0], 'name': dp[1], 'average_rating': float(dp[2]) if dp[2] else None} for dp in driver_performance],
            'common_routes': [{'start_location': cr[0], 'end_location': cr[1], 'route_count': cr[2]} for cr in common_routes]
        }

        return jsonify(report_data), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@admin_bp.route('/feedback', methods=['GET'])
@secure_route(required_roles=['admin'])
def view_feedback():
    try:
        feedbacks = db.session.query(
            Review.review_id,
            Review.comments,
            Review.rating,
            User.name.label('passenger_name'),
            Driver.driver_id
        ).join(Booking, Booking.booking_id == Review.booking_id)\
         .join(User, User.user_id == Booking.passenger_id)\
         .join(Driver, Driver.driver_id == Review.driver_id).all()

        feedback_data = [{
            'review_id': f.review_id,
            'comments': f.comments,
            'rating': f.rating,
            'passenger_name': f.passenger_name,
            'driver_id': f.driver_id
        } for f in feedbacks]

        return jsonify(feedback_data), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500

@admin_bp.route('/bookings', methods=['GET'])
@secure_route(required_roles=['admin'])
def list_bookings():
    try:
        bookings = Booking.query.all()
        return jsonify(BookingSchema(many=True).dump(bookings)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500
    

@admin_bp.route('/bookings/<int:booking_id>', methods=['PUT'])
@secure_route(required_roles=['admin'])
def amend_booking(booking_id):
    try:
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'msg': 'Booking not found'}), 404
        
        data = request.get_json()
        for key, value in data.items():
            if hasattr(booking, key):
                setattr(booking, key, value)
        db.session.commit()
        return jsonify({'msg': 'Booking updated successfully', 'booking': BookingSchema().dump(booking)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400

@admin_bp.route('/bookings', methods=['POST'])
@secure_route(required_roles=['admin'])
def add_booking():
    data = request.get_json()
    booking_schema = BookingSchema(session=db.session)
    try:
        booking = booking_schema.load(data)
        db.session.add(booking)
        db.session.commit()
        return jsonify(booking_schema.dump(booking)), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400
    

@admin_bp.route('/passengers', methods=['GET'])
@secure_route(required_roles=['admin'])
def list_all_passengers():
    try:
        passengers = User.query.filter_by(role='passenger').all()
        return jsonify(UserSchema(many=True).dump(passengers)), 200
    except Exception as e:
        return jsonify({'msg': str(e)}), 500
    


@admin_bp.route('/passengers/<int:user_id>', methods=['PUT'])
@secure_route(required_roles=['admin'])
def update_passenger(user_id):
    try:
        passenger = User.query.get(user_id)
        if not passenger or passenger.role != 'passenger':
            return jsonify({'msg': 'Passenger not found'}), 404
        
        data = request.get_json()
        for key, value in data.items():
            if hasattr(passenger, key):
                setattr(passenger, key, value)
        db.session.commit()
        return jsonify({'msg': 'Passenger updated successfully', 'passenger': UserSchema().dump(passenger)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400


@admin_bp.route('/passengers', methods=['POST'])
@secure_route(required_roles=['admin'])
def add_passenger():
    data = request.get_json()
    user_schema = UserSchema(session=db.session)
    try:
        user = user_schema.load(data)
        db.session.add(user)
        db.session.commit()
        return jsonify(user_schema.dump(user)), 201
    except Exception as e:
        db.session.rollback()  
        return jsonify({'msg': str(e)}), 400

@admin_bp.route('/passengers/<int:user_id>', methods=['DELETE'])
@secure_route(required_roles=['admin'])
def remove_passenger(user_id):
    try:
        passenger = User.query.get(user_id)
        if not passenger:
            return jsonify({'msg': 'Passenger not found'}), 404
        
        db.session.delete(passenger)
        db.session.commit()
        return jsonify({'msg': 'Passenger removed successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'msg': str(e)}), 400
    

@admin_bp.route('/details', methods=['GET'])
@secure_route(required_roles=['admin'])
def get_admin_details():
    try:
        user_id = get_jwt_identity()
        admin = User.query.filter_by(user_id=user_id, role='admin').first()

        if not admin:
            return jsonify({"msg": "Admin not found"}), 404

        user_schema = UserSchema()
        return jsonify(user_schema.dump(admin)), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500