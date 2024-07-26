from eagleai import create_app
from flask import Flask, render_template, url_for, request
from loadclasses import get_all_courses
from searchcourses import search_courses
from boost import createStudent

app = create_app()

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
    
if __name__ == "__main__":
    app.run(debug=True)
    #Turn off when in production