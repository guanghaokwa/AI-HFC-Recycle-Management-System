import psycopg2
from config import DB_PARAMS

cat_type_list = ['Metal', 'Plastic', 'Paper'] # Different category type available when user sign up account

def get_connection():
    conn = psycopg2.connect(**DB_PARAMS)
    return conn

def find_userID(username):
    conn = get_connection()
    curs = conn.cursor()

    sql_select = 'SELECT * FROM account WHERE username = %s'
    curs.execute(sql_select, (username,))

    user_info = curs.fetchone()
    user_id = user_info[0]

    curs.close()
    conn.close()

    return user_id

def create_user_cat(username): 
    conn = get_connection()
    curs = conn.cursor()
    
    user_id = find_userID(username)

    for type in cat_type_list:
        
        # Create multiple category linked to user with default point of 0
        sql_insert = 'INSERT INTO category ("user_ID", "cat_Name") VALUES (%s, %s);'

        curs.execute(sql_insert, (user_id, type,))
        conn.commit()

    curs.close()
    conn.close()

    return user_id