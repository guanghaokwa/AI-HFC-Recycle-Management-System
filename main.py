import psycopg2
import qrcode
import bcrypt
import os
import random # To replace once correct object type detected from LabelImg
from flask import Flask, render_template, request, redirect, send_file, session, Response
from config import SECRET_KEY, NGROK_TOKEN
from PIL import Image
from pyngrok import ngrok
import requests
import cv2
import io
from werkzeug.datastructures import FileStorage
import json
import time
from util import get_connection, create_user_cat, retrieve_dashboard_info, find_history_log, find_userID, AddPts_WhenLogin, send_image_to_colab

ngrok.set_auth_token(NGROK_TOKEN)
tunnel = ngrok.connect(5000)  # Adjust the port to match your Flask app
ngrok_url = tunnel.public_url  # Get the public URL
print(f"ngrok URL: {ngrok_url}")

app = Flask(__name__)
app.secret_key = SECRET_KEY

QR_IMAGE_PATH = 'static/qr_code.png'

POINT_TO_ADD = 1 # UPDATE field for point to add if user interact wih QR code

temp_data_list = [] # Temporary Storage the image file (data and type)

camera = cv2.VideoCapture(0)

def create_history_log(username, result_string):
    image_data = temp_data_list[0]
    image_type = temp_data_list[1]
    conn = get_connection()
    curs = conn.cursor()

    user_id = find_userID(username)

    sql_insert = 'INSERT INTO history ("user_ID", "res_string", "detect_img_data", "detect_img_type") VALUES (%s, %s, %s, %s);'
    curs.execute(sql_insert, (user_id, result_string, psycopg2.Binary(image_data), image_type))
    conn.commit()

    curs.close()
    conn.close()
    
    del temp_data_list[1]
    del temp_data_list[0]

    return "Successful"

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Convert frame to bytes
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/chatbot')
def chatbot():
     return render_template('chatbot.html')


@app.route('/send', methods=['GET','POST'])
def send_to_colab():
    COLAB_NGROK_URL = "YOUR_NGROK_URL/process"

    if request.method == 'GET':
        return render_template('chatbot.html')
    
    elif request.method == 'POST':
        user_input = request.form.get('prompt')  # Get the input from the form
        if not user_input:
            return render_template("chatbot.html", error="Please provide a prompt.")

        try:
            # Forward the input to Colab
            response = requests.post(COLAB_NGROK_URL, json={"prompt": user_input})
            colab_response = response.json().get("response", "No response from Colab.")
            return render_template("chatbot.html", prompt=user_input, response=colab_response)
        except Exception as e:
            return render_template("chatbot.html", error=f"Error: {str(e)}")

            
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/", methods=['GET', 'POST'])
def index():
    if 'username' in session:
        return redirect('/dashboard')
    
    if request.method == 'GET':
        form_status = 'not yet'
        return render_template('index.html', form_status=form_status)
    
    elif request.method == 'POST':
        # result_string = random.choice(cat_type_list) # To replace the correct object type detected
        # image_file = request.files['image_upload']
        start_time = time.time()
        success, frame = camera.read()

        if success:
            # Encode the frame as JPEG and prepare it as a file-like object
            _, buffer = cv2.imencode('.jpg', frame)
            file_like = io.BytesIO(buffer)
            file_like.name = 'captured_image.jpg'  # Set a name for the file-like object
            
            # Create a FileStorage object for compatibility with Flask's file handling
            file = FileStorage(stream=file_like, filename=file_like.name, content_type='image/jpeg')

            print(f"Time after file storage: {time.time() - start_time:.2f}s")
            # Send the image to the Colab API
            response = send_image_to_colab(file)
            print(f"Time after response received: {time.time() - start_time:.2f}s")

            if response.status_code == 200:
                # Save the processed image locally
                processed_image_path = 'static/processed_image.jpg'

                with open(processed_image_path, 'wb') as f:
                    f.write(response.content)  # Save the image content to a file

                # Retrieve metadata from the headers
                metadata_json = response.headers.get('X-Metadata')
                object_type = ''
                if metadata_json:
                    metadata = json.loads(metadata_json)  # Parse the JSON metadata
                    print("Message:", metadata['message'])
                    print("Highest Detected Item:", metadata['highest_detected_item']['label'])
                    object_type = metadata['highest_detected_item']['label']
                else:
                    print("No metadata found in the response headers.")

                with open(processed_image_path, 'rb') as f:

                    file = FileStorage(stream=f,filename='image.jpg',  content_type='image/jpeg')
                    image_data = file.read()
                    image_type = file.content_type

                    temp_data_list.append(image_data) 
                    temp_data_list.append(image_type)
        
                    # QR Code Data (User will be redirected to this URL when scan)
                    highest_image_detection = object_type
                    qr_data =   f'{ngrok_url}/login?pt_check&type=' + highest_image_detection[0:1].upper() + highest_image_detection[1:]

                    qr = qrcode.QRCode(
                        version=3,
                        error_correction=qrcode.constants.ERROR_CORRECT_H, 
                        box_size=10,
                        border=1,
                    )

                    # Set the image (width, height)
                    logo = Image.open('static/text.png')
                    basewidth = 200
                    wpercent = (basewidth/float(logo.size[0]))
                    hsize = int((float(logo.size[1])*float(wpercent)))
                    logo = logo.resize((basewidth, hsize))

                    qr.add_data(qr_data)
                    qr.make(fit=True)

                    img = qr.make_image(fill='black', back_color='white')

                    # Paste a image in the middle of the QR code
                    pos = ((img.size[0] - logo.size[0]) // 2,(img.size[1] - logo.size[1]) // 2)
                    img.paste(logo, pos)
                    
                    img.save(QR_IMAGE_PATH)

                    res_string = highest_image_detection[0:1].upper() + highest_image_detection[1:]
                    form_status = 'hide'

                    return render_template('index.html', res_string=res_string, form_status=form_status)
            else:
                print(f"Error: Received status code {response.status_code}")

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        return redirect('/dashboard')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_connection()
        curs = conn.cursor()

        sql_query = "SELECT password FROM account WHERE username = %s"
        curs.execute(sql_query, (username,))

        stored_hash_pw = curs.fetchone()

        if stored_hash_pw:
            # Convert database password from hex to bytes
            stored_hash_pw = bytes.fromhex(stored_hash_pw[0])

            # To compare password if matches
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash_pw):
                session['username'] = username

                # Only Add Points if the user interact with QR Code
                if 'pt_check' in request.args and 'type' in request.args:
                    AddPts_WhenLogin(username)
                    create_history_log(username, request.args.get('type'))
    
                cat_info = retrieve_dashboard_info(username)

                history_info = find_history_log(username)
                username = session['username']
                point = cat_info[1]
                cat_info = cat_info[0]

                curs.close()
                conn.close()
                
                return render_template('dashboard.html', username=username, point=point, cat_info=cat_info, history_info=history_info)
            else:
                status = 'Sorry, your password was incorrect. Please try again.'
                return render_template("login.html", status=status)
        else:
            status = 'Sorry, your username is not found. Please try again'
            return render_template("login.html", status=status)
        
    return render_template('login.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if 'username' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        status_list = []

        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['re_password']

        conn = get_connection()
        curs = conn.cursor()

        # Verify that the input username does not exist in database
        sql_query = "SELECT COUNT(username) FROM account WHERE username = %s"
        curs.execute(sql_query, (username,))

        total_user = curs.fetchone()

        if total_user[0] == 1:
            status_list.append('Username is taken')
        
        if password != confirm_password:
            status_list.append('Password is incorrect')
        
        if len(password) < 8:
            status_list.append('Password need at least 8 characters long')
        
        if len(status_list) == 0:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            point = 0
            cat_type = ''

            if 'pt_check' in request.args and 'type' in request.args:
                point = POINT_TO_ADD
                cat_type = request.args.get('type')

            sql_insert = "INSERT INTO account (username, password, point) VALUES (%s, %s, %s);"
            curs.execute(sql_insert, (username, hashed_password.hex(), point,))
            conn.commit()

            create_user_cat(username, cat_type)
            cat_info = retrieve_dashboard_info(username)

            if temp_data_list != []:
                create_history_log(username, cat_type)

            session['username'] = username

            curs.close()
            conn.close()
            
            history_info = find_history_log(username)
            username = session['username']
            point = cat_info[1]
            cat_info = cat_info[0]
            
            return render_template('dashboard.html', username=username, point=point, cat_info=cat_info, history_info=history_info)
        else:
            return render_template('signup.html', status_list=status_list)
    return render_template('signup.html')

@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/login')
    else:
        session.clear()
        return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    if 'username' not in session:
        return redirect('/login')

    cat_info = retrieve_dashboard_info(session['username'])
    history_info = find_history_log(session['username'])

    point = cat_info[1]
    cat_info = cat_info[0]

    return render_template('dashboard.html', username=session['username'], point=point, cat_info=cat_info, history_info=history_info)

@app.route('/image/<int:image_id>')
def get_image(image_id): # To extract the images
    conn = get_connection()
    curs = conn.cursor()

    sql_query = 'SELECT * FROM history WHERE hist_id = %s'
    curs.execute(sql_query, (image_id,))

    history_img = curs.fetchone()

    image_data = history_img[3]
    image_type = history_img[4]

    return Response(image_data, content_type=image_type)

@app.route('/static/qr_code.png')
def qr_code_image():
    return send_file(QR_IMAGE_PATH)

if __name__ == "__main__":
    if not os.path.exists('static'):
        os.makedirs('static')
        
    app.run(port=5000)
