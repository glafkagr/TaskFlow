from flask import jsonify
from flask.views import MethodView
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from flask_smorest import Blueprint

from app.extensions import db
from app.extensions import db, limiter
from app.models.user import User
from app.api.schemas import UserRegisterSchema, UserLoginSchema, UserResponseSchema

auth_blp = Blueprint('auth', __name__, url_prefix='/auth')  # ΜΟΝΟ /auth

@auth_blp.route('/register')
class Register(MethodView):
    @limiter.limit("5 per minute")
    @auth_blp.arguments(UserRegisterSchema)
    @auth_blp.response(201, UserResponseSchema)
    def post(self, user_data):
        if User.query.filter_by(email=user_data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        if User.query.filter_by(username=user_data['username']).first():
            return jsonify({'error': 'Username already taken'}), 409

        user = User(
            username=user_data['username'],
            email=user_data['email'],
            password_hash=generate_password_hash(user_data['password'])
        )

        db.session.add(user)
        db.session.commit()

        return user, 201

@auth_blp.route('/login')
class Login(MethodView):
    @limiter.limit("5 per minute")
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200)
    def post(self, login_data):
        user = User.query.filter_by(email=login_data['email']).first()

        if not user or not check_password_hash(user.password_hash, login_data['password']):
            return jsonify({'error': 'Invalid email or password'}), 401

        access_token = create_access_token(identity=str(user.id))

        return {
            'access_token': access_token,
            'user_id': user.id,
            'username': user.username
        }, 200
