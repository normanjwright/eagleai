from flask import Flask, render_template, url_for, request
from loadclasses import get_all_courses
from searchcourses import search_courses, find_all_reqs

app = Flask(__name__)

@app.route("/", )
def home():
    return render_template("home.html")
    
@app.route("/coursesearch", methods=['GET', 'POST'])
def coursesearch():
    offering = True
    search_text = ""
    search_dept = "Department"
    search_req = "Requirement"
    search_cred = "Credit"

    if request.method == 'POST':
            search_text = request.form['searchText']
            search_dept = request.form['searchDept']
            search_req = request.form['searchReq']
            search_cred = request.form['searchCredit']

    
    searched_courses = search_courses(courses, str(search_text), str(search_dept[0:4]) ,offering, search_req, search_cred)
  
    return render_template("coursesearch.html", searched_courses = searched_courses , departments=departments, \
                           search_text=search_text, search_dept=search_dept, requirements=requirements, search_req=search_req, search_cred=search_cred)

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

courses, departments = get_all_courses()
requirements = reqs = ["Major Requirements", "Minor Requirements", "Arts", "Cultural Diversity", "History I", "History II",\
            "Literature", "Mathematics", "Natural Science", "Philosophy","Social Science", "Theology", "Writing" ]

print(departments[0])



    
if __name__ == "__main__":
    app.run(debug=True)