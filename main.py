import bcrypt
from flask import Flask, render_template, request, session, redirect, Response
from config import SECRET_KEY 
from util import get_connection, create_user_cat, retrieve_dashboard_info, find_history_log

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

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
                
                cat_info = retrieve_dashboard_info(username)

                history_info = find_history_log(username)
                username = session['username']
                point = cat_info[1]
                cat_info = cat_info[0] 

                curs.close()
                conn.close()
                
                return render_template('dashboard.html', username=username, point=point, cat_info=cat_info, history_info=history_info)
            else:
                status = 'Password Incorrect'
                return render_template("login.html", status=status)
        else:
            status = 'Username not found'
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

            sql_insert = "INSERT INTO account (username, password) VALUES (%s, %s);"
            curs.execute(sql_insert, (username, hashed_password.hex(),))
            conn.commit()

            create_user_cat(username)
            cat_info = retrieve_dashboard_info(username)

            session['username'] = username

            curs.close()
            conn.close()

            username = session['username']
            
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

if __name__ == "__main__":
    app.run(port=5000)
