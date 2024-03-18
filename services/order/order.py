#!/usr/bin/env python3
# The above shebang (#!) operator tells Unix-like environments
# to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint

from datetime import datetime

#function for generating mock data if its empty
def generate_mock_data():
    try:
        # Generate some mock users if the table is empty
        if db.session.query(User).count() == 0:
            for i in range(1, 11):
                customer_id = f"{i}"
                email = f"user{i}@example.com"
                username = f"user{i}"
                address = f"Address_{randint(1, 100)}"
                credits = randint(0, 100)
                user = User(customer_id=customer_id, email=email, username=username, address=address, credits=credits)
                db.session.add(user)
                db.session.commit()

        # Generate some mock retailers if the table is empty
        if db.session.query(Retailer).count() == 0:
            for i in range(1, 11):
                retailer_id = f"{i}"
                email = f"retailer{i}@example.com"
                username = f"retailer{i}"
                address = f"Address_{randint(1, 100)}"
                credits = randint(0, 100)
                retailer = Retailer(retailer_id=retailer_id, email=email, username=username, address=address, credits=credits)
                db.session.add(retailer)
                db.session.commit()

        # Generate some mock orders and order items
        if db.session.query(Order).count() == 0 and db.session.query(Order_Item).count() == 0:
            for i in range(1,11):
                # Generate random data for an order
                order_id = f"{i}"
                status_options = ['shipped', 'processing', 'cancelled', 'pending']
                status = status_options[randint(0, len(status_options) - 1)]
                payment_status_options = ['paid', 'pending', 'failed']
                payment_status = payment_status_options[randint(0, len(payment_status_options) - 1)]
                shipping_address = f"Address_{randint(1, 100)}"
                customer_id = randint(1,10)
                
                order = Order(order_id=order_id, customer_id=customer_id, status=status, payment_status=payment_status, shipping_address=shipping_address)
                db.session.add(order)
                db.session.commit()

                # Generate random order items for the order
                for i in range(randint(1, 5)):
                    game_id = f"GameID_{randint(1, 100)}"
                    quantity = randint(1, 10)
                    retailer_id = randint(1,10)
                    order_item = Order_Item(retailer_id=retailer_id, order_id=order.order_id, game_id=game_id, quantity=quantity)
                    db.session.add(order_item)
                    db.session.commit()

            print("Mock data generation completed.")
        else:
            print("Mock data has already been generated before.")
    except Exception as e:
        print(f"An error occurred while generating mock data: {e}")

#regular Flask and SQLALCHEMY start
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@host.docker.internal:3306/kueh_games'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

#creating tables

class User(db.Model):
    __tablename__ = 'user'

    customer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Float, nullable=False, default=0)

class Retailer(db.Model):
    __tablename__ = 'retailer'

    retailer_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable = False)
    username = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    credits = db.Column(db.Float, nullable=False, default=0)

class Order(db.Model):
    __tablename__ = "order"

    order_id = db.Column(db.Integer, primary_key=True) #auto-increments
    customer_id = db.Column(db.ForeignKey(
        'user.customer_id', onupdate='CASCADE'), index=True) #taken from Users database
    status = db.Column(db.String(15), nullable = False) #shipped, processing, cancelled, pending
    created = db.Column(db.DateTime, nullable= False, default=datetime.now)
    modified = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    payment_status = db.Column(db.String(10), nullable = False) #paid, pending, failed #probaby FK from Payment
    shipping_address = db.Column(db.String(255), nullable = False) 
    
    def json(self):
        dto = {
            'order_id': self.order_id,
            'customer_id': self.customer_id,
            'status': self.status,
            'created': self.created,
            'modified': self.modified,
            'payment_status': self.payment_status,
            'shipping_address': self.shipping_address
        }

        dto['order_item'] = []
        for oi in self.order_item:
            dto['order_item'].append(oi.json())

        return dto

class Order_Item(db.Model):
    __tablename__ = 'order_item'

    item_id = db.Column(db.Integer, primary_key=True) #auto-increments
    order_id = db.Column(db.ForeignKey(
        'order.order_id', ondelete='CASCADE', onupdate='CASCADE'), nullable=False, index=True)
    game_id = db.Column(db.String(100), nullable = False) #e.g, supermarionintendo
    quantity = db.Column(db.Integer, nullable = False) #e.g, 2
    retailer_id = db.Column(db.ForeignKey(
        'retailer.retailer_id', onupdate='CASCADE'), index=True) #e.g, gamesandwares
    order = db.relationship(
        'Order', primaryjoin='Order_Item.order_id == Order.order_id', backref='order_item')

    def json(self):
        return {'item_id': self.item_id,
                'order_id': self.order_id,
                'game_id': self.game_id,
                'quantity': self.quantity,
                'retailer_id': self.retailer_id
                }

@app.route("/order")
def get_all():
    orderlist = db.session.scalars(db.select(Order)).all()
    if len(orderlist):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "orders": [order.json() for order in orderlist]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no orders."
        }
    ), 404

@app.route("/order/<string:order_id>")
def find_by_order_id(order_id):
    order = db.session.scalars(
        db.select(Order).filter_by(order_id=order_id).limit(1)).first()
    if order:
        return jsonify(
            {
                "code": 200,
                "data": order.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "order_id": order_id
            },
            "message": "Order not found."
        }
    ), 404

@app.route("/order", methods=['POST'])
def create_order():
    customer_id = request.json.get('customer_id', None)
    shipping_address = request.json.get('shipping_address', None)
    order = Order(customer_id=customer_id, shipping_address=shipping_address, status='processing', payment_status='paid')

    cart_item = request.json.get('cart_item')
    for item in cart_item:
        order.order_item.append(Order_Item(
            game_id=item['game_id'], quantity=item['quantity'], retailer_id=item['retailer_id']))

    try:
        db.session.add(order)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while creating the order. " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": order.json()
        }
    ), 201

with app.app_context():
    db.create_all()
    generate_mock_data()

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__) + ": manage orders ...")
    app.run(host='0.0.0.0', port=5000, debug=True)