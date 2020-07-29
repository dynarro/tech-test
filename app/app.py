from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
api = Api(app)

# init db
db = SQLAlchemy(app)

# Passenger model
class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    last_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(100))

    def __init__(self, name, last_name, email, city):
        self.name = name
        self.last_name = last_name
        self.email = email
        serf.city = city


@api.route('/passanger')
class Passanger(Resource):
    def get(self):
        return {'hello': 'world'}

if __name__ == '__main__':
    app.run(debug=True)
