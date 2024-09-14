import bcrypt
import jwt
import json
from flask import jsonify
from bson import json_util
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone

def create_response(status_code, message=None, errors=None, data=None, access_token=None):
    response = {
        "status": status_code
    }
    if message:
        response["message"] = message
    if errors:
        response["errors"] = errors
    if data:
        response["data"] = data
    if access_token:
        response["access_token"] = access_token
    return jsonify(response), status_code

def encode_auth_token(username, expiry_date, secret_key):
    payload = {
        "iat": datetime.now(timezone.utc),
        "exp": expiry_date,
        "sub": username,
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

def decode_auth_token(auth_token, secret_key):
    try:
        payload = jwt.decode(auth_token, secret_key, algorithms=["HS256"])
        return payload  
    except ExpiredSignatureError:
        return create_response(401, errors="Token has expired.")
    except InvalidTokenError:
        return create_response(401, errors="Invalid token!")
    
def bson_to_json(data):
    return json.loads(json_util.dumps(data))

def hash_password(password: str) -> str:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode(), salt)
    return hashed.decode()
