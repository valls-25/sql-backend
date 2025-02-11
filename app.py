import pymysql
pymysql.install_as_MySQLdb()


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:fleabag20055@localhost/my_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from flask_migrate import Migrate
migrate = Migrate(app, db)


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    value = db.Column(db.String(100), nullable=False)
    value2 = db.Column(db.String(100), nullable=True)  # New optional field
    value3 = db.Column(db.String(100), nullable=True)  # New optional field


@app.route('/data', methods=['GET'])
def get_data():
    data = Data.query.all()
    return jsonify([{ 'id': d.id, 'name': d.name, 'value': d.value ,  'value2': d.value2,
        'value3': d.value3} for d in data])

@app.route('/data', methods=['POST'])
def add_data():
    new_data = Data(
        name=request.json['name'], 
        value=request.json['value'],
        value2=request.json.get('value2', ''),  # Default to empty if not provided
        value3=request.json.get('value3', '')
    )
    db.session.add(new_data)
    db.session.commit()
    return jsonify({'message': 'Data added!'})


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

if __name__ == '__main__':
    if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

    
    
