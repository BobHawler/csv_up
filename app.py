from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
auth = HTTPBasicAuth()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(256))

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f'Username: {self.username}'


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    return True


@app.route('/registration', methods=['POST'])
def registration():
    username = request.json.get('username')
    password = request.json.get('password')

    if username is None or password is None:
        return jsonify({'message': 'Enter username and password'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'This username is already exists'}), 400

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)


@app.route('/upload', methods=['POST'])
@auth.login_required
def upload():
    file = request.files['file']
    filename = file.filename
    file.save(filename)
    return jsonify({'message': 'File successfully uploaded'})


@app.route('/files', methods=['GET'])
@auth.login_required
def get_files():
    files = []
    for filename in os.listdir():
        if filename.endswith('.csv'):
            file_info = {'filename': filename}
            df = pd.read_csv(filename)
            file_info['columns'] = list(df.columns)
            files.append(file_info)
    return jsonify(files)


@app.route('/data', methods=['GET'])
@auth.login_required
def get_data():
    filename = request.args.get('filename')
    filter_col = request.args.get('filter_col')
    filter_val = request.args.get('filter_val')
    sort_cols = request.args.get('sort_cols')

    df = pd.read_csv(filename)
    if filter_col and filter_val:
        df = df[df[filter_col] == filter_val]
    if sort_cols:
        df = df.sort_values(sort_cols)

    return jsonify(df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(debug=True)
