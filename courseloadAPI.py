import requests
import re
class ApiCourse():
    def __init__(self, title, code, course_id, description, credits, program_reqs, prerequisites=""):
        self.title = title
        self.code = code
        self.course_id = course_id
        self.description = description
        try:
            self.credits = int(credits[0][-3])
        except:
            self.credits = 0
        self.prerequisites = prerequisites if prerequisites else "None"
        self.program_reqs = program_reqs



        
def prerequisites_as_string(prereqs):
        output = ""
        if len(prereqs) == 0:
            output = "None"
        elif len(prereqs) == 1:
            
            output = str(prereqs[0][0])
        else:
            for prereq in prereqs:
                output = output + str(prereq[0]) + " and "
            output = output[:-5]

        return output

def corereqs_as_string(corereqs):
        output = ""
        if len(corereqs) == 0:
            output = "None"
        elif len(corereqs) == 1:
            
            output = str(corereqs[0])
        else:
            for req in corereqs:
                output = output + str(req) + " and "
            output = output[:-5]

        return output

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

def get_core_reqs(course):
    reqs = []
    for req in (course['requirements']):
        reqs.append(req['name'])
    return reqs
        

def format_courses(courses):
    formatted = {}
    depts = []
    depts_long = []
    #i = 0
    for course in courses.json():
        prerequisites = None
        prereq_string = None
        if course['course']['levelValueId'] == 'kuali.result.value.course.level.UG' or course['course']['levelValueId'] == 'kuali.result.value.course.level.B':
            if len(course['prereqTerseTranslations']) > 0:
                prerequisites = find_prerequisites(course['prereqTerseTranslations'][0]['translation']['formatted'], course['course']['courseCode'])
                #print(type(prerequisites))
                prereq_string = prerequisites_as_string(prerequisites)
            core_req = corereqs_as_string(get_core_reqs(course))

            desc = course['course']['descr']['plain']
            if ("&#34;" in desc):
                desc = desc.replace('&#34;', '"')
            if ("&#233;" in desc):
                desc = desc.replace('&#233;', 'é')
            if ("&#151" in desc):
                desc = desc.replace('&#151', '-')
            if ("&#252" in desc):
                desc = desc.replace('&#252', 'ü')
            if ("<br>" in desc):
                desc = desc.replace('<br>', '')
                desc = desc.replace('</br>', '')
            if ("</br>" in desc):
                desc = desc.replace('</br>', '')
            if ("<br/>" in desc):
                desc = desc.replace('<br/>', '')
            if ("&#224;" in desc):
                desc = desc.replace('&#224;', 'à')
            if ("<i>" in desc):
                desc = desc.replace('<i>', '')
                desc = desc.replace('</i>', '')
                desc = desc.replace('<i/>', '')
            if ("<I>" in desc):
                desc = desc.replace('<I>', '')
                desc = desc.replace('</I>', '')
            if ("<P>" in desc):
                desc = desc.replace('<P>', '')
                desc = desc.replace('</P>', '')
            if ("<p>" in desc):
                desc = desc.replace('<p>', '')
                desc = desc.replace('</p>', '')
            if ("<BR>" in desc):
                desc = desc.replace('<BR>', '')
                desc = desc.replace('</BR>', '')
            if ("<b>" in desc):
                desc = desc.replace('<b>', '')
                desc = desc.replace('</b>', '') 
            if ("</i>" in desc):
                desc = desc.replace('</i>', '')

            title = course['course']['title']
            if ("<i>" in title):
                title = title.replace('<i>', '')
                title = title.replace('</i>', '')
            if ("<I>" in title):
                title = title.replace('<I>', '')
                title = title.replace('</I>', '')


            formatted.update({str(course['course']['courseCode']): ApiCourse(
                title,
                course['course']['courseCode'],
                course['course']['id'],
                desc,
                course['course']['creditOptionIds'],
                core_req,
                prereq_string
            )})
            dept = str(course['course']['courseCode'][0:4])
            if dept not in depts and (course['course']['levelValueId'] == 'kuali.result.value.course.level.UG' or course['course']['levelValueId'] == 'kuali.result.value.course.level.B') :
                depts.append(dept) 
                temp = dept + ": " + str(course["subjectArea"]["longName"])
                depts_long.append(temp)
    return formatted, depts_long

def get_all_courses():
    courses = []
    try:
        courses = requests.get(f"http://localhost:8080/waitlist/planningcourses")
    except:
        return []
    return format_courses(courses)


