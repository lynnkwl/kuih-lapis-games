from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys
from os import environ

import requests
from invokes import invoke_http

import pika
import json
import amqp_connection

app = Flask(__name__)
CORS(app)

wishlist_URL = environ.get('wishlist_URL') or "http://localhost:5001/wishlist_database"
send_email_URL = environ.get('send_email_URL') or "http://localhost:5002/send_email"
 
exchangename = "recommendation"
exchangetype = "topic"

connection = amqp_connection.create_connection()
channel = connection.channel()

@app.route("/recommend", methods=['POST'])
def recommend():
    if request.is_json:
        try:
            # Get the JSON data from the request
            req = request.get_json()
            print("\nReceived a request to recommend item in [JSON]:", req)

            #step 1: compile user's fave genre from wishlist
            #   can add game genre into wishlist as well
            favourite_genre = req['payload'][0]
        
            #step 1.5: compile user's interested genre from activity log
            
            
            #step 2: get all games of that genre from catalog
            
            
            #step 3: get all games that the customer owns from that genre
            # fire off an API to user database to obtain it? will ask kango 
        
            
            #step 4: filter out games that user already owns
            
            #step 5: return the list of games
            
            #step 6: notify customer of the recommendation

            # Validate the JSON data
            if 'user_id' not in req:
                return jsonify({
                    "code": 400,
                    "data": "Invalid request data"
                }), 400

            user_id = req['user_id']

            # Invoke the user service
            user_result = invoke_http(user_svc, 'GET', f'/user/{user_id}')
            print(f"\nReceived a response from user service: {user_result}")

            if user_result['code'] != 200:
                return jsonify({
                    "code": 500,
                    "data": "User service is unavailable"
                }), 500

            user_data = user_result['data']

            # Get the user's age

        except:
            return jsonify({
                "code": 500,
                "data": "Unable to process the request"
            }), 500
        

def processRecommendation(customer_id):
    print('\n-----Invoking wishlist microservice-----')
    wishlist = invoke_http(wishlist_URL, method='GET', json=customer_id)

    wishlist_dict = wishlist['data']['wishlist']

    #---if we decide to log wishlist activity---
    # code = wishlist["code"]
    # message = json.dumps(wishlist)

    # if code not in range(200, 300):
    #     channel.basic_publish(exchange=exchangename, routing_key="reco.error", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2)) 

    #     print("\nwishlist status ({:d}) published to the RabbitMQ Exchange:".format(
    #         code), wishlist)

    #     return {
    #         "code": 500,
    #         "data": {"wishlist": wishlist},
    #         "message": "wishlist failure"
    #     }
    # else: 
    #     print("\nReceived wishlist from wishlist microservice:", wishlist)
    #     print("\n\n-----Publishing the wishlist message with routing_key=wishlist.info-----")
    #     channel.basic_publish(exchange=exchangename, routing_key="wishlist.info", 
    #         body=message, properties=pika.BasicProperties(delivery_mode = 2))

    #step 2: get all games of that genre from catalog
    # this part I checking w lynn on how to get all games of a genre from catalog

    #step 3: get all games that the customer owns from that genre

    #step 4: filter out games that user already owns

    #step 5: return the list of games

    #step 6: notify customer of the recommendation

    recommended_games=[]
    list_indent = len(recommended_games)

    recommended_games_json = {
        "recommended_games_list": recommended_games
    }


    email_body = f"Here are some recommended games for you:\n\n"
    index = 1
    for game in recommended_games:
        email_body += f"{index}. {game}\n"
        index += 1

    email_body += "\n\nEnjoy your games!" 
    #can explore including a link for them to purchase the game

    recommendation_message = {
         "customer_address": "example@example.com",
         "email_subject": "Recommendation for you based on your wishlist (and activity log)",
         "email_body": email_body
     }
    
    invoke_http(send_email_URL, method='POST', json=recommendation_message)

    #log email activity
