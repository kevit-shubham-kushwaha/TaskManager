import jwt
from flask_smorest import Blueprint
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
from bson import ObjectId
from bson.errors import InvalidId

from database.repository import flask_task_repository, flask_user_repository
from schema.users import UserSchema as USchema, UserLoginSchema
from auth.userAuth import token_required, check_admin
from libs.utils.config.config import (
    YOUR_SECRET_KEY
)
# from app import app

user_blp = Blueprint("users", __name__, description="Operations on users")

@user_blp.route("/users", methods=["GET", "POST"])
class UserRoutes(MethodView):
    
    @check_admin
    @token_required
    @user_blp.response(200, USchema(many=True))
    def get(self):
        user = flask_user_repository.find_many({})
        userList = []
        if not user:
            return jsonify({"message": "No users found"}), 404

        for u in user:
            u['_id'] = str(u['_id'])
            userList.append(u) 
        return jsonify(userList), 200

    @check_admin
    @token_required
    @user_blp.arguments(USchema)
    @user_blp.response(201, USchema)
    def post(self,data):
       
        if not data:
           return jsonify({"message": "No input data provided"}), 400
        try:
            
            if flask_user_repository.find_one({"email": data.get('email')}):
                return jsonify({"message": "User already exists"}), 400
            
            created_at = datetime.utcnow()
            data['created_at'] = created_at
            
            plain_password = data.get('password')
            hashed_password = generate_password_hash(plain_password)
            data['password'] = hashed_password
            
            user = flask_user_repository.insert_one(data)
            data['_id'] = str(user.inserted_id) 
            
            return jsonify(data), 201
        
        except Exception as e: 
            return jsonify({"message": str(e)}), 500



@user_blp.route("/users/<string:user_id>", methods=["PUT", "DELETE"])
class UserRoutesSpecific(MethodView):

    @check_admin
    @token_required
    @user_blp.response(200, USchema)
    @user_blp.arguments(USchema, location="json")
    def put(self, data, user_id):
        try:
            # print("User ID:", user_id)
            object_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({"message": "Invalid user ID format"}), 400

        result = flask_user_repository.update_one({"_id": object_id}, {"$set": data})

        if result.matched_count == 0:
            return jsonify({"message": "User not found"}), 404

        user = flask_user_repository.find_one({"_id": object_id})
        user['_id'] = str(user['_id'])
        return user, 200
    
    @check_admin
    @token_required
    def delete(self, user_id):
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({"message": "Invalid user ID format"}), 400

        result = flask_user_repository.delete_one({"_id": object_id})
        if result.deleted_count == 0:
            return jsonify({"message": "User not found"}), 404

        return jsonify({"message": "User deleted successfully"}), 200

@user_blp.route("/auth", methods=["POST"])
class UserAuthRoute(MethodView):

    @user_blp.arguments(UserLoginSchema, location="json")
    @user_blp.response(200, UserLoginSchema)
    def post(self,data):

        try:
            if request.method == 'POST':
                
                email = data.get('email')
                password = data.get('password')

                if not email or not password:
                    return jsonify({'message': 'email and password are required'}), 400

                user = flask_user_repository.find_one({'email': email})

                if not user:
                    return jsonify({'message': 'User not found'}), 404

                if not (user['password'] == password):
                    return jsonify({'message': 'Invalid password'}), 401
            
                token = jwt.encode({'public_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(minutes=30)}, YOUR_SECRET_KEY)
                
                flask_user_repository.update_one({'_id': user['_id']}, {'$set': {'token': token}})
                
                return jsonify({'token': token}), 200
        except Exception as e:
         
            return jsonify({"message": str(e)}), 500
            
           