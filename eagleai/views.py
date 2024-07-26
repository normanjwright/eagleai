#anything not related to  authenticaton goes here
#for example the login page will go in auth.py
from flask import Blueprint, render_template, url_for, request
from searchcourses import search_courses
from loadclasses import get_all_courses


views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html")
    
@views.route("/coursesearch")
def coursesearch():
    offering = True

    courses = get_all_courses()    

    CSCI_courses = search_courses(courses, "", "MUSA",offering, "" )
    
    return render_template("coursesearch.html", CSCI_courses = CSCI_courses)

@views.route("/askbaldwin")
def askbaldwin():
    return render_template("askbaldwin.html")

@views.route("/profile")
def profile():
    return render_template("profile.html")