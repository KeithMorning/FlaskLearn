from flask import Flask,url_for,render_template,request

app = Flask(__name__)

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name = None):
    return render_template('hello.html',name=name)

@app.route('/login',methods=['POST','GET'])
def login():
    error = None
    if request.method == 'POST':
        name = request.form['username']
        passowrd = request.form['password']
        return 'hello ' + name +' you have come in'

    return render_template('login.html',error = error)

@app.route('/goto/<name>')
def goto(name):
    try:
        gugu = request.args.get('sex')
        age = request.args.get('age')
        return name + ' is a '+gugu+' '+'age is '+age
    except Exception as e:
        return str(e)



if __name__ == '__main__':
    app.run()

