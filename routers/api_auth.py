from flask import Blueprint, request
from common.utils import create_response
from middlewares.auth_middleware import authenticate

# Create a Blueprint for authentication routes
api_auth = Blueprint('api_auth', __name__)

# POST route for login
@api_auth.route('/login', methods=['POST'])
def login():
    # Extract username and password from the request
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    # Return error if either field is missing
    if username is None or password is None:
        return create_response(400, errors="Username and Password are required.")
    
    return authenticate(username=username, password=password)
