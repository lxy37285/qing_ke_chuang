import os

from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, logout_user, login_user
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 数据库配置(设置数据库 和关闭数据库事务)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.root_path, 'sqlite3.db')

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'this is a secret key'
# 数据库app
db = SQLAlchemy()
db.init_app(app)
# 登录app
login_manager = LoginManager(app)


# 如果数据库不存在，就创建数据库


class User(db.Model, UserMixin):
    """
    继承自 UserMixin 和 db.Model
    UserMixin 提供了默认的用户属性和方法
    db.Model 是 SQLAlchemy 的基类，用于定义数据库模型
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()


def getUser(username):
    try:
        return User.query.filter_by(username=username).first()
    except Exception as e:
        return None


@app.route('/', methods=['GET'])
def hello_world():
    return render_template('index.html')


@app.route('/about', methods=['POST'])
def about():
    return {"info": "This is the about page"}


@app.route('/user/login', methods=['POST'])
def Login1():
    username = request.form['username']
    password = request.form['password']
    user:User = getUser(username)
    print(user.username, user.password,user.id)
    if user and user.password == password:
        login_user(user)
        return {"info": "登录成功"}
    else:
        return {"info": "用户名或密码错误"}


@app.route('/user/register', methods=['POST'])
def Register():
    username = request.form['username']
    password = request.form['password']
    new_user = User()
    new_user.username = username
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()
    return {"info": "注册成功"}


@app.route('/user/logout', methods=['POST'])
def Logout():
    logout_user()
    return {"info": "登出成功"}


if __name__ == '__main__':
    app.run()
