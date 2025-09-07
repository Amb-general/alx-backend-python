#!/usr/bin/python3
import mysql.connector
import csv

def connect_db():
    """
    Connect to MySQL server (no specific DB).
    Returns the connection object.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # update with your MySQL user
            password="password" # update with your MySQL password
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_database(connection):
    """
    Create the ALX_prodev database if it doesn't exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")


def connect_to_prodev():
    """
    Connect directly to ALX_prodev database.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",        # update with your MySQL user
            password="password",# update with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def create_table(connection):
    """
    Create user_data table if it does not exist.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            )
        """)
        connection.commit()
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")


def insert_data(connection, csv_file):
    """
    Insert rows from CSV into user_data table (ignoring duplicates).
    """
    try:
        cursor = connection.cursor()
        with open(csv_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cursor.execute("""
                    INSERT IGNORE INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s)
                """, (row["user_id"], row["name"], row["email"], row["age"]))
        connection.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data: {e}")

