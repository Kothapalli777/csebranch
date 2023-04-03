# Store this code in 'app.py' file

from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re,os
from werkzeug.utils import secure_filename
app = Flask(__name__)


app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Reddy@777'
app.config['MYSQL_DB'] = 'testing'
mysql = MySQL(app)
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/notes')
def notes():
    return render_template('notes.html')

@app.route('/2ndyear')
def secound():
    return render_template('secound.html')
             # 

@app.route("/sucess",methods=['GET','POST'])
def upload_file():                                       # This method is used to upload files 
        if request.method == 'POST':
                f = request.files['file']
                print(f.filename)
                #f.save(secure_filename(f.filename))
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                return redirect("/uploader")

@app.route('/adminhome')
def adminhome():
    return render_template('adminhome.html')

@app.route('/wed')
def refrences():
    return render_template('wed.html')


@app.route('/contact')
def contactus():
    return render_template('contact.html')

@app.route('/faculty')
def faculty():
    return render_template('faculty.html')

@app.route('/events')
def events():
    return render_template('events.html')

@app.route('/students')
def students():
    return render_template('students.html')	

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/hodp')
def hodp():
    return render_template('hodp.html')

@app.route('/swathip')
def swathip():
    return render_template('swathip.html')

@app.route('/nagap')
def nagap():
    return render_template('nagap.html')

@app.route('/swapnap')
def swapnap():
    return render_template('swapnap.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/table')
def table():
    return render_template('table.html')


@app.route('/login', methods =['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s AND password = % s', (username, password, ))
		user = cursor.fetchone()
		if user:
			session['loggedin'] = True
			#session['id'] = user['id']
			session['username'] = user['username']
			msg = 'Logged in successfully !'
		return render_template('dashboard.html', msg = msg)
	else:
	    msg = 'Incorrect username / password !'
	    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
	session.pop('loggedin', None)
	session.pop('id', None)
	session.pop('username', None)
	return redirect(url_for('login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM user WHERE username = % s', (username, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', username):
			msg = 'Username must contain only characters and numbers !'
		elif not username or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO user VALUES ( % s, % s, % s)', (username, password, email, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
        
	elif request.method == 'GET':
		msg = 'Please fill out the form !'
	return render_template('register.html', msg = msg)


@app.route("/adminregister",methods=["GET","POST"])
def admin_register():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        secret_key = request.form['secret']
        if secret_key == "12345":
            #hashed_password = pbkdf2_sha256.hash(password)
            cursor = mysql.connection.cursor()
            cursor.execute("INSERT INTO admin(username,email,password,secret_key) VALUES(%s,%s,%s,%s)",(username,email,password,secret_key))
            mysql.connection.commit()
            return redirect(url_for("adminhome"))
        else:
            return render_template("adminregister.html",msg="Invlaid Secret")

    return render_template("adminregister.html")

@app.route('/users')
def users():
    cur = mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM user")
    if resultValue > 0:
        userDetails = cur.fetchall()
        return render_template('users.html',userDetails=userDetails)

if __name__=='__main__':
    app.run(debug=True)

