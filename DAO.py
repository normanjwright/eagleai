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
                eid integer,
                firstname text,
                lastname text,
                school text,
                major text,
                minor text,
                academic_record text,
                grad_year text,
                add_credit text,
                qual_data text
                );
                """

    cur.execute(table_create_command)
    cur.close()
    conn.commit()


    cur = conn.cursor()



courses, depts = get_all_courses()

def majors_to_string(majors):
    str = ""
    for major in majors:
        str = str + major + "/"
    str[:-1]
    return str

def string_to_majors(str):
     # Split the string by "/" to get the list of majors
    majors = str.split("/")
    # Remove any empty strings that might occur due to trailing slashes
    majors = [major for major in majors if major]
    return majors

def minors_to_string(minors):
    str = ""
    for minor in minors:
        str = str + minor + "/"
    str[:-1]
    return str

def string_to_minors(str):
     # Split the string by "/" to get the list of majors
    minors = str.split("/")
    # Remove any empty strings that might occur due to trailing slashes
    minors = [minor for minor in minors if minor]
    return minors


def academic_record_to_string(ar):
    str = ""
    for sem in ar:
        str = str + sem + ": "
        for course in ar[sem]:
            str = str + " " + course[0:8]
        str = str + "|"
    return str

def qual_to_string(qual):
    str = ""
    for answer in qual:
        str = str + answer + "||"
    str[:-2]
    return str

def string_to_qual(string):
    # Split the string using the delimiter '||'
    if string == "":
        qual_to_string(["","",""])
    qual_list = string.split('||')
    
    # Remove the last empty string if it exists (due to trailing '||')
    if qual_list[-1] == '':
        qual_list.pop()
    
    return qual_list

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



def create_student_in_db(student):
    create_table_if_not_exists()
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE eid = %s", (student.eid,))
    existing_student = cur.fetchone()

    student_id = 0
    
    if existing_student is None:
        # Insert new student

        cur.execute("""INSERT INTO users (eid, firstname, lastname, school, major, minor, 
                    academic_record, grad_year, add_credit, qual_data)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (student.eid, student.firstname, student.lastname, student.school, 
              majors_to_string(student.major), minors_to_string(student.minor), academic_record_to_string(student.academic_record),
              student.grad_year, student.add_credit, qual_to_string(student.qual_data)))
        student_id = cur.fetchone()[0]
        conn.commit()
        print(f"Student inserted with ID: {student_id}")
    else:
        print("Student already exists.")

    return student_id


def update_student_in_db(student):
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # Check if student exists
    cur.execute("SELECT * FROM users WHERE eid = %s", (student.eid,))
    existing_student = cur.fetchone()

    if existing_student is not None:
        # Update the student's information
        cur.execute("""
            UPDATE users
            SET firstname = %s,
                lastname = %s,
                school = %s,
                major = %s,
                minor = %s,
                academic_record = %s,
                grad_year = %s,
                add_credit = %s,
                qual_data = %s
            WHERE eid = %s
        """, (student.firstname, student.lastname, student.school, 
              majors_to_string(student.major), minors_to_string(student.minor), 
              academic_record_to_string(student.academic_record), student.grad_year, 
              student.add_credit, qual_to_string(student.qual_data), student.eid))
        conn.commit()
        print(f"Student with EID {student.eid} updated.")
    else:
        print("Student not found.")

    cur.close()
    conn.close()

def get_student(eagleid):
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()

    # Fetch the student data
    cur.execute("SELECT eid, firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data FROM users WHERE eid = %s", (eagleid,))
    student_data = cur.fetchone()

    cur.close()
    conn.close()

    if student_data is not None:
        # Unpack the data and create a Student object
        eid, firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data = student_data
        student = createStudent(eid, firstname, lastname, school, string_to_majors(major), string_to_minors(minor), string_to_academic_record(academic_record, courses), grad_year, add_credit, string_to_qual(qual_data))
        print("Student found")
        return student
    else:
        print("Student not found.")
        return None
    


    



# Testing

student = createStudent(12345678, "Owen", "S",\
    "Morissey College of Arts and Science", \
    ["Computer Science", "Music"], ["Finance", "Mathematics"], \
    {"Freshman Summer":[], "Freshman Fall": ["CSCI1101: Computer Science I", "MATH1103: Calculus II (Mathematics/Science Majors)", \
                        "PHYS2200: Introductory Physics I (Calculus)", "SPAN1015: Elementary Spanish I",\
                            "ENGL1110: First Year Writing Seminar: From Slavery to Mass Incarceration"], \
                                "Freshman Spring": [], "Sophomore Summer": [],\
        "Sophomore Fall": [], "Sophomore Spring": [], "Junior Summer": [],\
        "Junior Fall": [], "Junior Spring": [], "Senior Summer": [],\
        "Senior Fall": [], "Senior Spring": []},\
    "Freshman", ["MATH1102: Calculus (Mathematics/Science Majors)"], "")

