#helper functions for the search courses page 

def search_courses(courses, search_text, dept, curr_offered, core_req, search_credit):
    return_courses = []
    secondary_courses = []
    for course in courses:
        #Check Dept and core req
        if (dept in courses[course].code[0:4] or dept == "Depa" or dept == "") and (core_req in courses[course].program_reqs or core_req == "Requirement") \
            and (search_credit == "Credit" or search_credit == str(courses[course].credits) or courses[course].credits >= 5) and (courses[course].credits > 0):
            #check text
            if search_text == "" or search_text.casefold() in str(courses[course].title).casefold() \
                or search_text in courses[course].code:
                return_courses.append(courses[course])
            elif search_text.casefold() in courses[course].description.casefold():
                secondary_courses.append(courses[course])
    
    return_courses = return_courses + secondary_courses
    
    if len(return_courses) == 0:
        return_courses, search_text = search_courses(courses, search_text[:-1], dept, curr_offered, core_req, search_credit)
            


    return return_courses, search_text


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
