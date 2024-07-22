#helper functions for the search courses page 

def search_courses(courses, search_text, dept, curr_offered, core_req):
    return_courses = []
    for course in courses:
        #Check Dept and core req
        if (dept in course.code[0:4] or dept == "Any") and (core_req in course.program_reqs or core_req == "Any"):
            #check text
            if search_text == "" or search_text.casefold() in course.title.casefold() \
                or search_text.casefold() in course.description.casefold() \
                or search_text in course.code:
                return_courses.append(course)
            


    return return_courses


def find_all_departments():
    dept = []

    return dept


def find_all_reqs():
    # Should these be hard coded since they are the main bc cores
    reqs = ["History I", "History II", "Cultural Diversity",\
             "Mathematics", "Minor Requirements", "Major Requirements", \
                "Social Science", "Natural Science", "Philosophy", "Theology", "Writing",\
                    "Literature", "Arts"  ]
    return reqs



def boost_card(course, student):
    chat_response = 'blank'
    return chat_response
