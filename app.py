from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/about', methods=['POST'])
def about():
    return {"info": "This is the about page"}


@app.route('/user/login', methods=['POST'])
def Login1():
    username = request.form['username']
    password = request.form['password']
    print(username, password)
    return {"info": "登录成功"}


if __name__ == '__main__':
    app.run()


