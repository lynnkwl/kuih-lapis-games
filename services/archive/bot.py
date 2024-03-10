from telegram import Bot
from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Define a function to handle the /start command
def start(update, context):
    return 'Hello, welcome to KuihGames! I am your notification bot. Send me a message and I will notify you!'

# Define a function to handle sending notifications
def send_notification(chat_id, message, bot_token):
    try:
        response = requests.post(
        url='https://api.telegram.org/bot{0}'.format(bot_token),
        data={'chat_id': chat_id, 'text': message}
        ).json()
        # bot = Bot(token=bot_token)
        # bot.send_message(chat_id=chat_id, text=message)
        return jsonify({"success": True, "message": f"Notification sent successfully. ChatID = <{chat_id}> Message = <{message}> Bot token= <{bot_token}>"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Define a route to receive notification requests
@app.route('/send_notification', methods=['POST'])
def send_notification_api():
    data = request.json
    chat_id = data.get('chat_id')
    message = data.get('message')
    bot_token = "6475666330:AAFuGhLSKQ8hGh41wbErRxNE8HDyCLwXlWQ"
    # os.getenv('TELEGRAM_BOT_TOKEN')

    if not chat_id or not message:
        return jsonify({"success": False, "error": "Username and message are required"})

    return send_notification(chat_id, message, bot_token)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
