from flask import Flask,render_template,request,session,g,url_for,redirect

from sense_emu import SenseHat

import random

s=SenseHat()

s.clear(0,0,0) #katharismos otan ektelw to arxeio

green=[0,200,0]
black=[0,0,0]
shipmap=[green]*10+[black]*54
random.shuffle(shipmap)


users= []

users.append([1, 'Giannis','kodikos_Gianni'])
users.append([2, 'Maria','kodikos_Marias'])


app = Flask(__name__)
app.secret_key = "Μυστικό_Κλειδί_Κρυπτογράφησης"

@app.route('/naumaxia',methods=['POST'])
def set_pixel():
    if not g.user:
        return redirect(url_for('logme'))

    if request.method=='POST':

        while True:
           try:
               X = int(request.form['x'])
               Y = int(request.form['y'])

               if X>7 or Y>7:
                  random.shuffle(shipmap)
                  s.set_pixels(shipmap)
                  return render_template('ships.html')
               break;
           except ValueError:
               s.clear(0,0,0)
               s.show_message("lathos timi")
               return render_template('ships.html')

        s.set_pixel(X,Y,[0,0,200])
    return render_template('ships.html')

@app.before_request
def before_request():
    g.user=None

    if 'user_id' in session:

        for user in users:
            if user[0] == session['user_id']:

                g.user = user
                g.s=s


@app.route('/')
def hello_world():
    return 'Γεια σου κόσμε!'


@app.route('/logme', methods=['POST','GET'])
def logme():

    session.pop('user_id', None)

    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:

            if user[1]==username and user[2]==password:

                session['user_id'] = user[0]
                return redirect(url_for('arxikh_selida'))
    return render_template('login.html')

@app.route('/arxikh',methods=['POST','GET'])
def arxikh_selida():
    if not g.user:
        return redirect(url_for('logme'))

    return render_template('index.html')

@app.route('/naumaxia',methods=['POST','GET'])
def naumaxia():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('ships.html')

@app.route('/sense', methods=['POST','GET'])
def sense_data():
    if not g.user:
        return redirect(url_for('logme'))
    return render_template('info.html')

@app.context_processor

def a_processor():
    def roundv(value,digits):
        return round(value,digits)
    return {'roundv':roundv}


if __name__ == '__main__' :
    app.run(debug=False,host='0.0.0.0')

