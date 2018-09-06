from flask import *
import os
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = "phil"

conn = sql.connect('mydb.db', check_same_thread =  False)
conn.cursor().execute('CREATE TABLE IF NOT EXISTS clients( username text NOT NULL PRIMARY KEY);')
conn.cursor().execute('CREATE TABLE IF NOT EXISTS todo( id integer PRIMARY KEY, username text NOT NULL, info text, done boolean);')
cor = conn.cursor()

@app.route('/')
def homepage():
	return render_template('index.html')



@app.route('/user/<username>')
def home(username):
	get_column = '''SELECT todo.info FROM todo JOIN clients ON todo.username = clients.username where clients.username = ? and todo.done = ?'''
	todo = cor.execute(get_column, ( username, 0)).fetchall()
	get_column = '''SELECT todo.id FROM todo JOIN clients ON todo.username = clients.username where clients.username = ? and todo.done = ?'''
	get_id = cor.execute(get_column, ( username, 0)).fetchall()
	get_column = '''SELECT todo.info FROM todo JOIN clients ON todo.username = clients.username where clients.username = ? and todo.done = ?'''
	get_uncomplete = cor.execute(get_column, ( username, 1)).fetchall()
	return render_template('profile.html', name = username, data1 = zip(todo, get_id), data2 = get_uncomplete, )




@app.route('/add', methods = ['POST'])
def add():
	#cor = conn.cursor()
	id = len(cor.execute('SELECT id FROM todo').fetchall())
	todo =  '''INSERT INTO todo values(?,?,?,?)'''
	cor.execute(todo, (id, session['login_in'],request.form['needtobedone'],0))
	conn.commit()
	return redirect(url_for('home', username = session['login_in']))



@app.route('/complete/<id>')
def complete(id):
	get_column = '''UPDATE todo SET done = 1 where id = ?'''
	cor.execute(get_column, (id,))
	conn.commit()
	return redirect(url_for('home', username = session['login_in']))




@app.route('/delete/<id>')
def delete(id):
	get_column = '''UPDATE todo SET username = "cry boby cry boby" where id = ?'''
	cor.execute(get_column, (id,))
	conn.commit()
	return redirect(url_for('home', username = session['login_in']))

@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		username = cor.execute('SELECT username from clients').fetchall()
		for index in range(len(username)):
			if request.form['username'] == ''.join(username[index]):
				session['login_in'] = request.form['username']
				return redirect(url_for('home', username = request.form['username']))
		error = "Your username is incorrect!"
	return render_template('login.html', error = error)




@app.route('/register', methods = ['GET', 'POST'])
def register():
	reg = None
	username = cor.execute('SELECT username from clients').fetchall()
	if request.method == 'POST':
		for index in range(len(username)):
			if request.form['regs'] == ''.join(username[index]):
				reg = "Someone with this username has already registered"
				return render_template('signup.html', reg = reg)
	if request.form.get('regs') != None:
		cor.execute('INSERT INTO clients values(?)', (request.form.get('regs'),))
		conn.commit()
		reg = "You successfully registered!"
	return render_template('signup.html', reg = reg)



@app.route('/logout')
def logout():
	session.pop('username', None)
	return redirect(url_for('register'))




def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None


if __name__ == '__main__':
	app.run(debug=True)
