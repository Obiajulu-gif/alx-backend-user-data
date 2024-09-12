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
    Accepts email and password as form data and creates a new session
    if the login is valid, otherwise responds with 401.
    """
    # Get email and password from the request form
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate email and password
    if not AUTH.valid_login(email, password):
        # If invalid, return 401 Unauthorized
        abort(401)

    # Create a new session for the user
    session_id = AUTH.create_session(email)

    if session_id is None:
        # If session creation fails, return 401 Unauthorized
        abort(401)

    # Prepare the response with session_id in the cookie
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route('/sessions', methods=['DELETE'])
def logout():
    """
    Handles the DELETE /sessions route to log out a user.

    It retrieves the session_id from the request's cookies, finds associated
    user, destroys their session, and redirects to the home page.

    If the session_id is invalid, a 403 Forbidden response is returned.
    """
    # Get the session_id from the cookie
    session_id = request.cookies.get('session_id')

    if session_id is None:
        # If no session_id is found in cookies, return a 403 response
        abort(403)

    # Find the user associated with the session_id
    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        # If no user is found for this session_id, return a 403 response
        abort(403)

    # Destroy the session (logout the user)
    AUTH.destroy_session(user.id)

    # Redirect to the home page
    return redirect('/')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
