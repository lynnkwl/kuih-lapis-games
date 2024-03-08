from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/wishlist'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Wishlist(db.Model):
    __tablename__ = 'wishlist'

    customerID = db.Column(db.Integer, primary_key=True)
    gameName = db.Column(db.String(64), nullable=False)


    def __init__(self, customerID, gameName):
        self.customerID = customerID
        self.gameName = gameName


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


if __name__ == '__main__':
    app.run(port=5000, debug=True)