from flask_pymongo import PyMongo
from flask import request
import bcrypt

mongo = PyMongo()

class Student(): #change to person or user when migrated
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

    def sign_up(self):
        user = {
            "_id" : request.form.get("eagle_id"),
            "firstname" : request.form.get("firstname"),
            "lastname" : request.form.get("lastname"),
            "password" : request.form.get("password")
        }

        user['password'] = bcrypt.generate_password_hash(user['password'])
        



    @staticmethod
    def get_from_db(firstname, lastname):
        return mongo.db.profiles.find_one({"firstname": firstname, "lastname": lastname})
    

def createStudent(firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data):
    student = Student(firstname, lastname, school, major, minor, academic_record, grad_year, add_credit, qual_data)
    return student

    
