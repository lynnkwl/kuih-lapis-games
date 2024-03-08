from telegram.ext import Updater, CommandHandler
from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Define a function to handle the /start command
def start(update, context):
    update.message.reply_text('Hello! I am your notification bot. Send me a message and I will notify you!')

# Define a function to handle sending notifications
def send_notification(username, message):
    try:
        bot.send_message(chat_id=username, text=message)
        return jsonify({"success": True, "message": f"Notification sent successfully. ChatID = <{username}> Message = <{message}>"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

# Define a route to receive notification requests
@app.route('/send_notification', methods=['POST'])
def send_notification_api():
    data = request.json
    username = data.get('username')
    message = data.get('message')

    if not username or not message:
        return jsonify({"success": False, "error": "Username and message are required"})

    return send_notification(username, message)

def main():
    # Initialize the bot with the bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if token is None:
        print("Please set TELEGRAM_BOT_TOKEN environment variable.")
        return
    updater = Updater(token, use_context=True)
    global bot
    bot = updater.bot

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Start the Bot
    updater.start_polling()

    # Run the Flask app
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()
