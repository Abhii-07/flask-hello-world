from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate



app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/wanderlust_backend_db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/wanderlust_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)



# Models

class Destination(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    location = db.Column(db.String(255), nullable=False)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Float, nullable=False)

class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination_id = db.Column(db.Integer, db.ForeignKey('destination.id'), nullable=False)
    activity = db.Column(db.String(255), nullable=False)

# Routes

# Destination Routes


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/destinations', methods=['GET'])
def get_destinations():
    destinations = Destination.query.all()
    destination_list = []
    for destination in destinations:
        destination_dict = {
            'id': destination.id,
            'name': destination.name,
            'description': destination.description,
            'location': destination.location
        }
        destination_list.append(destination_dict)
    return jsonify(destination_list)

@app.route('/destinations', methods=['POST'])
def create_destination():
    data = request.json
    destination = Destination(name=data['name'], description=data.get('description'), location=data.get('location'))
    db.session.add(destination)
    db.session.commit()
    return jsonify({'message': 'Destination created successfully'})

@app.route('/destinations/<int:destination_id>', methods=['GET'])
def get_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        destination_data = {
            'id': destination.id,
            'name': destination.name,
            'description': destination.description,
            'location': destination.location
        }
        return jsonify(destination_data)
    return jsonify({'message': 'Destination not found'}, 404)

@app.route('/destinations/<int:destination_id>', methods=['PUT'])
def update_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        data = request.json
        destination.name = data['name']
        destination.description = data.get('description')
        destination.location = data.get('location')
        db.session.commit()
        return jsonify({'message': 'Destination updated successfully'})
    return jsonify({'message': 'Destination not found'}, 404)

@app.route('/destinations/<int:destination_id>', methods=['DELETE'])
def delete_destination(destination_id):
    destination = Destination.query.get(destination_id)
    if destination is not None:
        db.session.delete(destination)
        db.session.commit()
        return jsonify({'message': 'Destination deleted successfully'})
    return jsonify({'message': 'Destination not found'}, 404)

# Expense Routes

@app.route('/expenses', methods=['POST'])
def create_expense():
    data = request.json
    destination_id = data['destination_id']
    expense = Expense(destination_id=destination_id, category=data['category'], amount=data['amount'])
    db.session.add(expense)
    db.session.commit()
    return jsonify({'message': 'Expense added successfully'})

@app.route('/expenses/<int:destination_id>', methods=['GET'])
def get_expenses(destination_id):
    expenses = Expense.query.filter_by(destination_id=destination_id).all()
    expense_list = []
    for expense in expenses:
        expense_dict = {
            'id': expense.id,
            'category': expense.category,
            'amount': expense.amount
        }
        expense_list.append(expense_dict)
    return jsonify(expense_list)

@app.route('/expenses/<int:expense_id>', methods=['PUT'])
def update_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense is not None:
        data = request.json
        expense.category = data['category']
        expense.amount = data['amount']
        db.session.commit()
        return jsonify({'message': 'Expense updated successfully'})
    return jsonify({'message': 'Expense not found'}, 404)

@app.route('/expenses/<int:expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expense = Expense.query.get(expense_id)
    if expense is not None:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({'message': 'Expense deleted successfully'})
    return jsonify({'message': 'Expense not found'}, 404)

# Itinerary Routes

@app.route('/itineraries', methods=['POST'])
def create_itinerary():
    data = request.json
    destination_id = data['destination_id']
    itinerary = Itinerary(destination_id=destination_id, activity=data['activity'])
    db.session.add(itinerary)
    db.session.commit()
    return jsonify({'message': 'Itinerary activity added successfully'})

@app.route('/itineraries/<int:destination_id>', methods=['GET'])
def get_itineraries(destination_id):
    itineraries = Itinerary.query.filter_by(destination_id=destination_id).all()
    itinerary_list = []
    for itinerary in itineraries:
        itinerary_dict = {
            'id': itinerary.id,
            'activity': itinerary.activity
        }
        itinerary_list.append(itinerary_dict)
    return jsonify(itinerary_list)

@app.route('/itineraries/<int:itinerary_id>', methods=['PUT'])
def update_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if itinerary is not None:
        data = request.json
        itinerary.activity = data['activity']
        db.session.commit()
        return jsonify({'message': 'Itinerary activity updated successfully'})
    return jsonify({'message': 'Itinerary activity not found'}, 404)

@app.route('/itineraries/<int:itinerary_id>', methods=['DELETE'])
def delete_itinerary(itinerary_id):
    itinerary = Itinerary.query.get(itinerary_id)
    if itinerary is not None:
        db.session.delete(itinerary)
        db.session.commit()
        return jsonify({'message': 'Itinerary activity deleted successfully'})
    return jsonify({'message': 'Itinerary activity not found'}, 404)

if __name__ == '__main__':
    app.run(debug=True)
