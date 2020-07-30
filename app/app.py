from flask import Flask
from flask_restx import Resource, Api, fields
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask import make_response, jsonify, request

app = Flask(__name__)
api = Api(app)

# set db URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://passnflyuser:password@localhost:3306/passnfly'

# init db
db = SQLAlchemy(app)

# Passenger SQLAlchemy model
class Passenger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    last_name = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    destination = db.Column(db.String(100))

    def __init__(self, name, last_name, email, destination):
        self.name = name
        self.last_name = last_name
        self.email = email
        serf.destination = destination

# Passenger API model
passenger = api.model('Passenger', {
    'id': fields.Integer(readOnly=True, description='The passenger unique identifier'),
    'name': fields.String(required=True, description='The passenger name'),
    'last_name': fields.String(required=True, description='The passenger last name'),
    'email': fields.String(required=True, description='The passenger email address'),
    'destination': fields.String(required=True, description='The passenger destination')
    }

@api.route('/passenger')
class PassengerApi(Resource):
    @api.marshal_with(passenger)
    @api.route('/passenger/<int:id>/')
    def get_passenger(self, id):
        passenger = Passenger.query.filter_by(id=id).first()
        if passenger is None:
            return {}
        return make_response(jsonify(passenger), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(passenger, code=200)
    @api.route('/passenger/create/', methods=['POST'])
    def create_passenger(self):

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

    @api.marshal_with(passenger, code=200)
    @api.route('/passenger/update/<int:id>/', methods=['POST'])
    def update_passenger(self, id):
        data = request.json
        passenger = Passenger.query.get(id)
        passenger.name = data['name'],
        passenger.last_name = data['last_name'],
        passenger.email = data['last_name'],
        passenger.city = data['city']

        # updates new data
        db.session.commit()

        return make_response(jsonify(passenger), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(passenger, code=200)
    @api.route('/passenger/delete/<int:id>/', methods=['DELETE'])
    def delete_passenger(self, id):
        db.session.delete(Passenger.query.get(id))
        db.session.commit()
        return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
