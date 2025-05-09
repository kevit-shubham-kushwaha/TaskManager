from libs.utils.logger import app_logger
from flask import Flask
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))


# from libs.utils.logger.app_logger import logging
from src.routes.users import user_blp
from src.routes.tasks import task_blp
from libs.utils.config import config


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(user_blp)
app.register_blueprint(task_blp)



if __name__ == '__main__':
    # logging.basicConfig(filename="flask_app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    app.run(debug=False, use_reloader=False)