# Flask User Authentication App

* Flask is used for building the web application.
* SQLAlchemy is utilized for database interactions.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Usage](#usage)

## Features

- **User Registration**: Allows users to create an account with email and password.
- **User Login**: Provides session management for authenticated users.
- **Home Page**: A welcome page for logged-in users.
- **Logout Functionality**: Users can securely log out.

## Prerequisites

Ensure you have the following installed:

- [Python 3.8 or higher](https://www.python.org/downloads/)
- [MySQL](https://dev.mysql.com/downloads/)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Sur1010/Flask-login-and-registration.git
2. **Navigate to the project directory**:
   ```bash
    cd Flask-login-and-registration
3. **Create a virtual environment:**:
   ```bash
   python -m venv venv
4. **Activate the virtual environment**:
   - On Windows:
      ```bash
         .venv\Scripts\activate
   - On macOS and Linux:
      ```bash
         source venv/bin/activate
5. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
6. **Configure the database**:\
Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your database credentials:
    ```python
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/user_db'
7. **Initialize the database**:
    ```bash
    flask db init
    flask db migrate
    flask db upgrade

## Running the Application
1. **To run the application, execute**:
    ```bash
    python app.py
The application will run on `http://127.0.0.1:5000`.

## Usage
- Navigate to `/register` to create a new account.
- Use `/login` to access your account.
- After logging in, you'll be redirected to the home page.