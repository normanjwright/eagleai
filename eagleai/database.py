from flask import request
from eagleai import mongo
import bcrypt

def sign_up_user():
    user = {
        "_id": request.form.get("eagle_id"),
        "firstname": request.form.get("firstname"),
        "lastname": request.form.get("lastname"),
        "school": request.form.get("school", "Unknown School"),
        "major": request.form.get("major", "Undeclared"),
        "minor": request.form.get("minor", "None"),
        "academic_record": request.form.get("academic_record", []),
        "grad_year": request.form.get("grad_year", "Unknown"),
        "add_credit": request.form.get("add_credit", 0),
        "qual_data": request.form.get("qual_data", {})
    }
    
    user['password'] = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
    # mongo.db.profiles.insert_one(user)
