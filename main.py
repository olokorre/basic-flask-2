from flask import Flask, render_template, request, redirect, make_response
import mysql.connector

app = Flask(__name__)

class data_base(object):
    def __init__(self, user, passwd):
        self.mydb = mysql.connector.connect(user = user, passwd = passwd)
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute('use saulo')
    
    def register_user(self, nick, passwd):
        self.mycursor.execute('insert into users (nick, passwd) values ("%s", "%s")' %(nick, passwd))
        self.mydb.commit()
    
    def logon_user(self, nick, passwd):
        self.mycursor.execute('select * from users')
        list_of_users = []
        list_of_passwd = []
        for i in self.mycursor:
            list_of_users.append(i[0])
            list_of_passwd.append(i[1])
        for i in range(len(list_of_users)):
            if nick == list_of_users[i] and passwd == list_of_passwd[i]: return True
        return False

db = data_base('olokorre', 'Linux@290')

@app.route('/', methods = ('GET', 'POST'))
def index():
    nick = request.cookies.get('nick')
    if nick == None or nick == 'None': return redirect('/register')
    return render_template('index.html', nick = nick)

@app.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'GET':
        resp = make_response(render_template('login.html'))
        resp.set_cookie('nick', 'None')
        return resp
    else:
        nick = request.form['nick']
        passwd = request.form['passwd']
        if db.logon_user(nick, passwd):
            resp = make_response(redirect('/'))
            resp.set_cookie('nick', nick)
            return resp
        return '<div align="center"><h1>VOCÊ NÃO EXISTE!</h1><div>'

@app.route('/register', methods = ('GET', 'POST'))
def register():
    if request.method == 'GET':
        resp = make_response(render_template('register.html'))
        resp.set_cookie('nick', 'None')
        return resp
    else:
        nick = request.form['nick']
        passwd = request.form['passwd']
        db.register_user(nick, passwd)
        resp = make_response(redirect('/'))
        resp.set_cookie('nick', nick)
        return resp

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')