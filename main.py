from flask import Flask, render_template, url_for, request
from loadclasses import get_all_courses
from searchcourses import search_courses

app = Flask(__name__)

@app.route("/", )
def home():
    return render_template("home.html")
    
@app.route("/coursesearch")
def coursesearch():
    offering = True
    CSCI_courses = search_courses(courses, "", "AADS",offering, "Cultural Diversity" )
    
    

    #for course in courses:
    #    if course.code[0:4] == "CSCI" and course.credits > 0:
    #        CSCI_courses.append(course)
        
    
    return render_template("coursesearch.html", CSCI_courses = CSCI_courses)

@app.route("/askbaldwin")
def askbaldwin():
    return render_template("askbaldwin.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")

@app.route("/login")
def login():
    return render_template("login.html")

# Here we reference the function in load classes, 
# where courses is a list of objects of the type ApiCourse which is also defined there

courses = get_all_courses()



    
if __name__ == "__main__":
    app.run(debug=True)