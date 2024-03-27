from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json 
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/wishlist_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

import sys
sys.path.append('..')
from amqp import amqp_connection

#create a connection and a channel to the broker to publish messages to activity_log, error queues
connection = amqp_connection.create_connection() 
channel = connection.channel()

db = SQLAlchemy(app)

class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    customerID = db.Column(db.Integer, primary_key=True)
    gameName = db.Column(db.String(64), nullable=False)


    def __init__(self, customerID, gameName):
        self.customerID = customerID
        self.gameName = gameName
        
@app.route("/wishlist/<int:customerID>")
def return_all_wish_list_of_customer(customerID):
    wish_list_entries = db.session.query(Wishlist).filter(Wishlist.customerID == customerID).all()
    wishlist_dicts = [{"customerID": wishlist.customerID, "gameName": wishlist.gameName} for wishlist in wish_list_entries]

    return jsonify(
            {
                "code": 200,
                "data": {
                    "wishlist": wishlist_dicts
                }
            }
        )

@app.route("/wishlist/<int:customerID>", methods=['POST'])
def create_user_wishlist(customerID):
    existing_wishlist = db.session.query(Wishlist).filter_by(customerID=customerID).first()

    # If the wishlist already exists, remove its entry
    if existing_wishlist:
        db.session.delete(existing_wishlist)
        db.session.commit()
        return jsonify({"message": "Wishlist entry removed."}), 200
    
     # If the wishlist doesn't exist, create a new entry
    new_wishlist_entry = Wishlist(customerID=customerID, gameName=request.json['gameName'])
    db.session.add(new_wishlist_entry)
    db.session.commit()

    return jsonify({"message": "Wishlist entry created."}), 201

@app.route("/wishlist/view_interaction/<int:customerID>", methods=['POST'])
def sending_log_to_activity_log_view_interaction(customerID):
    message = f"{customerID} has viewed the following item"    
    # publish the message to activity log when user views the games
    channel.basic_publish(exchange="kuihgames_Activity_Log", routing_key="#", body=message)

@app.route("/wishlist/wishlist_interaction/<int:customerID>", methods=['POST'])
def sending_log_to_activity_log_wishlist_interaction(customerID):
    message = f"{customerID} has added this item to their wishlist"    
    # publish the message to activity log when user views the games
    channel.basic_publish(exchange="kuihgames_Activity_Log", routing_key="#", body=message)


if __name__ == '__main__':
    app.run(port=5000, debug=True)