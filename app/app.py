from app.utils import dumps
from flask import Flask
from flask_restx import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import make_response, jsonify, request

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


@api.route('/passenger')
class PassengerApi(Resource):
    def get_passenger(id):
        passenger = Passenger.query.filter_by(id=id).first()
        if passenger is None:
            return {}
        return make_response(jsonify(passenger), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    def create_passenger(self, id):

        data = request.json
        arg_pass = {
            'name': data['name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'city': data['city']
            }
            passenger = Passenger(**arg_pass)
            db.session.add(passenger)
            db.session.commit()
            print('passengerId', passanger.id)


        return make_response(jsonify(passenger), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

if __name__ == '__main__':
    app.run(debug=True)
