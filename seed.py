from app import app, db
from models.user import User
from models.driver import Driver
from models.vehicle import Vehicle
from models.booking import Booking
from models.review import Review
import random
from datetime import datetime, timedelta

def create_admins():
    admins = [
        User(email='admin1@example.com', password_hash='admin123', role='admin', name='Admin One', mobile_phone='+1234567890'),
        User(email='admin2@example.com', password_hash='admin234', role='admin', name='Admin Two', mobile_phone='+1234567891')
    ]
    db.session.add_all(admins)
    db.session.commit()
    print("Admins created successfully.")

def create_users_and_drivers():
    users = [
        User(email='passenger1@example.com', password_hash='pass123', role='passenger', name='Passenger One', mobile_phone='+1234567891'),
        User(email='passenger2@example.com', password_hash='pass123', role='passenger', name='Passenger Two', mobile_phone='+1234567892'),
        User(email='driver1@example.com', password_hash='drive123', role='driver', name='Driver One', mobile_phone='+1234567893'),
        User(email='driver2@example.com', password_hash='drive123', role='driver', name='Driver Two', mobile_phone='+1234567894'),
    ]
    db.session.add_all(users)
    db.session.commit()
    print("Users and Drivers created successfully.")

    driver_users = User.query.filter(User.role == 'driver').all()
    driver_entries = [Driver(user_id=user.user_id, license_number=f'DRIV123{index}') for index, user in enumerate(driver_users, start=4)]
    db.session.add_all(driver_entries)
    db.session.commit()
    print("Driver entries created successfully.")

    vehicles = [
        Vehicle(driver_id=driver_entries[0].driver_id, make='Tesla', model='Model X', year=2020, license_plate='TESLA1', is_active=True),
        Vehicle(driver_id=driver_entries[1].driver_id, make='Honda', model='Accord', year=2019, license_plate='HONDA1', is_active=True),
    ]
    db.session.add_all(vehicles)
    db.session.commit()
    print("Vehicles created successfully.")

    return users, driver_entries

def create_bookings(users, driver_entries):
    today = datetime.now()
    past_date = today - timedelta(days=30)
    future_date = today + timedelta(days=30)

    passenger_users = [user for user in users if user.role == 'passenger']
    bookings = []
    for i in range(7):
        bookings.append(Booking(
            passenger_id=passenger_users[0].user_id,
            driver_id=driver_entries[0].driver_id,
            start_location=f'{100 + i} Main St',
            end_location=f'{200 + i} Oak St',
            booking_date=past_date - timedelta(days=i),
            start_time=(past_date - timedelta(days=i)).time(),
            end_time=(past_date - timedelta(days=i, hours=1)).time(),
            status='completed',
            fare=random.uniform(20.0, 100.0)
        ))
    for i in range(5):
        bookings.append(Booking(
            passenger_id=passenger_users[1].user_id,
            driver_id=driver_entries[1].driver_id if i % 2 == 0 else None,
            start_location=f'{300 + i} Pine St',
            end_location=f'{400 + i} Elm St',
            booking_date=future_date + timedelta(days=i),
            start_time=(future_date + timedelta(days=i)).time(),
            status='scheduled' if i % 2 == 0 else 'pending',
            fare=random.uniform(25.0, 120.0)
        ))
    db.session.add_all(bookings)
    db.session.commit()
    print(f"{len(bookings)} bookings created successfully.")

def create_reviews():
    past_bookings = Booking.query.filter(Booking.status == 'completed').all()
    reviews = [
        Review(
            booking_id=booking.booking_id,
            passenger_id=booking.passenger_id,
            driver_id=booking.driver_id,
            rating=random.randint(1, 5),
            comments=random.choice([
                'Excellent service!', 
                'Good, but room for improvement.', 
                'Not satisfied with the ride.', 
                'Great driver, very polite.', 
                'Will ride again!'
            ])
        ) for booking in past_bookings
    ]
    db.session.add_all(reviews)
    db.session.commit()
    print(f"{len(reviews)} reviews created successfully.")

with app.app_context():
    try:
        db.drop_all()
        db.create_all()
        create_admins()
        users, driver_entries = create_users_and_drivers()
        create_bookings(users, driver_entries)
        create_reviews()
        print("Database seeded successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"An error occurred: {e}")