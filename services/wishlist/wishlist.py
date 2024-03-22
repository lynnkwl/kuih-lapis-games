from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json 
from os import environ
import schedule
import time
import requests
from collections import Counter

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/wishlist_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# import amqp_connection

#create a connection and a channel to the broker to publish messages to activity_log, error queues
# connection = amqp_connection.create_connection() 
# channel = connection.channel()
        
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

    # If the wishlist already exists, remove its entry~
    if existing_wishlist:
        return jsonify({"message": "Wishlist entry already exists."}), 200
    
     # If the wishlist doesn't exist, create a new entry
    new_wishlist_entry = Wishlist(customerID=customerID, gameName=request.json['gameName'])
    db.session.add(new_wishlist_entry)
    db.session.commit()

    return jsonify({"message": "Wishlist entry created."}), 201


@app.route("/wishlist/<int:customerID>", methods=['POST'])
def sending_log_to_activity_log_view_interaction(customerID):
    message = f"{customerID} has viewed the following item"    
    # publish the message to activity log when user views the games
    # channel.basic_publish(exchange="kuihgames_Activity_Log", routing_key="#", body=message)

@app.route("/wishlist/<int:customerID>", methods=['POST'])
def sending_log_to_activity_log_wishlist_interaction(customerID):
    message = f"{customerID} has added this item to their wishlist"    
    # publish the message to activity log when user views the games
    # channel.basic_publish(exchange="kuihgames_Activity_Log", routing_key="#", body=message)

def computing_genre_list_in_descending_order():
    # Query all entries in the Wishlist model
    wishlists = db.session.query(Wishlist).all()

    # Extract the favorite genres from the wishlists
    favorite_genres = [wishlist.favgenre for wishlist in wishlists]

    # Count the occurrences of each genre using Counter from collections
    genre_counts = Counter(favorite_genres)

    # Sort the genres in descending order based on their counts
    sorted_genres = [genre for genre, count in genre_counts.most_common()]

    # Return the list of genres, descending order
    return sorted_genres
            
def perform_post_request():
    # cron job that runs every midnight to updates the favgenre of the user based on their wishlist that day
    
    # Define the URL and payload for your POST request
    url = 'tobedefined-likely-recommend-function-in-recommender.py'
    sorted_genre = computing_genre_list_in_descending_order()
    payload = {'favgenre': sorted_genre}

    # Send the POST request
    response = requests.post(url, json=payload)

    # Print the response status code and content
    print(f'Response Status Code: {response.status_code}')
    print(f'Response Content: {response.text}')

    # Schedule the POST request to run every day at midnight (12:00 AM)
    schedule.every().day.at('00:00').do(perform_post_request)  

    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for 1 second to avoid high CPU usage

if __name__ == '__main__':
    app.run(port=5000, debug=True)