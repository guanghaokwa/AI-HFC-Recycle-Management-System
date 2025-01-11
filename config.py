import secrets

SECRET_KEY = secrets.token_hex(24)
NGROK_TOKEN = "YOUR_NGROK_TOKEN"
DB_PARAMS = {
    "database": "RecycleMgmt", 
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}