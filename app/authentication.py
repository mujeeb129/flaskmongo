from functools import wraps
from datetime import datetime, timedelta

import jwt

from flask import request, abort, jsonify
from app import app


def authenticate(view_function):
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        headers = request.headers

        if not headers.get("Authorization"):
            abort(400, description="Authorization header not found")
        try:
            token = headers.get("Authorization").split(" ")[1]
            user = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])['user']
        except Exception as e:
            return jsonify({"message": f"something went wrong: {str(e)}"}), 401
        return view_function(user,*args, **kwargs)

    return wrapper

def create_token(user):
    try:
        access_payload = {"user": user, "exp": datetime.utcnow() + timedelta(days=app.config["ACCESS_TOKEN_AGE"])}
        refresh_payload = {"exp": datetime.utcnow() + timedelta(days=app.config["REFRESH_TOKEN_AGE"])}
        
        access_token = jwt.encode(access_payload, app.config["SECRET_KEY"], algorithm="HS256")
        refresh_token = jwt.encode(refresh_payload, app.config["SECRET_KEY"], algorithm="HS256")
        return True, {"access": access_token, "refresh": refresh_token}
    except Exception as e:
        return False, str(e)
    
