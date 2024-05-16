"""
@File : test.py.py
@Author : mr
@Description : 
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import secrets

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mytest01:v57YzysJ0ajnngSQ@mysql.sqlpub.com/pygametest01'
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)  # 设置令牌过期时间为5分钟
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    createtime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updatetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


class UserList(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime.isoformat(),
            'updatetime': user.updatetime.isoformat()
        } for user in users])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', required=True, help="Phone cannot be blank!")
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        data = parser.parse_args()

        if User.query.filter_by(phone=data['phone']).first():
            return {'message': 'Phone number already exists'}, 400
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        user = User(phone=data['phone'], username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime.isoformat(),
            'updatetime': user.updatetime.isoformat()
        }

    @jwt_required()
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()

        if data['phone']:
            user.phone = data['phone']
        if data['username']:
            user.username = data['username']
        if data['password']:
            user.password = data['password']

        user.updatetime = datetime.now(timezone.utc)
        db.session.commit()
        return {'message': 'User updated successfully'}

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}


api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta, timezone
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
import secrets

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://mytest01:v57YzysJ0ajnngSQ@mysql.sqlpub.com/pygametest01'
app.config['JWT_SECRET_KEY'] = secrets.token_urlsafe(32)
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=5)  # 设置令牌过期时间为5分钟
db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    createtime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updatetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc),
                           onupdate=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f"<User {self.username}>"


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


class UserList(Resource):
    @jwt_required()
    def get(self):
        users = User.query.all()
        return jsonify([{
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime.isoformat(),
            'updatetime': user.updatetime.isoformat()
        } for user in users])

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('phone', required=True, help="Phone cannot be blank!")
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        data = parser.parse_args()

        if User.query.filter_by(phone=data['phone']).first():
            return {'message': 'Phone number already exists'}, 400
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        user = User(phone=data['phone'], username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()

        return {'message': 'User created successfully'}, 201


class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        return {
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime.isoformat(),
            'updatetime': user.updatetime.isoformat()
        }

    @jwt_required()
    def put(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        parser = reqparse.RequestParser()
        parser.add_argument('phone')
        parser.add_argument('username')
        parser.add_argument('password')
        data = parser.parse_args()

        if data['phone']:
            user.phone = data['phone']
        if data['username']:
            user.username = data['username']
        if data['password']:
            user.password = data['password']

        user.updatetime = datetime.now(timezone.utc)
        db.session.commit()
        return {'message': 'User updated successfully'}

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted'}


api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
