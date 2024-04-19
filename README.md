# Canary Wharf Chauffeurs - Backend Documentation

Welcome to the backend documentation! This guide is designed to help beginners, tech recruiters, and engineers understand how to use and interact with the backend system I developed. Whether you're looking to integrate with our services, contribute to the project, or simply explore the technology stack I chose, this document will provide you with the necessary information to get started.

## Getting Started

To get started with the backend, you'll need to set up your development environment. This involves installing the required dependencies and setting up the database.

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation

1. Clone the repository to your local machine.
2. Navigate to the project directory and create a virtual environment:
   `venv`
3. Activate the virtual environment:
   - On Windows: `venv\Scripts\activate`
   - On macOS/Linux: `source venv/bin/activate`
4. Install the required dependencies:
   `txt`
5. Set up the database by running the provided initialization script:
   `py`
6. Start the backend server:
   `run`

## Technology Stack

The backend is built using a variety of technologies, each chosen for its reliability, performance, and ease of use. Below is an overview of the tech stack, complete with logos:

| Technology  | Use Case                        | Logo         |
|-------------|---------------------------------|--------------|
| Flask       | Web framework                   | !Flask       |
| SQLAlchemy  | ORM for database interactions   | !SQLAlchemy  |
| PostgreSQL  | Database                        | !PostgreSQL  |
| JWT         | Authentication and authorization| !JWT         |

Note: Logos are resized and aligned to ensure a professional appearance in the documentation.

## Project Structure

The backend project is structured as follows:

- `models/`: Contains the SQLAlchemy models that define the database schema.
- `controllers/`: Houses the Flask routes and controllers that handle API requests.
- `serializers/`: Includes Marshmallow schemas for serializing and deserializing model instances.
- `middleware/`: Middleware components, such as authentication and authorization checks.
- `seed.py`: A script for initializing the database with test data.

## Usage

The backend supports various endpoints for managing bookings, drivers, passengers, and reviews. Here's a brief overview:

- `/api/bookings`: Manage booking records.
- `/api/drivers`: Access driver information and manage driver-specific actions.
- `/api/passengers`: Passenger-related operations.
- `/api/reviews`: Submit and view feedback for rides.

For detailed API documentation, including available endpoints and request/response formats, please refer to the `api_documentation.md` file (if available) or the Postman collection included in the project repository.

## Contributing

While this project was developed by me alone, I welcome contributions from the community! If you're interested in contributing, please take a look at our `CONTRIBUTING.md` file for guidelines on how to submit pull requests, report issues, and suggest improvements.

## Support

If you encounter any issues or have questions about the backend, please file an issue on the GitHub repository, and I'll do my best to assist you.

Thank you for exploring my backend documentation. I hope this guide helps you understand the system and encourages you to dive deeper into the project!
