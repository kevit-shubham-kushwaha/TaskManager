from functools import wraps
import jwt
from flask import request, jsonify
from src.app import app
from src.database import db


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('jwt_token')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = db.user_db.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated