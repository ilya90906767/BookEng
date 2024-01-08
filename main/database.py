import psycopg2 

def connect():
    conn = psycopg2.connect(
        database="bookengdb",
        user="betyaevilya",
        password="90906767",
        host="localhost",
        port="5432"
    )

    conn.autocommit = True
    cursor = conn.cursor()
    return cursor

def create_table(): 
    try:
        curs = connect()
        query = """
            CREATE TABLE IF NOT EXISTS users(
                id SERIAL PRIMARY KEY,
                user_id INTEGER UNIQUE NOT NULL,
                data_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        curs.execute(query)
        print("Table created successfully.")

    except Exception as error:
        print(f"An error occurred: {error}")


def create_user(user_id):
    curs = connect()
    if curs is not None:
        try:
            query = """ INSERT INTO users (id, user_id) VALUES (DEFAULT, %s); """
            curs.execute(query, [user_id])
            print('USER WAS ADDED')
        except Exception as error:
            print(f"An error occurred when trying to execute the query: {error}")
            return None
    else:
        return None

def is_user_exist(user_id):
    curs = connect()
    if curs is not None:
        try:
            query = "SELECT * FROM users WHERE user_id = %s"
            curs.execute(query, [user_id])
            result = curs.fetchone()

            if result is not None:
                    return True
            else:
                return False
        except Exception as error:
            print(f"An error occurred when trying to execute the query: {error}")
            return None
    else:
        return None

def get_users():
    curs = connect()
    curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = curs.fetchall()


    for table in tables:
        print(table)
    """curs.execute("SELECT * FROM users")
    users = curs.fetchall()
    for user in users:
        print(user)"""
