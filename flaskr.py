import sqlite3
from flask import Flask, request, session, g, redirect, url_for,\
    abort, render_template, flash
import flask_uploads
from flask_uploads import UploadSet,IMAGES
from contextlib import closing
import os

#configuration
DATABASE = '/Users/keith/PycharmProjects/FlaskLearn/sqllite/flaskr.db'
DEBUG = True
SECRET_KEY = 'developmentkey'
USERNAME = 'admin'
PASSWORD = 'default'

#upload Configuration
UPLOADED_PHOTOS_DEST = '/Users/keith/PycharmProjects/FlaskLearn/Photos'



app = Flask(__name__)
app.config.from_object(__name__)
photos = UploadSet('photos',IMAGES)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#上传多个文件
@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method == 'POST':
        for filename in request.files:
            file = request.files[filename]
            file.save(os.path.join(UPLOADED_PHOTOS_DEST,file.filename))
            print(file.filename)
        return "success"

    if request.method == 'GET':
        return render_template('upload.html')




@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g,'db',None)
    if db is not None:
        db.close()
    g.db.close()

@app.route('/')
def show_entries():
    cur = g.db.execute('select title, text from entries order by id desc')
    entries = [dict(title = row[0], text = row[1]) for row in cur.fetchall()]
    return render_template('show_entries.html',entries = entries)


@app.route('/add',methods=['GET','POST'])
def add_entry():
    if request.method=='POST':
        if not session.get('loggin_in'):
            abort(401)
        g.db.execute('insert into entries(title, text) VALUES (?,?)',
                     [request.form['title'],request.form['text']])
        g.db.commit()
        flash('New enty was successfully posted')
        return redirect(url_for('show_entries'))
    if request.method == 'GET':
        return render_template('add_entries.html')


@app.route('/login',methods=['GET','POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username']!=app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password']!=app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['loggin_in'] = True
            flash('Your are logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html',error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in',None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))

if __name__ =="__main__":
    app.run()
