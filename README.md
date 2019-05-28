# AndoirdDeviceLocator
Server Side Andoird Device Locator

## Installation
Navigate to the folder with the code you just cloned and setup a virtual environment.
```sh
$ virtualenv venv 
```

Activate the environment source 
```sh
$ source venv/bin/activate 
```
Install the dependencies (Flask,Flask-Login and FlaskMigrate)

```sh
$ pip install -r requirements.txt 
```
#### Setting up your PostgreSQL database 

Firstly make sure PostgreSQL is started 
sudo service postgresql start 

Then connect to PostgreSQL and create a user and a database: 
sudo sudo -u postgres psql create user "lab5"; create database "lab5"; 
Set a password for the user and make them the owner of the lab5 database: 
\password lab5 alter database lab5 owner to lab5; 
You can now quit the PostgreSQL command prompt by using: 
\q

