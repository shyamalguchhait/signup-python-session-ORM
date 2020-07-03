from flask import Flask,render_template,request,session
from flask_session import sessions
import os
SECRET_KEY=os.urandom(24)
import mysql.connector

app=Flask(__name__)
app.config["SECRET_KEY"]=SECRET_KEY

imDB=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="login"
)
db=imDB.cursor()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="GET":
        error="ONLY post method are allow"
        return render_template("error.html",error=error)
    session['username']=request.form.get("username")
    session['password']=request.form.get("password")
    error="If u don't have account sign up"
    log="login"
    sql="SELECT * FROM login WHERE username=%s AND password =%s"
    username=session['username']
    password=session['password']
    value=(username,password)
    db.execute(sql,value)
    user =db.fetchone() 
    if user is None:
        return render_template("error.html", error=error)
    
    else:
        return render_template("success.html", log=log)

@app.route("/account")
def account():
    return render_template("signup.html")

@app.route("/signup",methods=["POST"])
def signup():
    session['name']=request.form.get("name")
    session['username']=request.form.get("username")
    session['email']=request.form.get("email")
    session['phone']=request.form.get("phone_no")
    session['password_1']=request.form.get("password_0")
    session['password_2']=request.form.get("password_1")
    log="Signup"
    sql="SELECT * FROM login WHERE username=%s"
    name=session['name']
    username=session["username"]
    email=session['email']
    phone=session['phone']
    password_1=session['password_1']
    password_2=session["password_2"]
    value=(username,)
    db.execute(sql,value)
    user=db.fetchone()

    if user is None:
        if password_1==password_2:
            sql="INSERT INTO login(name,username,email,phone_no,password) VALUES(%s,%s,%s,%s,%s)"
            value=(name,username,email,phone,password_2)
            db.execute(sql,value)
            imDB.commit()
            return render_template("success.html",log=log)
        else:
            ret="Two pass word are not equal"
            return render_template("signup.html",ret=ret)
    else:
        ret="This user name is already exist"
        return render_template("signup.html",ret=ret)

@app.route("/profile")
def profile():
    sql="SELECT * FROM login WHERE username=%s"
    username=session['username']
    value=(username,)
    db.execute(sql,value)
    username=db.fetchone() 
    if 'username' in session:
        username=session['username']
        return render_template("profile.html",username=username)


@app.route("/logout")
def logout():
    error="error logout"
    if "username" in session:
        session.pop('username',None)
        return render_template("logout.html")
    else:
        return render_template("error.html",error=error)



    