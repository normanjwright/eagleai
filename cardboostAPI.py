from openai import OpenAI
from eagleai.models import createStudent
from courseloadAPI import get_all_courses
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def get_completion_from_messages(messages, model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature, 
    max_tokens=max_tokens)
    return response.choices[0].message.content

#test

## Define a Prompt for the LLM





def boost_card(student, course):
    delimiter = "```"
    class_name = course.title
    class_code = course.code
    class_desc = course.description
    class_credit = course.credits
    class_prereqs = course.prerequisites

    school = student.school
    majors = student.major
    minors = student.minor
    academic_record = student.academic_record
    curr_year = student.grad_year
    add_credit = student.add_credit
    qual_data = student.qual_data

    # Here we take the list of their majors and turn that into a single string
    major_string = ""
    for major in majors:
        major_string = major_string + major + " and "
    major_string = major_string[:-5]
    
    # Repeat for minors
    minor_string = ""
    for minor in minors:
        minor_string = minor_string + minor + " and "
    minor_string = minor_string[:-5]

    # Here we turn their academic record into a string
    ad_string = ""
    for sem in academic_record:
        if len(academic_record[sem]) > 0:
            temp_str = f"{sem}: "
            for prev_class in academic_record[sem]:
                temp_str = temp_str + f"{prev_class}, "
            temp_str = temp_str[:-2]
            ad_string = ad_string + temp_str + "\n"




    # Set system message to help set appropriate tone and context for model
    system_message = f"""
    You are an academic advisor helping students get feedback on why a class might be a good fit or not. \
    You work with undergraduates at Boston College. \
    You are taking in various information about the student you are speaking with, such as previous classes, programs and year. \
    You respond in an academic and advisory tone. \
    """

    # User Input
    input = f""" 
            ## Output Format
            Please give a couple sentences total, giving final recommendations on whether or not the student in question should take {class_name}.

            ## Task
            Give some feedback to a student who is reading about {class_name}. The feedback does not have to be all positive. You should not suggest a class if the student is missing any prerequisites.
            For prerequisite checking, check each class one at a time and when the prerequisites are mentioned, put the year it was taken, if it was, in parentheses after. 
            The students previous courses will be listed by course code and title. Typically freshman at Boston College take either 1000 or 2000 level courses, and upperclassmen tend to have higher level courses.
            Look at the different classes the student as already taken in the previous courses section below, however do not output this process.

            ## Class in Question
            Title: {class_name}
            Code: {class_code}
            Description: {class_desc}
            Prerequisites: {class_prereqs}
            Credit: {class_credit}



            ## Student Information
            Year: {curr_year}
            School: {school}
            Majors:{major_string}
            Minors: {minor_string}
            

            ## Student Previous Courses
            {ad_string}

        
        """



    # Prepare messages to pass to model
    # We use a delimiter to help the model understand the where the user_input starts and ends

    # {"role": "assistant", "content": assistant_content } 
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{input}{delimiter}"},
    ]
    final_response = get_completion_from_messages(messages)
    return final_response



# Testing part: mocked for me after one semester at BC, no qual data yet

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

#courses, departments = get_all_courses()
#print(boost_card(student, courses["MUSA1100"]))
