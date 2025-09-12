import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator that automatically handles opening and closing database connections.
    The connection is passed as the first argument to the decorated function.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Open database connection
        conn = sqlite3.connect('database.db')  # You can make this configurable
        try:
            # Pass connection as first argument to the decorated function
            result = func(conn, *args, **kwargs)
            # Commit any changes
            conn.commit()
            return result
        except Exception as e:
            # Rollback in case of error
            conn.rollback()
            raise e
        finally:
            # Always close the connection
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that manages database transactions by automatically committing or rolling
    back changes. If the function raises an error, rollback; otherwise commit the transaction.
    
    Note: This decorator assumes the connection is passed as the first argument to the function.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            # Start transaction (SQLite is in autocommit mode by default, 
            # so we need to explicitly start a transaction)
            conn.execute("BEGIN")
            
            # Execute the decorated function
            result = func(conn, *args, **kwargs)
            
            # If no exception occurred, commit the transaction
            conn.commit()
            return result
        except Exception as e:
            # If an exception occurred, rollback the transaction
            conn.rollback()
            raise e
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    #### Update user's email with automatic transaction handling

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
