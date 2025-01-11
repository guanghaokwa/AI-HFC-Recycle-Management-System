import psycopg2
from config import DB_PARAMS

cat_type_list = ['Metal', 'Plastic', 'Paper'] # Different category type available when user sign up account

HISTORY_INFO_MAX_DISPLAY = 4 # Max No of Most Recent History Info to display in Dashboard

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

def find_history_log(username):
    conn = get_connection()
    curs = conn.cursor()

    user_id = find_userID(username)

    # Fetch History Information and order by latest datetime
    sql_query = 'SELECT hist_id, res_string FROM history WHERE history."user_ID" = %s ORDER BY datetime_created DESC'
    curs.execute(sql_query, (user_id,))

    history_info = curs.fetchall()

    return history_info[0:HISTORY_INFO_MAX_DISPLAY]

def retrieve_dashboard_info(username):
    conn = get_connection()
    curs = conn.cursor()
    
    sql_select = '''
        SELECT acc."username", acc.point, cat."cat_Name", cat.amount 
        FROM account as acc
        INNER JOIN category as cat
        ON acc."user_ID" = cat."user_ID"
        WHERE acc."username" = %s
        '''
    curs.execute(sql_select, (username,))
    result = curs.fetchall()

    return (result, result[0][1])