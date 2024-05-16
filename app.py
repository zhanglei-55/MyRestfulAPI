"""
@File : app.py@Author : mr
@Description : 1.Flask 框架的一个特性 : 会自动创建应用上下文 不需要自己创建 => with app.app_context():  # 创建应用上下文
2.Flask 框架的一个特性 : 默认使用的交互格式 Content-Type 是 text/html
@Time : 2024
"""
from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
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
    createtime = db.Column(db.DateTime, default=datetime.now)
    updatetime = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        """
        返回对象的字符串表示形式，以便于在调试和其他开发环境中清晰地识别和显示。

        参数:
        self: 表示对象自身的引用。

        返回值:
        str: 返回一个字符串，该字符串以"<User {username}>"的格式表示用户对象，其中{username}是用户的用户名。
        """
        return f"<User {self.username}>"


@app.route('/login', methods=['POST'])
def login():
    """
    处理用户登录请求的函数。

    接收JSON格式的用户名和密码，验证用户后返回访问令牌。

    参数:
    - 无

    返回值:
    - 如果请求中缺少JSON、用户名或密码，则返回400错误和相关消息。
    - 如果用户名或密码不正确，则返回401错误和相关消息。
    - 如果验证成功，则返回200状态码和包含访问令牌的JSON。
    """

    # 检查请求是否为JSON格式
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    # 从请求的JSON中获取用户名和密码
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    # 检查用户名和密码是否为空
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400

    # 验证用户名和密码
    user = User.query.filter_by(username=username).first()
    if not user or user.password != password:
        # 逻辑与 同假才假一真即真
        # user 1/2 密码必须为1/2的 否则都为证
        # 示例 user admin zabbix | password 000000 111111
        return jsonify({"msg": "Bad username or password"}), 401

    # 创建访问令牌
    access_token = create_access_token(identity=username)
    # 返回访问令牌
    return jsonify(access_token=access_token), 200


class UserList(Resource):
    @jwt_required()  # 要求用户登录后才能访问
    def get(self):
        """
        获取所有用户的信息列表

        参数:
        无

        返回值:
        jsonify对象: 包含所有用户信息的JSON列表，每个用户信息包括id、phone、username、createtime和updatetime
        """
        users = User.query.all()  # 从数据库查询所有用户信息
        return jsonify([{
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime,
            'updatetime': user.updatetime
        } for user in users])  # 将用户信息列表转换为JSON格式并返回

    def post(self):
        """
        创建新用户。

        该接口接收电话号码、用户名和密码作为请求参数，并验证这些参数的完整性。如果电话号码已存在于数据库中，
        则返回错误信息；否则，创建新用户并返回成功的消息。

        参数:
        - 无

        返回值:
        - 当电话号码已存在时，返回包含错误信息的字典和HTTP状态码400；
        - 当成功创建用户时，返回包含成功消息的字典和HTTP状态码201。
        """

        # 初始化请求参数解析器
        parser = reqparse.RequestParser()
        # 添加必要的请求参数及其验证规则
        parser.add_argument('phone', required=True, help="Phone cannot be blank!")
        parser.add_argument('username', required=True, help="Username cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        # 解析请求参数
        data = parser.parse_args()

        # 检查电话号码是否已存在
        if User.query.filter_by(phone=data['phone']).first():
            return {'message': 'Phone number already exists'}, 400
        # 检查用户名是否已存在
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        # 创建新用户并提交到数据库
        user = User(phone=data['phone'], username=data['username'], password=data['password'])
        db.session.add(user)
        db.session.commit()

        # 返回创建成功的消息
        return {'message': 'User created successfully'}, 201


class UserResource(Resource):
    @jwt_required()  # 要求用户登录后才能访问
    def get(self, user_id):
        """
        根据用户ID获取用户信息

        参数:
        - user_id: int, 需要查询的用户的ID

        返回值:
        - user_info: dict, 包含用户ID、电话、用户名、创建时间和更新时间的信息字典；
                      如果用户不存在，则返回错误信息和404状态码。
        """
        # 尝试根据用户ID查询用户信息
        user = User.query.get(user_id)
        if not user:
            # 如果用户不存在，返回错误信息
            return {'message': 'User not found'}, 404

        # 如果用户存在，返回用户信息
        return {
            'id': user.id,
            'phone': user.phone,
            'username': user.username,
            'createtime': user.createtime.isoformat(),  # 用户的创建时间，格式化为字符串
            'updatetime': user.updatetime.isoformat()  # 用户信息的更新时间，格式化为字符串
        }

    @jwt_required()
    def put(self, user_id):
        """
        更新用户信息。

        该接口使用JWT认证，允许通过用户ID更新用户的电话、用户名和密码。

        参数:
        - user_id: 要更新的用户的ID。

        返回值:
        - 当用户不存在时，返回404状态码和一个包含错误信息的字典。
        - 当用户存在且更新成功时，返回200状态码和一个包含成功信息的字典。
        """
        # 尝试根据user_id查询用户
        user = User.query.get(user_id)
        if not user:
            # 如果用户不存在，返回404错误
            return {'message': 'User not found'}, 404

        # 初始化请求解析器，用于解析客户端发送的更新数据
        parser = reqparse.RequestParser()
        parser.add_argument('phone')  # 添加电话参数
        parser.add_argument('username')  # 添加用户名参数
        parser.add_argument('password')  # 添加密码参数
        data = parser.parse_args()  # 解析客户端发送的更新信息

        # 根据接收到的数据更新用户字段
        if data['phone']:
            user.phone = data['phone']
        if data['username']:
            user.username = data['username']
        if data['password']:
            user.password = data['password']

        # 更新用户信息的时间
        user.updatetime = datetime.now()
        db.session.commit()  # 提交数据库事务，保存更新
        return {'message': 'User updated successfully'}

    @jwt_required()  # 要求用户登录后才能执行删除操作
    def delete(self, user_id):
        """
        删除指定的用户
        参数:
            user_id: 要删除的用户的ID
        返回值:
            当用户不存在时，返回一个包含错误信息的字典和HTTP状态码404；
            当用户成功删除时，返回一个包含成功信息的字典。
        """
        # 尝试根据用户ID查询用户
        user = User.query.get(user_id)
        if not user:
            # 如果用户不存在，返回错误信息
            return {'message': 'User not found'}, 404

        # 从数据库会话中删除用户，并提交改动
        db.session.delete(user)
        db.session.commit()
        # 返回删除成功的信息
        return {'message': 'User deleted'}


api.add_resource(UserList, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
"""
代码优化建议：
这里有几个优化和改进建议，可以进一步提高代码的效率和安全性，并确保遵循最佳实践：

优化和改进建议
安全性增强：尽管你目前不需要密码哈希加密，但在生产环境中，确保密码的安全性非常重要。你应该尽可能地使用哈希算法来存储密码，比如使用 werkzeug.security 的 generate_password_hash 和 check_password_hash。

代码结构和可读性：将一些常见的逻辑抽取为单独的函数或方法，可以提高代码的可读性和可维护性。

错误处理和日志记录：在关键操作中添加错误处理和日志记录，可以帮助你更好地跟踪和排查问题。

时间处理：确保所有时间戳使用时区感知的 datetime 对象。
"""