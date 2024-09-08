#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from api.v1.auth.basic_auth import BasicAuth
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

auth = None

auth_type = getenv("AUTH_TYPE", 'auth')
if auth_type == 'auth':
    auth = Auth()

if auth_type == 'basic_auth':
    auth = BasicAuth()
elif auth_type == 'session_auth':
    auth = Auth()
else:
    auth = Auth()


@app.before_request
def before_request() -> None:
    """Executed before each request."""
    excluded_paths = ['/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/']

    if auth:
        # Check if the request requires authentication
        if not auth.require_auth(request.path, excluded_paths):
            return

        # If no authorization header and no session cookie, abort with 401
        if auth.authorization_header(
                request) is None and auth.session_cookie(request) is None:
            abort(401)

        # Set the current user from the request
        request.current_user = auth.current_user(request)


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def before_request() -> None:
    """ Before request handler
    """
    if auth is None:
        return None
    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/']
    if not auth.require_auth(request.path, excluded_paths):
        return None
    if not auth.authorization_header(request):
        abort(401)
    if not auth.current_user(request):
        abort(403)


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
