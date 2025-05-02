from src.app import app
from src.routes.userRoutes import user_blp
from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response

from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid
from datetime import datetime, timezone, timedelta
from functools import wraps


@app.route('/')
def hello_world():
    return 'Hello, World!'

app.register_blueprint(user_blp)

app.config['secret_key'] = 'your_secret_key'  # Change this to a random secret key


if __name__ == '__main__':
    app.run(debug=False, use_reloader=False)