from src.app import app
from src.routes.userRoutes import user_blp
from src.routes.taskRoutes import task_blp
from dotenv import load_dotenv
import os


@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(user_blp)
app.register_blueprint(task_blp)

load_dotenv()  # Load environment variables from a .env file
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Retrieve the secret key from the .env file
print("Secret Key:", app.config['SECRET_KEY'])  # Print the secret key for debugging purposes


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)