from mysql.connector import Error
import mysql.connector
from db_config import DB_HOST, DB_NAME,\
    DB_USER, DB_USER_PASSWORD


def connect_to_db():
    """Create a database connection to execute a query
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_USER_PASSWORD
        )
        if connection.is_connected():
            return connection

    except Error as e:
        print("Error while connecting to MySQL", e)


def add_new_user(user_id: int, level=1):
    """Query to add a new user to the database
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    INSERT INTO users(user_id, level)
    VALUES ({user_id},{level})
        """)

    connection.commit()
    print(f"Add new user with id: {user_id}\tlvl:{level}")


def get_user_by_id(user_id: int) -> bool:
    """If there is a user with this id in
    the database, returns True
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    SELECT user_id FROM users
    WHERE user_id={user_id}
        """)

    result = cursor.fetchone()

    return False if result is None else True


def get_all_users() -> list:
    """Returns a list of all user tuples from database
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT id, user_id, level FROM users
        """)

    result = cursor.fetchall()
    print(f"{result}")
    return result


def get_users_with_lvl(level: int) -> list:
    """Returns a list of tuples users
    with the appropriate level
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    SELECT id, user_id, level FROM users 
    WHERE level = {level}
    ORDER BY id
        """)

    result = cursor.fetchall()
    print(f"{result}")
    return result


def get_user_level(user_id: int) -> int:
    """Returns the user level by his id
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    SELECT level FROM users 
    WHERE user_id = {user_id}
        """)

    result = cursor.fetchone()
    return result[0]


def update_user_level(user_id: int, level: int):
    """Change user level by user ID
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    UPDATE users SET level='{level}'
    WHERE user_id = {user_id}
        """)

    connection.commit()

    print(f"Level for user {user_id} updated on {level}")


def update_user_first_name(user_id: int, first_name: str):
    """Change username by userid
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    UPDATE users SET first_name = '{first_name}'
    WHERE user_id = {user_id}
        """)

    connection.commit()

    print(f"First name for user {user_id} updated on {first_name}")


def update_user_last_name(user_id: int, last_name: str):
    """Change user's last name by his id
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    UPDATE users SET last_name = '{last_name}'
    WHERE user_id = {user_id}
        """)

    connection.commit()

    print(f"Last name for user {user_id} updated on {last_name}")


def update_user_user_name(user_id: int, user_name: str):
    """Change user name by his id
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    UPDATE users SET user_name = '{user_name}'
    WHERE user_id = {user_id}
        """)

    connection.commit()

    print(f"User name for user {user_id} updated on {user_name}")


def update_user_age(user_id: int, age: int):
    """Change user age by his id
    """
    connection = connect_to_db()
    cursor = connection.cursor()

    cursor.execute(rf"""
    UPDATE users SET age = {age}
    WHERE user_id = {user_id}
        """)

    connection.commit()

    print(f"Age for user {user_id} updated on {age}")


# def query_boilerplate():
#     connection = connect_to_db()
#     cursor = connection.cursor()

#     cursor.execute(rf"""
# """)

#     connection.commit()

#     print(f"")
#     pass
