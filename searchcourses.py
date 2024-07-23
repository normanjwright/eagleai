#helper functions for the search courses page 

def search_courses(courses, search_text, dept, curr_offered, core_req):
    return_courses = []
    for course in courses:
        #Check Dept and core req
        if (dept in courses[course].code[0:4] or dept == "Depa" or dept == "") and (core_req in courses[course].program_reqs or core_req == "Requirement"):
            #check text
            if search_text == "" or search_text.casefold() in str(course.title).casefold() \
                or search_text.casefold() in courses[course].description.casefold() \
                or search_text in courses[course].code:
                return_courses.append(courses[course])
            


    return return_courses


def find_all_departments():
    dept = []

    return dept


def find_all_reqs():
    # Should these be hard coded since they are the main bc cores
    reqs = ["Major Requirements", "Minor Requirements", "Arts", "Cultural Diversity", "History I", "History II",\
            "Literature", "Mathematics", "Natural Science", "Philosophy","Social Science", "Theology", "Writing" ]
    return reqs



def boost_card(course, student):
    chat_response = 'blank'
    return chat_response
