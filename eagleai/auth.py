from flask import Blueprint, render_template, url_for, request
from eagleai.models import Student
from eagleai.database import sign_up_user
import bcrypt

auth = Blueprint('auth', __name__)


@auth.route("/login", methods=["GET","POST"])
def login():
    # data = request.form.to_dict()
    # print(data)

    if request.method == "POST":
        eagle_id = request.form.get("eagle_id")
        password = request.form.get("password")

        user = profile.get_from_db(eagle_id)

        if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            return render_template("home.html")
        else:
            flash("User does not exist or password is incorrect", category="error")

    return render_template("login.html")

@auth.route("/register", methods=["GET","POST"])
def register():
    data = request.form.to_dict()
    print(data)
    return render_template("register.html")