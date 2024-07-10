import requests
import re
class ApiCourse():
    def __init__(self, title, code, course_id, description, credits, prerequisites=""):
        self.title = title
        self.code = code
        self.course_id = course_id
        self.description = description
        try:
            self.credits = int(credits[0][-3])
        except:
            self.credits = 0
        self.prerequisites = prerequisites if prerequisites else [["None"]]
        

def find_prerequisites(text, course_code):
    # this return a list of lists [[prereq_1], [prereq_2], [prereq_3a, prereq_3b], ...]
    # the inside list with multiple items means the prereq can be satisfied in multiple ways
    pattern = r'[A-Z]{4}\d{4}(?:/[A-Z]{4}\d{4})*'
    code_groups = re.findall(pattern, text)
    codes = [code.split('/') for code in code_groups]
    try:
        codes.remove([course_code])
    except:
        pass
    return codes


def format_courses(courses):
    formatted = []
    i = 0
    for course in courses.json():
        prerequisites = None
        if len(course['prereqTerseTranslations']) > 0:
            prerequisites = find_prerequisites(course['prereqTerseTranslations'][0]['translation']['formatted'], course['course']['courseCode'])
        formatted.append(ApiCourse(
            course['course']['title'],
            course['course']['courseCode'],
            course['course']['id'],
            course['course']['descr']['plain'],
            course['course']['creditOptionIds'],
            prerequisites
        ))
        if (i % 1000 == 0):
            print(str(i) + ": " + course['course']['title'])
        i += 1
    print(i)
    return formatted

def get_all_courses():
    courses = []
    try:
        courses = requests.get(f"http://localhost:8080/waitlist/planningcourses")
    except:
        return []
    return format_courses(courses)


