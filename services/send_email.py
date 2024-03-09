# This script defines a Flask web application that handles POST requests to send emails.
# It expects JSON data containing 'customer_address', 'email_subject', and 'email_body'.


# Usage:
#   1. Send a POST request to '/send_email' endpoint with JSON data containing:
#      {
#          "customer_address": "example@example.com",
#          "email_subject": "Subject of the email",
#          "email_body": "Body of the email"
#      }
#   2. The application will respond with a JSON message indicating that the email will be sent.



from redmail import gmail
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()
    customer_address = data.get('customer_address')
    email_subject = data.get('email_subject')
    email_body = data.get('email_body')

    
    gmail.username = "kuihgames6@gmail.com"
    gmail.password = "vfjs gdde nffm mmmk"

    gmail.send(
        subject=email_subject,
        receivers=[customer_address],
        text=email_body
    )

    response = {
        "message": "Email will be sent to {} with subject: '{}' and body: '{}'".format(customer_address, email_subject, email_body)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
