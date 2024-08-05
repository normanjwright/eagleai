import psycopg2
from eagleai.models import createStudent
from psycopg2.extras import execute_values
from courseloadAPI import get_all_courses
# Connect to the database
# Q: should we keep the eagleid as part of the student object or keep a seperate id

def create_table_if_not_exists():
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)

    print("Database opened successfully")


    #conn = psycopg2.connect(database="postgres", user='newuser', password='password', host="localhost", port=5432)
    #conn = psycopg2.connect(connection_string)
    cur = conn.cursor()


    # Create table to store embeddings and metadata
    table_create_command = """
    CREATE TABLE IF NOT EXISTS users (
                id serial primary key, 
                eid serial,
                firstname text,
                lastname text,
                school text,
                major text,
                minor text,
                academic_record text,
                grad_year integer,
                add_credit text,
                qual_data text
                );
                """

    cur.execute(table_create_command)
    cur.close()
    conn.commit()


    cur = conn.cursor()


student = createStudent(12345678, "Owen", "S",\
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

def majors_to_string(majors):
    return

def string_to_majors(str):
    return

def minors_to_string(minors):
    return

def string_to_minors(str):
    return


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


def create_student(student):
    create_table_if_not_exists()
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE eid = %s", student.eid)
    existing_student = cur.fetchone()
    

    if existing_student is None:
        # Insert new student
        cur.execute("""
            INSERT INTO users (eid, firstname, lastname, school, major, minor, 
                    academic_record, grad_year, add_credit, qual_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (student.eid, student.firstname, student.lastname, student.school, 
              majors_to_string(student.major), minors_to_string(student.minor), academic_record_to_string(student.academic_record),
              student.grad_year, student.add_credit, student.qual_data))
        student_id = cur.fetchone()[0]
        conn.commit()
        print(f"Student inserted with ID: {student_id}")
    else:
        print("Student already exists.")

    return


def udpate(student):
    return

def get_student(eagleid):
    student = "object"
    return student