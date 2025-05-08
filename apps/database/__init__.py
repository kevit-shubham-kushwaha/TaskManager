from pymongo import MongoClient
from libs.utils.config import (
    MONGODB_URI
)


def connect_db(db_name:str):
  
    """
    Connect to the MongoDB database.
    """
    try:
        client = MongoClient(MONGODB_URI)
        db = client[db_name]
      
    except Exception as e:
        raise Exception(
            f"Failed to connect to the database: {e}"
            f"Error: {str(e)}"
        )
    return db
  
  

flask_db = connect_db("Tasks")

user_db = flask_db.Users
task_db = flask_db.Tasks