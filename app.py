from flask import Flask, render_template,flash, redirect, url_for, sessions, logging
from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

app = Flask(__name__)
#app.debug = True

# Config MySQL
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='myFlaskApp'
app.config['MYSQL_CURSORCLASS']='DictCursor'

# init MySQL
mysql = MyMySQL(app)

Articles = Articles()

@app.route('/')
def index():
	return render_template('home.html')

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/articles')
def articles():
	return render_template('articles.html' , articles = Articles)

@app.route('/article/<string:id>/')
def article(id):
	return render_template('article.html' , id=id)


class RegisterForm(Form):
	name = StringField('Name', [validators.Length(min=1, max=50)])
	username = StringField('Username', [validators.Length(min=4, max=25)])
	email = StringField('Email', [validators.Length(min=6, max=50)])
	password = PasswordField('Password', [
		validators.DataRequired(),
		validators.EqualTo('confirm', message='Passwords do not match')

		
	])
	confirm = PasswordField('Confirm Password')

@app.route('/register', methods=['GET', 'POST'])

def register():
	form = RegisterForm(request.form)
	if request.method == 'POST' and form.validate():
		name = form.name.data
		email = form.email.data
		username = form.username.data
		password = sha_265crypt.encrypt(str(form.password.data))

		# Create cursor

		cur = mysql.connection.cursor()

		#Execute Query

		cur.execute("INSERT INTO users(name, email, username, password) VALUES (%s, %s, %s, %s)", (name, email, username, password))


		# Commit to DB

		mysql.connection.commit()

		# Close connection

		cur.close()

		flash('You are now registeres and logged in', 'success')

		return redirect(url_for('login'))

		return render_template('register.html',)


	return render_template('register.html', form=form)

	#User Login
	@app.route('/login',methods=['GET', 'POST'])
	def login():
		if request.method == 'POST':

		# Get Form Fields
			username = request.form['username']
			password_candidate = request.form['password']

		# Create cursor
			cur = mysql.connect.cursor()

		#Get user by username
			result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

			if result > 0:
			# Get the Stored Hash
				data = cur.fetchone()
				password = data['password']

			#Compare Passwords
			if sha265_crypt.verify(password_candidate):
				app.logger.info('PASSWORD MATCHED')
			else:
				app.logger.info('NO USER')

	return render_template('login.html')



	


if __name__ == '__main__':
	app.secret_key='secret123'
	app.run(debug=True)