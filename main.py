from eagleai import create_app
from flask import Flask, render_template, url_for, request
from loadclasses import get_all_courses
from searchcourses import search_courses

app = create_app()

courses = get_all_courses()
    
if __name__ == "__main__":
    app.run(debug=True)
    #Turn off when in production