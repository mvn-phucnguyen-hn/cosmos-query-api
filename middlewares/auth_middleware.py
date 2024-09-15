import os
import bcrypt
from functools import wraps
from datetime import datetime, timezone, timedelta
from flask import request
import logging

from common.utils import create_response, encode_auth_token, decode_auth_token, hash_password

# Set up basic configuration for logging
logging.basicConfig(level=logging.INFO)

secret_key = os.getenv('SECRET_KEY')
username_env = os.getenv('USERNAME_ENV')
password_env = os.getenv('PASSWORD_ENV')
# Ensure expiry_days is an integer
expiry_days = int(os.getenv('EXPIRY_DAYS_DEFAULT', 1))  

def verify_token():
    token = None
    if "Authorization" in request.headers and "Bearer " in request.headers["Authorization"]:
        token = request.headers["Authorization"].split(" ")[1]
    
    if not token:
        return create_response(401, errors="Missing Authorization token!")
    
    payload_token = decode_auth_token(token, secret_key)
    # Check if an error response is returned
    if isinstance(payload_token, tuple):
        return payload_token
    
    if payload_token.get("sub") != username_env:
        return create_response(400, errors="User not found.")
    
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Call the verify_token function
        response = verify_token()
        if isinstance(response, tuple):  # Check if the response is an error response
            return response
        
        # If token is valid, proceed to the actual function
        return f(*args, **kwargs)
    
    return decorated_function

def authenticate(username, password):
    try:
        logging.info("password param: %s", password)
        logging.info("password env: %s", password_env)
        logging.info("Hash password: %s", hash_password(password))
        if username != username_env:
            return create_response(400, errors="User not found.")
        
        if not bcrypt.checkpw(password.encode(), password_env.encode()):
            return create_response(401, errors="The password is incorrect.")
        
        expiry_date = datetime.now(timezone.utc) + timedelta(days=expiry_days)
        access_token = encode_auth_token(username, expiry_date, secret_key)

        return create_response(200, message="Authentication successful", access_token=access_token)
    except ValueError:
        return create_response(400, errors="Invalid bcrypt hash format. Please check password again.")
    except Exception as e:
        return create_response(500, errors=f"An unexpected error occurred: {str(e)}")
