

class Student():
    def __init__(self, firstname, lastname, school, major, minor, academic_record, curr_year, add_credit, qual_data):
        self.firstname = firstname
        self.lastname = lastname
        self.school = school
        self.major = major
        self.minor = minor
        self.academic_record = academic_record
        self.curr_year = curr_year
        self.add_credit = add_credit
        self.qual_data = qual_data

# I have a test case in the boost.py file

def createStudent(fname, lname, school, major, minor, academic_record, curr_year, add_credit, qual_data):
    student = Student(fname, lname, school, major, minor, academic_record, curr_year, add_credit, qual_data)
    return student


    










