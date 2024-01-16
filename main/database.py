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
        
        query = """
        CREATE TABLE IF NOT EXISTS books(
                book_id SERIAL PRIMARY KEY,
                user_id SERIAL,
                book_name VARCHAR(255) DEFAULT 'Unknown',
                book_author VARCHAR(255) DEFAULT 'Unknown',
                book_picture VARCHAR(255) DEFAULT 'NoPicture',
                book_src VARCHAR(255),
                current_progress INT DEFAULT 0,
                data_added TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(user_id) 
                )
        """
        
        curs.execute(query)
        print("Tables created successfully.")

    except Exception as error:
        print(f"An error occurred: {error}")
        

def migrate():
    curs = connect()
    curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tables = curs.fetchall()
    print(tables, 'will be deleted')
    
    for table in tables:
        curs.execute(f"DROP TABLE IF EXISTS {table[0]} CASCADE")
    
    
    create_table()
    


def add_user(user_id):
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
    curs.execute("SELECT * FROM users")
    users = curs.fetchall()
    for user in users:
        print(user)
        
def get_books():
    curs = connect()
    curs.execute("SELECT * FROM books")
    books = curs.fetchall()
    for book in books:
        print(book)
        
def get_tables():
    curs = connect()
    curs.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    tables = curs.fetchall()


    for table in tables:
        print(table)
        
def delete_user(user_id):
    curs = connect()
    
    curs.execute(f"DELETE FROM users WHERE user_id = {user_id}")
    print(f"User with user_id = {user_id} was deleted")
    
    


def add_book(user_id,book_name,book_src):
    curs = connect()
    if curs is not None:
        try:
                curs.execute(f"INSERT INTO books(book_name, book_src, user_id) VALUES ('{book_name}','{book_src}',{user_id})")
                print('BOOK WAS ADDED', book_name)
        except Exception as error:
            print(f"An error occurred when trying to execute the query: {error}")
            return None
    else:
        return None
    
    

#create_table()
#add_book(111,'TestBook','URLTest')
#delete_user(111111)
get_users()
get_books()