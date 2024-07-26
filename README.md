# Messaging System

## Overview

This messaging system is built using Flask for the web application and Celery for asynchronous task management. It allows for sending emails and logging requests, ensuring efficient and scalable processing.

## Prerequisites

- Python 3.12+
- Virtualenv
- RabbitMQ (or another broker supported by Celery)
- An SMTP email account
- Nginx
- ngrok for external access

## Setup

### 1. Clone the Repository

```
git clone https://github.com/hayzedak/HNG3.git
cd HNG3/messaging_system
```

### 2. Create and Activate a Virtual Environment

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```
pip install Flask celery
```

### 4. Configure Environment Variable

Set the `EMAIL_PASSWORD` environment variable:

    
    export EMAIL_PASSWORD=your_email_password
    


Make sure to replace your_email_password with your actual email [app password] (https://myaccount.google.com/apppasswords).

### 5. Initialize RabbitMQ

Ensure that RabbitMQ is running on your system. You can start RabbitMQ with:

```
sudo systemctl start rabbitmq-server
```

### 6. Ensure Log Directory Exists 

Ensure the /var/log/messaging_system.log file exists:

```
sudo mkdir -p /var/log
sudo touch /var/log/messaging_system.log

```
### 6. Configure Nginx

Install Nginx if it's not already installed:

```
sudo apt update
sudo apt install nginx
```

Create an Nginx configuration file for your Flask application. For example, create /etc/nginx/sites-available/messaging_system:


```
sudo nano /etc/nginx/sites-available/messaging_system
```


Add the following configuration: remember to replace with your ip address.


```
server {
    listen 80;
    server_name your_domain_or_ip;

    location / {
        proxy_pass http://your_domain_or_ip:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    error_log /var/log/nginx/messaging_system_error.log;
    access_log /var/log/nginx/messaging_system_access.log;
}

```


Enable the configuration by creating a symlink:

```
sudo ln -s /etc/nginx/sites-available/messaging_system /etc/nginx/sites-enabled
```

Test the Nginx configuration and restart Nginx:

```
sudo nginx -t
sudo systemctl restart nginx
```

Now, your Flask application should be accessible via your domain or IP.


## Running the Application

1. Start the Flask Application

Remember to activate the virtual environment.

```
python3 app.py
```

2. Start the Celery worker: In another terminal, ensure you activate the virtual env.

    ```
    celery -A tasks worker --loglevel=info
    ```


## Exposing with ngrok

To expose your local server to the internet using ngrok, follow these steps:

- Download and install ngrok from [ngrok.com](https://ngrok.com/).

- Start ngrok with the following command:

    ```
    ngrok http 5000
    ```

- Copy the generated ngrok URL and use it to access your Flask application from the internet.

## Usage

- To send an email, navigate to `http://your_ngrok_endpoint/?sendmail=mailto:recipient@example.com`.
- To log a request, navigate to `http://your_ngrok_endpoint/?talktome`.


## Troubleshooting

If you encounter any issues, check the logs for more information:

- Flask application logs: `/var/log/messaging_system.log`
- Celery worker logs: Run `sudo journalctl -u celery.service -f` to view real-time logs.
- Nginx logs: `/var/log/nginx/error.log` and `/var/log/nginx/access.log`






















