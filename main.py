from flask import Flask, render_template,redirect, url_for, request, session
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import hashlib
import time

import mysql.connector
app = Flask(__name__)
app.config['SECRET_KEY'] = 'januar2021'
mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="",
	database="februar2021"
    )
@app.route('/')
@app.route('/index')
def index():
	return render_template('index.html')

@app.route('/register')
def register():

	if "username" in session:
		return render_template("index.html", poruka="Vec ste ulogovani!")
	return render_template("register.html")

@app.route('/registruj', methods=["POST","GET"])
def registruj():
	# return request.form['godina']
	username = request.form["username"]
	email = request.form["email"]
	password = request.form["password"]
	potvrda = request.form["potvrda"]
	godina = request.form["godina"]
	jmbg = request.form["jmbg"]

	if username=="" or email=="" or password=="" or potvrda=="" or godina=="" or jmbg=="":
		return render_template("register.html", poruka="Sva polja moraju biti popununjena")

	if len(jmbg) != 13:
		return render_template("register.html", poruka="JMBG mora imati 13 karaktera")

	if password != potvrda:
		return render_template("register.html", poruka="Lozinka i potvrda se ne podudaraju")

	mc = mydb.cursor()
	mc.execute("SELECT * FROM korisnici WHERE username='"+username+"' ")
	res = mc.fetchall()

	if len(res) != 0:
		return render_template("register.html", poruka="Postoji korisnik sa tim username-om")
	mc.execute("INSERT INTO korisnici VALUES(null, '"+username+"', '"+email+"', '"+password+"', '"+godina+"', '"+jmbg+"')")
	mydb.commit()

	return redirect(url_for("show_all"))

@app.route('/login', methods=["POST", "GET"])
def login():

	if "username" in session:
		return render_template("index.html", poruka="Vec ste ulogovani")
	return render_template("login.html")

@app.route('/uloguj', methods=["POST", "GET"])
def uloguj():

	username = request.form["username"]
	password = request.form["password"]

	mc = mydb.cursor()
	#return "SELECT * FROM korisnici WHERE username='"+username+"' AND password='"+password+"' "
	mc.execute("SELECT * FROM korisnici WHERE username='"+username+"' AND password='"+password+"' ")
	res= mc.fetchall()

	if len(res) == 0:
		return render_template("login.html", poruka="Korisnik ne postoji")
	else:
		session["username"] = username
		return redirect(url_for("show_all"))

@app.route('/logout')
def logout():

	if not "username" in session:
		return redirect(url_for("show_all"))
	else:
		session.pop("username", None)
		return redirect(url_for("login"))

@app.route('/show_all')
def show_all():

	ulogovan = False

	if "username" in session:
		ulogovan = True
	
	mc = mydb.cursor()
	mc.execute("SELECT * FROM korisnici")
	res = mc.fetchall()

	return render_template("show_all.html", korisnici = res, ulogovan = ulogovan)

@app.route('/delete/<username>')
def delete(username):

	if not username in session:
		return redirect(url_for("login"))
	
	mc = mydb.cursor()
	mc.execute("DELETE FROM korisnici WHERE username='"+username+"' ")
	mydb.commit()

	return render_template(url_for("show_all"))

@app.route('/show_year')
def show_year():

	godina = request.form["godina"]

	mc = mydb.cursor()
	mc.execute("SELECT * FROM korisnici WHERE godina='"+godina+"' ")
	res = mc.fetchall()

	return render_template("show_year.html", korisnici = res)

@app.route('/update/<username>')
def update(username):

	if "username" in session:
		return render_template("update.html", poruka="Ulogujte se!")
	return render_template("update.html")

@app.route('/update', methods=["POST", "GET"])
def update1():

	email = request.form["email"]
	password = request.form["password"]
	godina = request.form["godina"]

	mc = mydb.cursor()
	mc.execute("UPDATE korisnici SET email='"+email+"' '"+password+"' '"+godina+"' ")
	mydb.commit()


if __name__ == '__main__':
	app.run(debug=True)