API Documentation
Welcome to our API documentation. This guide provides detailed information on how to interact with our backend services, including endpoints, request/response formats, and authentication methods. This documentation is intended for developers, tech enthusiasts, and anyone interested in integrating with our services.

Base URL
All API requests are made to the base URL of our backend service. Replace localhost with your deployed service's domain if applicable.


Copy code
http://localhost:4000/api
Authentication
Our API uses JWT (JSON Web Tokens) for authentication. To make authenticated requests, you must include an Authorization header with the token obtained during login.


Copy code
Authorization: Bearer <your_token_here>
Endpoints Overview
Bookings
List Bookings: GET /bookings
Create Booking: POST /bookings
Update Booking Status: PUT /bookings/{booking_id}
Drivers
View Assigned Rides: GET /driver/assigned-rides
View Available Rides: GET /driver/available-rides
Update Ride Status: PUT /driver/update-status/{booking_id}
View Feedback: GET /driver/feedback
Passengers
Create Review: POST /passenger/reviews
Get Bookings: GET /passenger/bookings
Admin
View Feedback: GET /admin/feedback
List Bookings: GET /admin/bookings
Amend Booking: PUT /admin/bookings/{booking_id}
Generate Reports: GET /admin/reports
Example Requests
Create Booking (Passenger)

Copy code
POST /api/passenger/bookings
Content-Type: application/json
Authorization: Bearer <your_token_here>

{
  "start_location": "Downtown",
  "end_location": "Airport",
  "booking_date": "2023-01-01",
  "start_time": "10:00:00"
}
View Assigned Rides (Driver)

Copy code
GET /api/driver/assigned-rides
Authorization: Bearer <your_token_here>
Submit Review (Passenger)

Copy code
POST /api/passenger/reviews
Content-Type: application/json
Authorization: Bearer <your_token_here>

{
  "booking_id": 1,
  "rating": 5,
  "comments": "Excellent service!"
}
Error Handling
Our API uses conventional HTTP response codes to indicate success or failure of an API request. Here are some common responses:

200 OK - The request was successful.
400 Bad Request - The request was malformed or invalid.
401 Unauthorized - Authentication failed or token expired.
404 Not Found - The requested resource was not found.
500 Internal Server Error - We had a problem with our server. Try again later.
For errors, the API responds with a JSON object containing the error message:

json


Copy code
{
  "msg": "Error message"
}
Conclusion
This API documentation should provide you with all the necessary information to start integrating with our backend services. If you have any further questions or encounter any issues, please don't hesitate to contact us.
