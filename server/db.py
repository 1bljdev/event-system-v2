import mysql.connector

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "event_db",
    "port": 3306
}

def get_connection():
    return mysql.connector.connect(**db_config)
