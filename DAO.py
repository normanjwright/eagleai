from eagleai.models import createStudent
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
            {"Freshman Fall": ["CSCI1101: Computer Science 1", "MATH1120: Calculus 2", \
                                "PHYS1101: Introduction to Physics 1", "SPAN1101: Elementary Spanish 1",\
                                    "ENGL1110: Literature Core"], \
                                        "Freshman Spring": [], "Freshman Summer": [],\
                "Sophomore Fall": [], "Sophomore Spring": [], "Sophomore Summer": [],\
                "Junior Fall": [], "Junior Spring": [], "Junior Summer": [],\
                "Senior Fall": [], "Senior Spring": [],},\
            "Freshman", ["MATH1102: Calculus (Mathematics/Science Majors)"], "")

def academic_record_to_string(student):
    str = ""
    for sem in student.academic_record:
        str = str + sem + ": "
        for course in student.academic_record[sem]:
            str = str + " " + course[0:8]
        str = str + "|"
    return str

print(academic_record_to_string(student))  
