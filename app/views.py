"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm
from app.models import UserProfile,test,apData
from pprint import pprint
from werkzeug.datastructures import ImmutableMultiDict
import json
import ast
import math
from datetime import datetime
###
# Routing for your application.
###
data = '1111'

@app.route('/')
@login_required
def home():   

    latlong = (db.engine.execute('SELECT u.lat,u.longg FROM user_devices u WHERE u.macaddress = (SELECT DISTINCT macaddress FROM app_data  WHERE distance = (SELECT MIN(distance) FROM app_data));')).fetchall()
    
   
    
    
    percentage2 = (db.engine.execute('Select percentage,frequency,distance FROM app_data WHERE timestamp = (select max(timestamp)from app_data);')).first()
    #percentage2 = (db.engine.execute('Select percentage,frequency,distance FROM app_data ;')).first()
    percentage = (db.engine.execute('Select * FROM test_dataa WHERE datetime = (select max(datetime)from test_dataa);')).fetchall()
    # dbm = dbmcalc(percentage[0][0])#its 
    dbm = dbmcalc(percentage2[0])#its 
    # freq = (db.engine.execute('Select * FROM test_dataa WHERE datetime = (select max(datetime)from test_dataa);')).fetchall()
    dd= dist(percentage2[1],dbm)
    
    avgdistance = (float(dd)+percentage2[2])/2
    print type(percentage2[2])
    print type(dd)
    return render_template('home.html',data=latlong[0],lat=latlong[0][1],longg=latlong[0][0],dbm=percentage2,dist=dd,dist2=percentage2[2],avg=percentage2[2])
    # return render_template('home.html')

@app.route("/pingdevice")
#@login_required
def ping():
    return render_template('home.html')
    
    
@app.route("/about")
def about():
    return render_template('devicelocator.html')

#def calculatedistance():
    # data = apData.query.filter_by(username=username).first()
    
    
    
#dbm goes in rssi

    
    
  
  

@app.route("/api/data", methods=["POST","GET"])
def acceptClientData():
 
    clientData         = request.form 

    scantimeData = clientData.get('scantime')
    data         = ast.literal_eval(clientData.get('data')) 

    for scan in data:
       macData                = scan['mac']
       distanceData           = float(scan['distance'])
       frequencyData          = int(scan['frequency'])
       rssiData               = int(scan['rssi'])
       percentageData         = float(scan['percentage'])
       
       print macData
       print distanceData
       print frequencyData
       print rssiData
       
      
       dbrow = apData(macaddress = macData,distance = distanceData,frequency = frequencyData,percentage=percentageData,rssi = rssiData,scantime = scantimeData)
       db.session.add(dbrow)
       db.session.commit()
    return("data received ")
     
   
@app.route('/login', methods=['GET', 'POST'])

def login():

    if current_user.is_authenticated:


        return redirect(url_for('home'))
    form = LoginForm()

    # Login and validate the user.

    if request.method == 'POST' and form.validate_on_submit():

        username = form.username.data

        password = form.password.data

        user = UserProfile.query.filter_by(username=username, password=password).first()

        if user is not None :
            remember_me = False

            if 'remember_me' in request.form:

                remember_me = True

            login_user(user, remember=remember_me)



            flash('Logged in successfully.', 'success')



            next_page = request.args.get('next')

            return redirect(next_page or url_for('home'))

        else:

            flash('Username or Password is incorrect.', 'danger')

    return render_template('login.html', form=form)  



@app.route("/logout")
@login_required

def logout():

    logout_user()

    flash('You have been logged out.', 'danger')

    return redirect(url_for('home'))

@app.route('/secure-page')

@login_required

def secure_page():

    """Render a secure page on our website that only logged in users can access."""

    return render_template('secure_page.html')



@login_manager.user_loader

def load_user(id):

    return UserProfile.query.get(int(id))


###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


def dbmcalc(quality):
    if type(quality)==str:
        print(quality)
        quality=float(quality.replace('%',''))
    dbm=(139.86-quality)*(58/79)
    print(dbm)
    if quality>=95:
        dbm+=1
    elif dbm>=90:
        dbm+=6
    elif dbm<=30:
        dbm+=16
    return dbm


def dist(freq,RSSI):
    exp=(27.55-(20*math.log10(freq)-math.fabs(RSSI)))/20.0
    distance= math.pow(10.0,exp)
    distance=str(round(distance,3))
    return distance


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
