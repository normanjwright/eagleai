#anything not related to  authenticaton goes here
#for example the login page will go in auth.py
from flask import Blueprint, render_template, url_for, request, jsonify
from coursesearchAPI import search_courses, find_all_reqs
from courseloadAPI import get_all_courses
from cardboostAPI import boost_card, createStudent

courses, departments = get_all_courses()
requirements = reqs = ["Major Requirements", "Minor Requirements", "Arts", "Cultural Diversity", "History I", "History II",\
            "Literature", "Mathematics", "Natural Science", "Philosophy","Social Science", "Theology", "Writing" ]

print(departments[0])

student = createStudent("Owen", "S",\
            "Morissey College of Arts and Science", \
            ["Computer Science", "Music"], ["Finance", "Mathematics"], \
            {"Freshman Fall": ["CSCI1101: Computer Science 1", "MATH1120: Calculus 2", \
                                "PHYS1101: Introduction to Physics 1", "SPAN1101: Elementary Spanish 1",\
                                    "ENGL1110: Literature Core"], \
                                        "Freshman Spring": [], "Freshman Summer": [],\
                "Sophomore Fall": [], "Sophomore Spring": [], "Sophomore Summer": [],\
                "Junior Fall": [], "Junior Spring": [], "Junior Summer": [],\
                "Senior Fall": [], "Senior Spring": [],},\
            "Freshman", ["MATH1102: Calculus (Mathematics/Science Majors)"], "")


views = Blueprint('views', __name__)

@views.route("/")
def home():
    return render_template("home.html")
    
@views.route("/coursesearch", methods=['GET', 'POST'])
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
    course_id = request.json['course_id']
    print(courses[course_id].title)
    additional_info = "Baldwin Says:\n      " + str(boost_card(student, courses[course_id]))  # Your function to get additional data
    return jsonify({'additional_info': additional_info})

@views.route("/askbaldwin")
def askbaldwin():
    offering = True
    search_text = ""
    search_dept = "Department"
    search_req = "Requirement"
    search_cred = "Credit"
    searched_courses, search_text = search_courses(courses, str(search_text), str(search_dept[0:4]), offering, search_req, search_cred)
    searched_courses = searched_courses[:6]

    

    return render_template("askbaldwin.html", searched_courses = searched_courses)

@views.route("/profile")
def profile():
    studentname = str(student.firstname) + " " + str(student.lastname)
    return render_template("profile.html", studentname=studentname, departments=departments)


@views.route('/get_courses/<department>', methods=['GET'])
def get_courses(department):
    profileCourses = []
    for course in courses:
        if (department[0:4] in course):
            profileCourses.append(str(course) + ": " + str(courses[course].title))
    return jsonify(profileCourses)