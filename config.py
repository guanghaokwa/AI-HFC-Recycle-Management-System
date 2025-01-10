import secrets

SECRET_KEY = secrets.token_hex(24)

DB_PARAMS = {
    "database": "RecycleMgmt", 
    "user": "postgres",
    "password": "password",
    "host": "localhost",
    "port": "5432"
}