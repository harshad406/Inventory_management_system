import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Harshad@_2728",
        database="inventory_system"
    )