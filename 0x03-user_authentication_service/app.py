#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request
from auth import Auth


app = Flask(__name__)

AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome():
    """
    Return a JSON payload with a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user():
    """
    POST /users route to register a new user
    Expects form data: 'email' and 'password'
    """
    # Get the form data for email and password
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        # Register the user with the provided email and password
        user = AUTH.register_user(email, password)
        # Return success message if user is created
        return jsonify({"email": user.email, "message": "user created"}), 200
    except ValueError:
        # Return error message if email is already registered
        return jsonify({"message": "email already registered"}), 400


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
