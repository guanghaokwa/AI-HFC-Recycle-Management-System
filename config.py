import secrets

SECRET_KEY = secrets.token_hex(24)
NGROK_TOKEN = "YOUR_NGROK_TOKEN"
DB_PARAMS = {
    "database": "GreenMerlionAI", # Replace with your database name
    "user": "postgres", # Replace with your postgresql username
    "password": "password", # Replace with your postgresql password
    "host": "localhost", # Replace with host name (Default: localhost)
    "port": "5432" # Replacce with port number (Default: 5432)
}