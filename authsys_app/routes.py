import re, secrets
from flask import render_template, request, redirect, flash, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.sql import text
from sqlalchemy import *
from flask_wtf import CSRFProtect
from flask_mail import Message
from authsys_app.celery import send_confirmation_email_task
from authsys_app import app, db, mail
from authsys_app.models import User



csrf = CSRFProtect(app)


def validateMail(email):
    email_pattern = r"^\S+@\S+\.\S+$"
    if not re.match(email_pattern, email):
        flash("Please enter a valid email address", "danger")
        return False
    else:
        flash("", "success")
        return True
    

def validatePasswordMatch(x, y):
    if x != y:
            flash("The passwords must match!", "danger")
            return True
    else:
        flash("")
        return False







@app.route("/", strict_slashes = False)
def index():
    return render_template("index.html")

@app.route("/signup", methods = (["POST", "GET"]), strict_slashes = False)
def register():
    if request.method == "POST":
        req = request.form
        fname = req.get("fname")
        lname = req.get("lname")
        mail = req.get("mail")
        pwd = req.get("pwd")
        cpwd = req.get("cpwd")
        hashedpwd = generate_password_hash(pwd)
        userDetails = db.session.query(User).filter(User.user_email == mail).first()
        if fname != "" and lname != "" and mail != "" and pwd != "":
            if not validateMail(mail):
                return redirect(request.referrer)
            if validatePasswordMatch(pwd, cpwd):
                return redirect(request.referrer)
            if userDetails:
                flash("This email is taken! Use another email instead.", "warning")
                return redirect(request.referrer)
            confirmation_token = secrets.token_urlsafe(32) 
            new_user = User(user_fname = fname, user_lname = lname, user_email = mail, user_password = hashedpwd, confirmation_token = confirmation_token,)         
            db.session.add(new_user)
            db.session.commit()
            userId = new_user.user_id
            session["user"] = userId
            send_confirmation_email_task.apply_async(args=[mail, fname, confirmation_token])
            flash(f"Account created for you, {fname}! Please proceed to LOGIN ", "success")
            return redirect(url_for("login"))
    else:
        flash("")
    return render_template("register.html")

@app.route("/confirm-registration", methods = (["POST", "GET"]), strict_slashes = False)
def confirm():
    user = User.query.filter_by(confirmation_token=token).first()
    if user and not user.confirmed:
        user.confirmed = True
        user.confirmation_token = None
        db.session.commit()
        flash("Your registration has been confirmed. You can now log in.", "success")
        return redirect(url_for("login"))

    elif user.confirmed:
        flash("Your account is already confirmed. Please log in.", "info")
        return redirect(url_for("login"))
    else:
        abort(404)


@app.route("/sign-in", methods = (["POST", "GET"]), strict_slashes = False)
def login():
    if request.method == "POST":
        req = request.form
        mail = req.get("mail")
        pwd = req.get("pwd")
        userDetails = db.session.query(User).filter(User.user_email == mail).first()
        pwdInDb = userDetails.user_password
        pwd_chk = check_password_hash(pwdInDb, pwd)
        if pwd_chk:
            userId = userDetails.user_id
            session["user"] = userId
            flash(f"Welcome back, {userDetails.user_fname}", "success")

        else:
            flash("Incorrect username or password", "danger")
            flash("")
            return redirect(request.referrer)
    else:
        flash("")
        return render_template("login.html")


@app.route("/reset-password", methods = (["POST", "GET"]), strict_slashes = False)
def reset():
    if request.method == "POST":
        req = request.form
        mail = req.get("mail")
        pwd = req.get("pwd")
        cpwd = req.get("cpwd")
        hashedpwd = generate_password_hash(pwd)
        if (validateMail(mail) and validatePasswordMatch(pwd, cpwd)):
            return redirect(request.referrer)
        userDetails = db.session.query(User).filter(User.user_email == mail).first()
        userMail = userDetails.user_email
        if userMail:
            userDetails.user_password = hashedpwd
            db.session.commit()
            flash(f"Your password has been successfully changed, {userDetails.user_fname}", "success")
    else:
        flash("")
        return render_template("reset.html")