import jwt
from flask import g
from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime, date

from schema.tasks import TaskSchema
from auth.userAuth import token_required, check_admin
from database.repository import flask_user_repository, flask_task_repository
from libs.utils.config import (
    YOUR_SECRET_KEY
)
# from app import app


task_blp = Blueprint("tasks", __name__, description="Operations on tasks")

@task_blp.route("/tasks", methods=["GET", "POST"])
class TaskRoutes(MethodView):

    @token_required
    @task_blp.response(200, TaskSchema(many=True))
    def get(self):
          tasks = flask_task_repository.find_many({})
          tasks_list = []
          if not tasks:
                return jsonify({"message": "No tasks found"}), 404
         
          for task in tasks:
                
                task['_id'] = str(task['_id'])
                tasks_list.append(task)
              
          return jsonify(tasks_list), 200    
      
    @token_required
    @check_admin  
    @task_blp.arguments(TaskSchema)
    @task_blp.response(201, TaskSchema)
    def post(self, data):
        try:
            # Token already validated by @token_required and user set in g
            current_user = g.current_user
            if not current_user:
                return jsonify({'message': 'Authentication failed'}), 401

            # Validate presence of task data
            if not data:
                return jsonify({"message": "No data provided"}), 400

            # Validate assigned_to (email must exist in user_db)
            assigned_email = data.get('assigned_to')
            if not assigned_email:
                return jsonify({"message": "assigned_to field is required"}), 400

            user_emails = flask_user_repository.distinct("email")
            if assigned_email not in user_emails:
                return jsonify({"message": "Please provide a valid user email to assign the task"}), 404
            
            
            if isinstance(data['due_date'], date):
                data['due_date'] = datetime.combine(data['due_date'], datetime.min.time())

            
            data['created_by'] = current_user['email']
            
            
            result = flask_task_repository.insert_one(data)
            flask_user_repository.update_one({"email": assigned_email}, {"$push": {"tasks": str(result.inserted_id)}})
            data['_id'] = str(result.inserted_id)

            return jsonify(data), 201

        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({"message": "Internal server error", "error": str(e)}), 500


@task_blp.route("/tasks/<string:task_id>", methods=["PUT", "DELETE"])
class TaskRoutesSpecific(MethodView):

    @task_blp.response(200, TaskSchema)
    @task_blp.arguments(TaskSchema)
    def put(self, data, task_id):
        try:
            object_id = ObjectId(task_id)
        except InvalidId:
            return jsonify({"message": "Invalid task ID"}), 400
        
        if not data:
            return jsonify({"message": "No input data provided"}), 400
        if isinstance(data.get('due_date'), date):
            data['due_date'] = datetime.combine(data['due_date'], datetime.min.time())
        try:
            flask_task_repository.update_one({"_id": object_id}, {"$set": data})
            
            task_result = flask_task_repository.find_one({"_id": object_id})
            task_result['_id'] = str(task_result['_id'])
            
            return jsonify(task_result), 200
        except Exception as e:
            return jsonify({"message": str(e)}), 500
          
    def delete(self, task_id):
        try:
            object_id = ObjectId(task_id)
            result = flask_task_repository.delete_one({"_id": object_id})
        
            if result.deleted_count == 0:
              return jsonify({"message": "Task not found"}), 404
        
        except Exception as e:
            return jsonify({"message": str(e)}), 400
        
        return jsonify({"message": "Task deleted successfully"}), 200

@task_blp.route("/mytask", methods=["GET"])
class UserTask(MethodView):
  
  @task_blp.response(200, TaskSchema(many=True))
  def get(self):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Please Log in to see your tasks!'}), 401
      
    try:
        data = jwt.decode(token, YOUR_SECRET_KEY, algorithms=["HS256"])
        public_id = data.get('public_id')
            
        if not public_id:
                return jsonify({'message': 'Public ID not found in token'}), 400
            
        try:
                object_id = ObjectId(public_id)
        except Exception as e:
                return jsonify({'message': 'Invalid public_id format'}), 400
        print("Object ID:", object_id)    
        current_user = flask_user_repository.find_one({"_id": object_id})   
        
        if not current_user:
            return jsonify({'message': 'User not found!'}), 404
        
        tasks = flask_task_repository.find_many({"assigned_to": current_user['email']})
        
        
        tasks_list = []
        for task in tasks:
            task['_id'] = str(task['_id'])
            tasks_list.append(task)
            
        return jsonify(tasks_list), 200 
    except Exception as e:
      return jsonify({'message': 'Internal server error', 'error': str(e)}), 500