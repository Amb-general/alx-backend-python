#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator that streams rows from the user_data table one by one.
    """
    # Connect to the ALX_prodev database
    connection = mysql.connector.connect(
        host="localhost",
        user="root",        # change if your MySQL user is different
        password="root",    # change if your MySQL password is different
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    # Execute query
    cursor.execute("SELECT * FROM user_data")

    # Stream rows one by one
    for row in cursor:
        yield row

    # Clean up after iteration
    cursor.close()
    connection.close()

