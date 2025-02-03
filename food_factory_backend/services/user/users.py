from constants.queries import USER_INSERT_QUERY, FETCH_ALL_USERS_QUERY ,FETCH_USER_BY_EMAIL

def insert_user(db_connection, data):
    """ Insert a new user into the database.
    Args:
        db_connection: The active database connection.
        data (dict): A dictionary containing user data.
            Required keys: 'username', 'email', 'password', 'role', 'is_delete'.
    Returns:
        bool: True if the user was successfully inserted, False otherwise."""

    try:
        cursor = db_connection.cursor()
        print("Data - ", data)
        cursor.execute(USER_INSERT_QUERY, (
            data.get('username'),
            data.get('email'),
            data.get('password'),
            data.get('role'),
            data.get('is_delete', 0)  
        ))

        # Commit the transaction
        db_connection.commit()
        return True
    except Exception as e:
        print(f"Error inserting user: {str(e)}")
        return False
    finally:
        cursor.close()


def fetchall_users(db_connection):
    try:
        cursor = db_connection.cursor()
        cursor.execute(FETCH_ALL_USERS_QUERY)
        data = cursor.fetchall()
        db_connection.commit()
        return data
    except Exception as e:
        print(f"Error fetching users: {str(e)}")
        return e
    finally:
        cursor.close()

def fetch_user_by_email(db_connection, email):
    try:
        cursor = db_connection.cursor(dictionary=True)  
        cursor.execute(FETCH_USER_BY_EMAIL, (email,))
        user = cursor.fetchone() 
        return user  
    except Exception as e:
        print(f"Error fetching user: {e}")
        return None
    finally:
        cursor.close()