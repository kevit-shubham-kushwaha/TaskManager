import jwt
from functools import wraps
from flask import request, jsonify
from database.repository import flask_user_repository
from bson import ObjectId
from flask import g

# from app import app

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # your custom header
        
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            secret = "your_secret_key"  # Replace with your actual secret key
            data = jwt.decode(token, secret, algorithms=["HS256"])
            public_id = data['public_id']
            try:
                object_id = ObjectId(public_id)  
            except Exception as e:
                return jsonify({'message': 'Invalid public_id format'}), 400

            current_user = flask_user_repository.find_one({"_id": object_id})  
            
            if not current_user:
                return jsonify({'message': "user not found"}), 404
            g.current_user = current_user
        except Exception as e:
            return jsonify({'message': str(e)}), 401

        return f(*args, **kwargs)

    return decorated
#adding some data
def check_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Your custom header
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401
        
        try:
            secret = 'your_secret_key'  # Replace with your actual secret key
            jwt_decoded_data = jwt.decode(token, secret, algorithms=["HS256"])
            public_id = jwt_decoded_data.get('public_id')
            
            if not public_id:
                return jsonify({'message': 'Public ID not found in token'}), 400
            
            try:
                object_id = ObjectId(public_id)
            except Exception as e:
                return jsonify({'message': 'Invalid public_id format'}), 400

            current_user = flask_user_repository.find_one({"_id": object_id})  
            
            if not current_user:
                return jsonify({'message': "User not found"}), 404
            
            if current_user.get('user_role') != 'admin':
                return jsonify({'message': "Admin access required"}), 403

            g.current_user = current_user

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401
        except Exception as e:
            return jsonify({'message': f'An error occurred: {str(e)}'}), 500
        
        return f(*args, **kwargs)

    return decorated
