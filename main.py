import bcrypt
from flask import Flask, render_template, request, session, redirect
from config import SECRET_KEY 
from util import get_connection, create_user_cat

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route('/')
def index():
    return render_template('index.html')

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

            session['username'] = username

            curs.close()
            conn.close()

            username = session['username']
            
            return render_template('dashboard.html', username=username)
        else:
            return render_template('signup.html', status_list=status_list)
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/')
    
    username = session['username']
    return render_template('dashboard.html', username=username)

if __name__ == "__main__":
    app.run(port=5000)
