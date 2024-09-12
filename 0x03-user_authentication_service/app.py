#!/usr/bin/env python3
"""
Basic Flask app
"""
from flask import Flask, jsonify, request, abort, make_response
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


@app.route('/sessions', methods=['POST'])
def login():
    """
    POST /sessions route for user login.
    Accepts email and password as form data and create a new session
    if the login is valid, otherwise responds with 401.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.valid_login(email, password):
        abort(401)

    session_id = auth.create_session(email)

    if session_id is None:
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
