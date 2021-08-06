from flask import Blueprint, request, jsonify
from flask.wrappers import Response
from cars_inventory.helpers import token_required
from cars_inventory.models import db, User, Cars, car_schema, cars_schema


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'some_value': 52, 'another_value': 800}

@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    travel_range = request.json['travel_range']
    passengers = request.json['passengers']
    cost_of_prod = request.json['cost_of_prod']
    user_token = current_user_token.token

    print(f'TESTER: {current_user_token.token}')

    car = Cars(name, description, price, travel_range, passengers, cost_of_prod, user_token = user_token)

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

    # Retrieve all

api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner= current_user_token.token
    cars = Cars.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# Retrieve a single car endpoint

@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_cars(current_user_token, id):
    car = Cars.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)

# Update car by ID endpoint

@api.route('/cars/<id>', methods= ['POST'])
@token_required
def update_cars(current_user_token, id):
    cars = Cars.query.get(id)
    print(cars)
    if cars:
        cars.name = request.json['name']
        cars.description = request.json['description']
        cars.price = request.json['price']
        cars.travel_range = request.json['travel_range']
        cars.cost_of_prod = request.json['cost_of_prod']
        cars.user_token = current_user_token.token

        db.session.commit()

        response = car_schema.dump(cars)
        return jsonify(response)
    else:
        return jsonify({'Error': "That car does not exist!"})

# Delete car by id
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    car = Cars.query.get(id)
    if car:
        db.session.delete(car)
        db.session.commit()

        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({'Error': "That car does not exist!"})