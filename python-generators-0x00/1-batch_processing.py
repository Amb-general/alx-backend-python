#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from the user_data table in batches.
    Yields a list of dictionaries, each batch containing up to batch_size rows.
    """
    connection = mysql.connector.connect(
        host="localhost",
        user="root",        # update if needed
        password="root",    # update if needed
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM user_data")

    batch = []
    for row in cursor:
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []  # reset batch

    # yield any leftover rows
    if batch:
        yield batch

    cursor.close()
    connection.close()


def batch_processing(batch_size):
    """
    Process each batch: filter users over the age of 25 and print them.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)

