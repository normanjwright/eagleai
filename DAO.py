from eagleai.models import createStudent
from courseloadAPI import get_all_courses
# Connect to the database
# Q: should we keep the eagleid as part of the student object or keep a seperate id


def insert(student):
    return


def udpate(student):
    return

def get_student(eagleid):
    student = "object"
    return student

student = createStudent("Owen", "S",\
            "Morissey College of Arts and Science", \
            ["Computer Science", "Music"], ["Finance", "Mathematics"], \
            {"Freshman Summer":[], "Freshman Fall": ["CSCI1101: Computer Science I", "MATH1103: Calculus II (Mathematics/Science Majors)", \
                                "PHYS2200: Introductory Physics I (Calculus)", "SPAN1015: Elementary Spanish I",\
                                    "ENGL1110: First Year Writing Seminar: From Slavery to Mass Incarceration"], \
                                        "Freshman Spring": [], "Sophomore Summer": [],\
                "Sophomore Fall": [], "Sophomore Spring": [], "Junior Summer": [],\
                "Junior Fall": [], "Junior Spring": [], "Senior Summer": [],\
                "Senior Fall": [], "Senior Spring": [],},\
            "Freshman", ["MATH1102: Calculus (Mathematics/Science Majors)"], "")

courses, depts = get_all_courses()

def academic_record_to_string(student):
    str = ""
    for sem in student.academic_record:
        str = str + sem + ": "
        for course in student.academic_record[sem]:
            str = str + " " + course[0:8]
        str = str + "|"
    return str

def string_to_academic_record(str, course_list):
    academic_record = {}
    semesters = str.strip('|').split('|')
    
    for semester in semesters:
        # Split each semester into the semester name and its courses
        sem_name, courses_str = semester.split(':')
        
        # Remove leading/trailing whitespace and split courses by spaces
        courses = [course.strip() for course in courses_str.split() if course]
        long_courses = []
        for course in courses:
            long_courses.append(course + ": " + course_list[course].title)
        
        
        # Store the list of courses in the dictionary under the corresponding semester
        academic_record[sem_name.strip()] = long_courses
        
    return academic_record

ar = academic_record_to_string(student)
new_dict = string_to_academic_record(ar, courses)

