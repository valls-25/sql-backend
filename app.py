import pymysql
pymysql.install_as_MySQLdb()

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pegSZTZmPyrpZMwgsObjBwTBxEWgoIFY@mysql.railway.internal:3306/railway'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

# Routes
@app.route('/data', methods=['GET'])
def get_data():
    data = Data.query.all()
    return jsonify([{ 'id': d.id, 'name': d.name, 'value': d.value} for d in data])

@app.route('/data', methods=['POST'])
def add_data():
    data = request.get_json(force=True)  # Force parse JSON
    if not data or 'name' not in data or 'value' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    new_data = Data(name=data['name'], value=data['value'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data added!'}), 201

@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = Data.query.get(id)
    if not data:
        return jsonify({'message': 'Data not found'}), 404
    
    data.name = request.json.get('name', data.name)
    data.value = request.json.get('value', data.value)
    
    db.session.commit()
    return jsonify({'message': 'Data updated'})

@app.route('/data/<int:id>', methods=['DELETE'])
def delete_data(id):
    data = Data.query.get(id)
    if not data:
        return jsonify({'message': 'Data not found'}), 404
    
    db.session.delete(data)
    db.session.commit()
    return jsonify({'message': 'Data deleted'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000)
