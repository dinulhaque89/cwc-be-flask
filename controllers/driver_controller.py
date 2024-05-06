from flask import Blueprint, request, jsonify, g
from models.booking import Booking
from models.review import Review
from models.driver import Driver
from serializers.driver_schema import DriverSchema
from serializers.booking_schema import BookingSchema
from serializers.review_schema import ReviewSchema
from middleware.secure_route import secure_route
from flask_jwt_extended import get_jwt_identity
from app import db

driver_bp = Blueprint('driver', __name__)

@driver_bp.route('/assigned-rides', methods=['GET'])
@secure_route(required_roles=['driver'])
def view_assigned_rides():
    user_id = get_jwt_identity()
    # Fetch the driver entry based on the user_id
    driver = Driver.query.filter_by(user_id=user_id).first()
    if not driver:
        return jsonify({"message": "Driver not found."}), 404

    assigned_rides = Booking.query.filter(Booking.driver_id == driver.driver_id).all()
    if not assigned_rides:
        return jsonify({"message": "No assigned rides found."}), 200
    else:
        return jsonify({"message": f"You have {len(assigned_rides)} assigned ride(s).", "assigned_rides": BookingSchema(many=True).dump(assigned_rides)}), 200

@driver_bp.route('/available-rides', methods=['GET'])
@secure_route(required_roles=['driver'])
def view_available_rides():
    available_rides = Booking.query.filter(Booking.driver_id.is_(None), Booking.status.is_(None)).all()
    return jsonify(BookingSchema(many=True).dump(available_rides)), 200

@driver_bp.route('/accept-ride/<int:booking_id>', methods=['POST'])
@secure_route(required_roles=['driver'])
def accept_ride(booking_id):
    try:
        user_id = get_jwt_identity()
        driver = Driver.query.filter_by(user_id=user_id).first()
        if not driver:
            return jsonify({"msg": "Driver not found"}), 404

        booking = Booking.query.filter(Booking.booking_id == booking_id, Booking.driver_id.is_(None), Booking.status.is_(None)).first_or_404()
        booking.driver_id = driver.driver_id  
        booking.status = 'assigned'
        db.session.commit()
        return jsonify({"msg": "Ride accepted", "booking": BookingSchema().dump(booking)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400

@driver_bp.route('/update-status/<int:booking_id>', methods=['POST'])
@secure_route(required_roles=['driver'])
def update_status(booking_id):
    try:
        # Define allowed statuses
        allowed_statuses = [
            'on route to passenger pickup location',
            'picked up passenger',
            'on route to passengers destination location',
            'completed'
        ]

        # Get the status from the request
        status = request.json.get('status', '')

        # Validate the status
        if status not in allowed_statuses:
            return jsonify({"msg": "Invalid status update"}), 400

        # Fetch the driver based on the JWT identity (user_id)
        user_id = get_jwt_identity()
        driver = Driver.query.filter_by(user_id=user_id).first()
        if not driver:
            return jsonify({"msg": "Driver not found"}), 404

        # Ensure the booking belongs to the driver and update the status
        booking = Booking.query.filter_by(booking_id=booking_id, driver_id=driver.driver_id).first_or_404()
        booking.status = status
        db.session.commit()

        return jsonify({"msg": "Status updated", "booking": BookingSchema().dump(booking)}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": str(e)}), 400
    

@driver_bp.route('/feedback', methods=['GET'])
@secure_route(required_roles=['driver'])
def view_feedback():
    try:
        user_id = get_jwt_identity()
        driver = Driver.query.filter_by(user_id=user_id).first()
        if not driver:
            return jsonify({"msg": "Driver not found"}), 404
        
        feedbacks = Review.query.filter(Review.driver_id == driver.driver_id).all()
        return jsonify(ReviewSchema(many=True).dump(feedbacks)), 200
    except Exception as e:
        # Log the error for debugging purposes
        print(f"Error fetching feedback: {e}")
        return jsonify({"msg": "Failed to fetch feedback"}), 500
    

@driver_bp.route('/details', methods=['GET'])
@secure_route(required_roles=['driver'])
def get_driver_details():
    try:
        user_id = get_jwt_identity()
        driver = Driver.query.filter_by(user_id=user_id).first()

        if not driver:
            return jsonify({"msg": "Driver not found"}), 404

        driver_schema = DriverSchema()
        return jsonify(driver_schema.dump(driver)), 200

    except Exception as e:
        return jsonify({"msg": str(e)}), 500