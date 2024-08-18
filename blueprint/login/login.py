from flask import Flask,request,session,render_template,redirect,Blueprint,url_for,g
import db_manager as db
from settings import Settings


LOGIN = Blueprint("login",__name__,template_folder="templates",static_folder="static",static_url_path="/static")

@LOGIN.route("/login",methods=["GET","POST"])
def user_login():
    if request.method == "GET":
        return render_template("logexperment.html")
    elif request.method == "POST":
        username = request.form["username"]
        uid = request.form["UID"]
        Role = request.form["role"]
        ToDo = "login"
        print('$$$$$$$role',Role)
        with db.connect() as conn:
            valid = db.user(conn,username,uid,Role,ToDo)
            print("@"*5,valid)
            ToDo = "search"
            if valid:
                userID = db.user(conn, username, uid, Role , ToDo)[0][0]
                print("*"*7,Role,userID)
                session["userID"] = userID
                session["role"] = Role
                session["user"] = username
        if Role == "admin":
            return redirect(url_for("view._admin"))
        else:
            return redirect(url_for("view.profile"))

@LOGIN.route("/admin",methods=["GET","POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    elif request.method == "POST":
        username = request.form["username"]
        uid = request.form["UID"]
        Role = "admin"
        ToDo = "login"
        with db.connect() as conn:
            valid = db.user(conn,username,uid,Role,ToDo)
            print(valid)
            ToDo = "search"
            if valid:
                userID = db.user(conn, username, uid , Role , ToDo)[0][0]
                session["userID"] = userID
                session["role"] = Role
                session["user"] = username
        return redirect(url_for("view._admin"))

@LOGIN.route("/logout")
def logout():
    if "userID" in session:
        session.pop("userID",None)
        session.pop("role",None)
        session.pop("user",None)
        return redirect(url_for("login.user_login"))
    else:
        return redirect(url_for("login.user_login"))

