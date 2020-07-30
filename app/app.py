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

# ticket SQLAlchemy model
class Ticket(db.Model):
    id = db.Column(db.SmallInteger, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    city = db.Column(db.String(100))
    country = db.Column(db.String(100))
    iata = db.Column(db.String(3)),
    icao = db.Column(db.String(4)),
    latitude = db.Column(db.Numeric, as_decimal=True),
    longitude = db.Column(db.Numeric, as_decimal=True),
    altitude = db.Column(db.Numeric, as_decimal=False),
    timezone = db.Column(db.String(100)),
    DST = db.Column(db.String(1)),
    type = db.Column(db.String(100)),
    source = db.Column(db.String(100))

    def __init__(self, name, city, country, iata, icao, latitude, longitude,
    altitude, timezone, DST, type, source):
        self.name = name
        self.city = city
        self.country = country
        self.iata = iata
        self.icao = icao
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.timezone = timezone
        self.DST = DST
        self.type = type
        self.source = source

# ticket API model
ticket = api.model('Ticket', {
    'id': fields.Integer(readOnly=True, description='The ticket unique identifier'),
    'name': fields.String(required=True, description='The ticket name'),
    'city': fields.String(required=True, description='The ticket city'),
    'country': fields.String(required=True, description='The ticket country'),
    'iata': fields.String(required=True, description='The ticket iata'),
    'icao': fields.String(required=True, description='The ticket icao'),
    'latitude': fields.Float(required=True, description='The ticket latitude'),
    'longitude': fields.Float(required=True, description='The ticket longitude'),
    'altitude': fields.Float(required=True, description='The ticket altitude'),
    'timezone': fields.String(required=True, description='The ticket timezone'),
    'DST': fields.String(required=True, description='The ticket DST'),
    'type': fields.String(required=True, description='The ticket type'),
    'source': fields.String(required=True, description='The ticket source')
    })

@api.route('/ticket')
class ticketApi(Resource):
    @api.marshal_with(ticket)
    @api.route('/ticket/<int:id>/')
    def get_ticket(self, id):
        ticket = Ticket.query.filter_by(id=id).first()
        if ticket is None:
            return {}
        return make_response(jsonify(ticket), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(ticket, code=200)
    @api.route('/ticket/create/', methods=['POST'])
    def create_ticket(self):

        data = request.json
        arg_pass = {
            'name': data['name'],
            'city': data['city'],
            'country': data['country'],
            'iata': data['iata'],
            'icao': data['icao'],
            'latitude': data['latitude'],
            'longitude': data['longitude'],
            'altitude': data['altitude'],
            'timezone': data['timezone'],
            'DST': data['DST'],
            'type': data['type'],
            'source': data['source'],
            }
        ticket = Ticket(**arg_pass)
        db.session.add(ticket)
        db.session.commit()
        print('ticketId', ticket.id)

        return make_response(jsonify(ticket), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(ticket, code=200)
    @api.route('/ticket/update/<int:id>/', methods=['POST'])
    def update_ticket(self, id):
        data = request.json
        ticket = Ticket.query.get(id)
        ticket.name = data['name'],
        ticket.city = data['city'],
        ticket.country = data['country'],
        ticket.iata = data['iata'],
        ticket.icao = data['icao'],
        ticket.latitude = data['latitude'],
        ticket.longitude = data['longitude'],
        ticket.altitude = data['altitude'],
        ticket.timezone = data['timezone'],
        ticket.DST = data['DST'],
        ticket.type = data['type'],
        ticket.source = data['source'],

        # updates new data
        db.session.commit()

        return make_response(jsonify(ticket), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(ticket, code=200)
    @api.route('/ticket/delete/<int:id>/', methods=['DELETE'])
    def delete_ticket(self, id):
        db.session.delete(Ticket.query.get(id))
        db.session.commit()
        return jsonify({'result': True})

    @api.marshal_with(ticket, code=200)
    @api.route('/ticket/upload/', methods=['POST'])
    def upload_ticket(self):
        import csv

        with open('passnfly.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                ticket = Ticket(**line)
                db.session.add(ticket)
                db.session.commit()
        return make_response(jsonify(ticket), 200)

if __name__ == '__main__':
    app.run(debug=True)
