import os
import logging
import time  # Import the time module
from flask import Flask, request
from tasks import send_email

app = Flask(__name__)

# Ensure logging directory exists
log_dir = "/var/log"
log_file = os.path.join(log_dir, "messaging_system.log")
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
if not os.path.exists(log_file):
    open(log_file, 'a').close()

logging.basicConfig(filename=log_file, level=logging.INFO)

@app.route('/')
def index():
    sendmail = request.args.get('sendmail')
    talktome = request.args.get('talktome')

    try:
        if sendmail:
            recipient_email = sendmail.replace('mailto:', '')
            send_email.delay(recipient_email)
            return "Email sent!"

        if talktome:
            logging.info(f"Talk to me request at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            return "Logged time!"

        return "Welcome to the messaging system!"
    except Exception as e:
        logging.error(f"Error occurred: {e}")
        return "An error occurred. Check the logs for details.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
