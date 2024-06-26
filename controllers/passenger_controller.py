from flask import Blueprint, request, jsonify, g
from models.booking import Booking
from models.review import Review
from models.user import User
from models.driver import Driver
from serializers.driver_schema import DriverSchema
from serializers.booking_schema import BookingSchema
from serializers.review_schema import ReviewSchema
from serializers.user_schema import UserSchema
from middleware.secure_route import secure_route
from flask_jwt_extended import get_jwt_identity
from app import db
from datetime import date, datetime, timedelta


passenger_bp = Blueprint('passenger', __name__)

@passenger_bp.route('/details', methods=['GET'])
@secure_route(required_roles=['passenger'])
def get_passenger_details():
    try:
        passenger_id = get_jwt_identity()
        passenger = User.query.filter_by(user_id=passenger_id).first()

        if not passenger:
            return jsonify({"msg": "Passenger not found"}), 404

        user_schema = UserSchema()
        return jsonify(user_schema.dump(passenger)), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500
    


@passenger_bp.route('/bookings', methods=['POST'])
@secure_route(required_roles=['passenger'])
def create_booking():
    try:
        data = request.get_json()
        data['passenger_id'] = get_jwt_identity()

        # Validate booking_date and start_time
        booking_date = datetime.strptime(data['booking_date'], '%Y-%m-%d').date()
        start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        current_datetime = datetime.now()

        if booking_date < current_datetime.date():
            return jsonify({"msg": "Booking date must be today or in the future"}), 400
        
        if booking_date == current_datetime.date() and start_time < current_datetime.time():
            return jsonify({"msg": "Start time must be in the future"}), 400


        booking = BookingSchema().load(data, session=db.session)
        db.session.add(booking)
        db.session.commit()
        
        return BookingSchema().dump(booking), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400

@passenger_bp.route('/bookings', methods=['GET'])
@secure_route(required_roles=['passenger'])
def get_bookings():
    booking_type = request.args.get('type', 'all')
    status_filter = request.args.get('status')  
    passenger_id = get_jwt_identity()
    today = date.today()

    try:
        query = Booking.query.filter_by(passenger_id=passenger_id)

        if status_filter in ['completed', 'cancelled']:
            query = query.filter(Booking.status == status_filter)

        if booking_type == 'past':
            bookings = query.filter(Booking.booking_date < today).all()
        elif booking_type == 'upcoming':
            bookings = query.filter(Booking.booking_date >= today, Booking.status != 'cancelled').all()
        else:
            bookings = query.all()

        message = "No bookings found." if not bookings else f"Found {len(bookings)} booking(s)."
        return jsonify({"message": message, "bookings": BookingSchema(many=True).dump(bookings)}), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@passenger_bp.route('/bookings/<int:booking_id>', methods=['GET'])
@secure_route(required_roles=['passenger'])
def get_booking(booking_id):
    try:
        booking = Booking.query.filter_by(booking_id=booking_id, passenger_id=get_jwt_identity()).first_or_404()
        return jsonify(BookingSchema().dump(booking)), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@passenger_bp.route('/bookings/<int:booking_id>', methods=['DELETE'])
@secure_route(required_roles=['passenger'])
def cancel_booking(booking_id):
    try:
        booking = Booking.query.filter_by(booking_id=booking_id, passenger_id=get_jwt_identity()).first_or_404()
        start_time_str = booking.start_time.strftime("%H:%M:%S")
        start_datetime = datetime.combine(booking.booking_date, datetime.strptime(start_time_str, "%H:%M:%S").time())
        if datetime.now() + timedelta(hours=1) < start_datetime:
            booking.status = 'cancelled'
            db.session.commit()
            return jsonify({"msg": "Booking canceled"}), 200
        else:
            return jsonify({"msg": "Cancellation not allowed less than one hour before start time"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 500

@passenger_bp.route('/reviews', methods=['POST'])
@secure_route(required_roles=['passenger'])
def create_review():
    try:
        data = request.get_json()
        booking_id = data.get('booking_id')
        passenger_id = get_jwt_identity()
        booking = Booking.query.filter_by(booking_id=booking_id, passenger_id=passenger_id, status='completed').first()
        
        if not booking:
            return jsonify({"msg": "Review can only be made on completed bookings by the passenger."}), 400
        
        current_time = datetime.now()
        booking_end_time = datetime.combine(booking.booking_date, booking.end_time)
        
        if current_time <= booking_end_time:
            return jsonify({"msg": "Review can only be made after the booking end time."}), 400
        
        data['passenger_id'] = passenger_id
        review = ReviewSchema().load(data, session=db.session)
        db.session.add(review)
        db.session.commit()
        return ReviewSchema().dump(review), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400

@passenger_bp.route('/details', methods=['PUT'])
@secure_route(required_roles=['passenger'])
def update_passenger_details():
    passenger_id = get_jwt_identity()
    data = request.get_json()
    passenger = User.query.filter_by(user_id=passenger_id).first()
    if not passenger:
        return jsonify({"msg": "Passenger not found"}), 404
    passenger.name = data.get('name', passenger.name)
    passenger.email = data.get('email', passenger.email)
    passenger.mobile_phone = data.get('mobile_phone', passenger.mobile_phone)
    db.session.commit()
    return jsonify({"msg": "Details updated successfully"}), 200

@passenger_bp.route('/change-password', methods=['POST'])
@secure_route(required_roles=['passenger'])
def change_password():
    data = request.get_json()

    current_password = data.get('currentPassword')
    new_password = data.get('newPassword')

    if not current_password or not new_password:
        return jsonify({"msg": "Both current and new passwords are required."}), 400

    passenger_id = get_jwt_identity()
    passenger = User.query.filter_by(user_id=passenger_id).first()

    if not passenger:
        return jsonify({"msg": "Passenger not found"}), 404

    try:
        if not passenger.verify_password(current_password):
            return jsonify({"msg": "Current password is incorrect"}), 400

        # Check new password strength (example check, implement according to your policy)
        if len(new_password) < 8:
            return jsonify({"msg": "New password must be at least 8 characters long."}), 400

        passenger.set_password(new_password)
        db.session.commit()

        return jsonify({"msg": "Password changed successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Failed to change password due to an internal error"}), 500

@passenger_bp.route('/reviews', methods=['GET'])
@secure_route(required_roles=['passenger'])
def get_reviews():
    passenger_id = get_jwt_identity()
    try:
        reviews = db.session.query(Review, Driver, User).\
            join(Driver, Review.driver_id == Driver.driver_id).\
            join(User, Driver.user_id == User.user_id).\
            filter(Review.passenger_id == passenger_id).\
            all()

        reviews_data = [{
            "driver_name": user.name,
            "rating": review.rating,
            "comments": review.comments
        } for review, driver, user in reviews]

        return jsonify(reviews_data), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500

@passenger_bp.route('/bookings/<int:booking_id>/end-time', methods=['PUT'])
@secure_route(required_roles=['admin', 'driver'])
def update_booking_end_time(booking_id):
    try:
        data = request.get_json()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()

        booking = Booking.query.get_or_404(booking_id)
        booking.end_time = end_time
        db.session.commit()

        return jsonify({"msg": "Booking end time updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400