from io import TextIOWrapper
import csv

from flask import Flask, request,redirect, url_for
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
    latitude = db.Column(db.Float),
    longitude = db.Column(db.Float),
    altitude = db.Column(db.Float),
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

@api.route('/ticket/<int:id>', methods=['GET, POST, DELETE'])
class ticketApi(Resource):
    @api.marshal_with(ticket)
    @api.doc('get_ticket')
    def get_ticket(self, id):
        ticket = Ticket.query.filter_by(id=id).first()
        if ticket is None:
            return {}
        return make_response(jsonify(ticket), 200, {"mimetype": "text/json", 'Content-Type': 'text/json'})

    @api.marshal_with(ticket, code=200)
    @api.doc('create_ticket')
    def create_ticket(self):

        data = request.json
        arg_pass = {
            'id': data['id'],
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
    @api.doc('update_ticket')
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
    @api.doc('delete_ticket')
    def delete_ticket(self, id):
        from sqlalchemy.exc import IntegrityError
        try:
            db.session.delete(Ticket.query.get(id))
            db.session.commit()
        except AssertionError as e:
            return {'status_code': 400, 'success': False, 'msg': str(e)}
        except IntegrityError as e:
            return {'status_code': 400, 'success': False, 'msg': str(e)}
        return jsonify({'success': True})

    @api.marshal_with(ticket, code=200)
    @api.doc('upload_ticket')
    def upload_ticket(self):
        import csv
        if request.method == 'POST':
            csv_file = request.files['file']
            csv_file = TextIOWrapper(csv_file, encoding='utf-8')
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                ticket = Ticket(
                id=row[0], name=row[1], city=row[2], country=row[3],
                iata=row[4], icao=row[5],latitude=row[6],longitude=row[7],
                altitude=row[8], timezone=row[9], DST=row[10], type=row[11],
                source=row[12]
                )
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('upload_csv'))

        return {'success': True}

        with open('passnfly.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for line in csv_reader:
                ticket = Ticket(**line)
                db.session.add(ticket)
                db.session.commit()
        return make_response(jsonify(ticket), 200)

if __name__ == '__main__':
    app.run(debug=True)
