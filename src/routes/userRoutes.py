from src.app import app
from flask_smorest import Blueprint, abort, Api
from flask import request, jsonify
from flask.views import MethodView
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import db
from src.schema.userSchema import UserSchema as USchema ,UserLoginSchema
import jwt
from datetime import datetime, timedelta, timezone

user_blp = Blueprint("users", __name__, description="Operations on users")



@user_blp.route("/users", methods=["GET", "POST"])
class UserRoutes(MethodView):

    @user_blp.response(200, USchema(many=True))
    def get(self):
        user = db.user_db.find({})
        userList = []
        if not user:
            return jsonify({"message": "No users found"}), 404

        for u in user:
            u['_id'] = str(u['_id'])
            userList.append(u) 
        return jsonify(userList), 200

    @user_blp.arguments(USchema)
    @user_blp.response(201, USchema)
    def post(self,data):
       
        if not data:
           return jsonify({"message": "No input data provided"}), 400
        try:
            plain_password = data.get('password')
            hashed_password = generate_password_hash(plain_password)
            data['password'] = hashed_password
            user = db.user_db.insert_one(data)
            data['_id'] = str(user.inserted_id) 
            return jsonify(data), 201
        except Exception as e:
            print("Error occurred while inserting user:", e)
            print(e)
            return jsonify({"message": str(e)}), 500

from bson import ObjectId
from bson.errors import InvalidId

@user_blp.route("/users/<string:user_id>", methods=["PUT", "DELETE"])
class UserRoutesSpecific(MethodView):

    @user_blp.response(200, USchema)
    @user_blp.arguments(USchema, location="json")
    def put(self, data, user_id):
        try:
            print("User ID:", user_id)
            object_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({"message": "Invalid user ID format"}), 400

        result = db.user_db.update_one({"_id": object_id}, {"$set": data})

        if result.matched_count == 0:
            return jsonify({"message": "User not found"}), 404

        user = db.user_db.find_one({"_id": object_id})
        user['_id'] = str(user['_id'])
        return user, 200

    def delete(self, user_id):
        try:
            object_id = ObjectId(user_id)
        except InvalidId:
            return jsonify({"message": "Invalid user ID format"}), 400

        result = db.user_db.delete_one({"_id": object_id})
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

                # print(password)
                if not email or not password:
                    return jsonify({'message': 'email and password are required'}), 400

                user = db.user_db.find_one({'email': email})

                if not user:
                    return jsonify({'message': 'User not found'}), 404

                # print(type(user['password']))
                # print(type(password))
                if not (user['password'] == password):
                    return jsonify({'message': 'Invalid password'}), 401
                

                token = jwt.encode({'public_id': str(user['_id']), 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['secret_key'])
                print("Token generated:", token)
                db.user_db.update_one({'_id': user['_id']}, {'$set': {'token': token}})
                return jsonify({'token': token}), 200
        except Exception as e:
            print("Error occurred during authentication:", e)
            return jsonify({"message": str(e)}), 500
            
           