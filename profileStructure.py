

class Student():
    def __init__(self, firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data):
        self.firstname = firstname
        self.lastname = lastname
        self.school = school
        self.major = major
        self.minor = minor
        self.academic_record = academic_record
        self.grad_year = grad_year
        self.add_credit = add_credit
        self.qual_data = qual_data

def createStudent(firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data):
    student = Student(firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data)
    return student





