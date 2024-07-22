from openai import OpenAI
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

    student_year = student.grad


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
            Year: {student_year}
            Semester: 1
            School: Morissey College of Arts and Sciences
            Program: Bachelor of Science in Computer Science
            

            ## Student Previous Courses
            -these will be organized by semester and year.

            No previous courses
        
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

