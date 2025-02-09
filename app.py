from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend to connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Change to MySQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)

@app.route('/data', methods=['GET'])
def get_data():
    data = Data.query.all()
    return jsonify([{ 'id': d.id, 'name': d.name, 'value': d.value } for d in data])

@app.route('/data', methods=['POST'])
def add_data():
    new_data = Data(name=request.json['name'], value=request.json['value'])
    db.session.add(new_data)
    db.session.commit()
    return jsonify({ 'message': 'Data added!' })

@app.route('/data/<int:id>', methods=['PUT'])
def update_data(id):
    data = Data.query.get(id)
    if not data:
        return jsonify({'message': 'Data not found'}), 404
    data.name = request.json['name']
    data.value = request.json['value']
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

import os

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)

