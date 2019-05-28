from . import db
from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt



class UserProfile(db.Model):

    __tablename__ = 'user_profiles'



    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80))

    last_name = db.Column(db.String(80))

    username = db.Column(db.String(80), unique=True)

    password = db.Column(db.String(255))



    def __init__(self, first_name, last_name, username, password):

        self.first_name = first_name

        self.last_name = last_name

        self.username = username

        self.password = generate_password_hash(password, method='pbkdf2:sha256')



    def is_authenticated(self):
        return True


    def is_active(self):
        return True


    def is_anonymous(self):
        return False



    def get_id(self):
        try:

            return unicode(self.id)  # python 2 support

        except NameError:

            return str(self.id)  # python 3 support



    def __repr__(self):

        return '<User %r>' %  self.username
        

class apData(db.Model):
    __tablename__ = 'app_data'
    
    id                 = db.Column(db.Integer, primary_key=True)
    macaddress         = db.Column(db.String(80))
    distance           = db.Column(db.Float())
    frequency          = db.Column(db.Integer())
    rssi               = db.Column(db.Integer())
    scantime           = db.Column(db.String(80))
    percentage         = db.Column(db.Float(1))
    timestamp          = db.Column(db.DateTime(),default=db.func.current_timestamp())
    
    def __init__(self,macaddress,distance,frequency,percentage,rssi,scantime):

        self.macaddress    = macaddress
        self.distance      = distance
        self.frequency     = frequency
        self.percentage    = percentage
        self.rssi          = rssi
        self.scantime      = scantime

        
class test(db.Model):
    __tablename__ = 'test_dataa'
    
    id                 = db.Column(db.Integer, primary_key=True)
    data                   = db.Column(db.Integer())
    datetime               = db.Column(db.DateTime(),default=db.func.current_timestamp())

    
    def __init__(self,data):

        self.data          = data
       # self.datetime      = db.func.current_timestamp()

class historyData(db.Model):
    __tablename__ = 'history_data'
    
    id                  = db.Column(db.Integer, primary_key=True)
    time                = db.Column(db.String(80))
    xcords              = db.Column(db.Float())
    ycords              = db.Column(db.Float())
    datetime            = db.Column(db.DateTime(),default=db.func.current_timestamp())
    
    def __init__(self,time,xcords,ycords):

        self.time          = time
        self.xcords        = xcords
        self.ycords        = ycords

        
class devices(db.Model):
    __tablename__ = 'user_devices'
        
    id                  = db.Column(db.Integer, primary_key=True)
    devicename          = db.Column(db.String(80))
    macaddress          = db.Column(db.String(80))
    longg              = db.Column(db.Float())
    lat              = db.Column(db.Float())
    
    def __init__(self, macaddress,devicename,lat,longg):

        self.macaddress           = macaddress
        self.devicename           = devicename
        self.longg                = longg
        self.lat                  = lat
    
    
#class Location(db.Model):
#    __tablename__ = 'device_Data'
#    
#    def __init__(self,xcords,ycords,devicestatus,deviceid,datetime):
#
#        self.xcords            = xcords
#        self.ycords            = ycords
#        self.devicestatus      = devicestatus
#        self.deviceid          = deviceid
#        self.datetime          = datetime
#        
#    id                  = db.Column(db.Integer, primary_key=True)
#    xcords              = db.Column(db.String(80))
#    ycords              = db.Column(db.String(80))
#    devicestatus        = db.Column(db.String(80))
#    deviceid            = db.Column(db.Integer)
#    datetime            = db.Column(db.String(80))
#    
#    
#    #