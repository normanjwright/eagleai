#anything not related to  authenticaton goes here
#for example the login page will go in auth.py
from flask import Blueprint, render_template, url_for, request, jsonify, session, redirect
from flask_session import Session
from coursesearchAPI import search_courses, find_all_reqs
from courseloadAPI import get_all_courses
from cardboostAPI import boost_card, createStudent
from semanticSearchAPI import semantic_search
from DAO import get_student, udpate_student_in_db, create_student_in_db, create_table_if_not_exists

courses, departments = get_all_courses()
requirements = reqs = ["Major Requirements", "Minor Requirements", "Arts", "Cultural Diversity", "History I", "History II",\
            "Literature", "Mathematics", "Natural Science", "Philosophy","Social Science", "Theology", "Writing" ]

print(departments[0])

# student = createStudent(12345678, "Owen", "S",\
#             "Morissey College of Arts and Science", \
#             ["Computer Science", "Music"], ["Finance", "Mathematics"], \
#             {"Freshman Fall": ["CSCI1101: Computer Science 1", "MATH1120: Calculus 2", \
#                                 "PHYS1101: Introduction to Physics 1", "SPAN1101: Elementary Spanish 1",\
#                                     "ENGL1110: Literature Core"], \
#                                         "Freshman Spring": [], "Freshman Summer": [],\
#                 "Sophomore Fall": [], "Sophomore Spring": [], "Sophomore Summer": [],\
#                 "Junior Fall": [], "Junior Spring": [], "Junior Summer": [],\
#                 "Senior Fall": [], "Senior Spring": [],},\
#             "Freshman", ["MATH1102: Calculus (Mathematics/Science Majors)"], "")


views = Blueprint('views', __name__)

@views.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        if "eid" in request.form:
            eagleID = int(request.form["eid"])
            student = get_student(eagleID)
            session["student"] = student
            return redirect("/profile")
        else:
            print("EagleID not found in form data")
    return render_template("login.html")

@views.route("/logout")
def logout():
    session["student"] = None
    return redirect("/login")

@views.route("/register",  methods=["GET","POST"])
def register():
    if request.method == 'POST':
        create_table_if_not_exists()
        eid = int(request.form["eid"])
        fname = request.form["fname"]
        lname = request.form["lname"]
        school = request.form["school"]
        major1 = request.form["major1"]
        major2 = request.form["major2"]
        minor1 = request.form["minor1"]
        minor2 = request.form["minor2"]
        ar = {"Freshman Fall": [], "Freshman Spring": [], "Freshman Summer": [],\
                 "Sophomore Fall": [], "Sophomore Spring": [], "Sophomore Summer": [],\
                 "Junior Fall": [], "Junior Spring": [], "Junior Summer": [],\
                 "Senior Fall": [], "Senior Spring": []}
        year = request.form["year"]
        add_credit = []
        qual = ""
        major_list = [major1]
        if major2 != "":
            major_list.append(major2)
        minor_list = [minor1]
        if minor2 != "":
            minor_list.append(minor2)
        student = createStudent(eid, fname, lname, school,major_list, minor_list, ar, year, add_credit, qual)
        if get_student(eid) == None:
            create_student_in_db(student)
            session["student"] = student
            return redirect("/profile")
        else:
            student = get_student(eid)
            session["student"] = student
            return redirect("/profile")
    return render_template("register.html")
            



@views.route("/")
def home():
    return render_template("home.html")
    
@views.route("/coursesearch", methods=['GET', 'POST'])
def coursesearch():
    if not session.get("student"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
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

    
    searched_courses, search_text = search_courses(courses, str(search_text), str(search_dept[0:4]) ,offering, search_req, search_cred)
  
    page = request.args.get('page', 1, type=int)
    per_page = 20
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (len(searched_courses) + per_page - 1) // per_page

    items_on_page = searched_courses[start:end]

    #return render_template("coursesearch.html", items_on_page = items_on_page, total_pages = total_pages, page = page , departments=departments, \
    #                       search_text=search_text, search_dept=search_dept, requirements=requirements, \
     #                       search_req=search_req, search_cred=search_cred, num_courses=len(searched_courses))

    return render_template("coursesearch.html", searched_courses = searched_courses , departments=departments, \
                           search_text=search_text, search_dept=search_dept, requirements=requirements, \
                            search_req=search_req, search_cred=search_cred, num_courses=len(searched_courses))



@views.route('/boost', methods=['POST'])
def boost():
    if not session.get("student"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    course_id = request.json['course_id']
    print(courses[course_id].title)
    additional_info = "Baldwin Says:\n      " + str(boost_card(session["student"], courses[course_id]))  # Your function to get additional data
    return jsonify({'additional_info': additional_info})

@views.route("/askbaldwin", methods=['GET', 'POST'])
def askbaldwin():
    if not session.get("student"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    degree = ""
    for major in session["student"].major:
        degree = degree + str(major) + " and "
    for minor in session["student"].minor:
        degree = degree + str(minor) + " and "
    degree = degree[:-5]
    print(degree)

    input_string = "I want a class for my degrees, "+ degree
    if request.method == 'POST':
            input_string = request.form['inputString']


    searched_courses = semantic_search(input_string, courses)
    

    return render_template("askbaldwin.html", searched_courses = searched_courses)

@views.route("/profile")
def profile():
    if not session.get("student"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    studentname = str(session["student"].firstname) + " " + str(session["student"].lastname)
    studentsch = str(session["student"].school)
    studentMaj = session["student"].major
    studentMin= session["student"].minor
    return render_template("profile.html", studentname=studentname, departments=departments, studentsch=studentsch, studentMaj=studentMaj, studentMin= studentMin, student=session["student"])

@views.route("/delete_course", methods=['GET', 'POST'])
def delete_course():
    course = str(request.form.get('course'))


    print(course)
    
    for sem in session["student"].academic_record:
        if course in session["student"].academic_record[sem]:
            print("test")
            session["student"].academic_record[sem].remove(course)
            udpate_student_in_db(session["student"])

        
    return redirect("/profile")



@views.route('/get_courses/<department>', methods=['GET', 'POST'])
def get_courses(department):
    
    profileCourses = []
    for course in courses:
        if (department[0:4] in course):
            profileCourses.append(str(course) + ": " + str(courses[course].title))
    return jsonify(profileCourses)