from config import DB_PARAMS
import psycopg2
import qrcode
import bcrypt
import os
import random # To replace once correct object type detected from LabelImg
from flask import Flask, render_template, request, redirect, send_file, session, Response
from config import SECRET_KEY
from PIL import Image
from pyngrok import ngrok
import requests
import cv2
import io
from werkzeug.datastructures import FileStorage
import json
import time

cat_type_list = ['Metal', 'Plastic', 'Paper'] # Different category type available when user sign up account

HISTORY_INFO_MAX_DISPLAY = 4 # Max No of Most Recent History Info to display in Dashboard

POINT_TO_ADD = 1 # UPDATE field for point to add if user interact wih QR code

def send_image_to_colab(file):
    # Replace with the actual public URL from Colab
    colab_url = "https://b482-104-196-70-150.ngrok-free.app/predict"  # Replace with the actual Ngrok URL from Colab
    files = {'file': file}
    response = requests.post(colab_url, files=files)
    return response


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

def create_user_cat(username, cat_type): 
    conn = get_connection()
    curs = conn.cursor()
    
    user_id = find_userID(username)

    for type in cat_type_list:

        if type == cat_type:
            # Create that category linked to the user with 1 point to add
            sql_insert = 'INSERT INTO category ("user_ID", "cat_Name", amount) VALUES (%s, %s, %s);'

            curs.execute(sql_insert, (user_id, type, POINT_TO_ADD,))
            conn.commit()
        else:
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

def AddPts_WhenLogin(username):
    point = POINT_TO_ADD
    type = request.args.get('type')        

    conn = get_connection()
    curs = conn.cursor()

    user_id = find_userID(username)

    # Update user total point by 1
    sql_update = "UPDATE account SET point = point + %s WHERE username = %s"
    curs.execute(sql_update, (point, username))
    conn.commit()

    # Update user total point for that category by 1
    sql_update2 = 'UPDATE category SET amount = amount + %s WHERE "user_ID" = %s AND "cat_Name" = %s'
    curs.execute(sql_update2, (point, user_id, type, ))
    conn.commit()

    curs.close()
    conn.close()

    return 'Successful Updated'
