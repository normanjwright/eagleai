from openai import OpenAI
import os

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def get_completion_from_messages(messages, model="gpt-3.5-turbo-0613", temperature=0, max_tokens=1000):
    response = client.chat.completions.create(model=model,
    messages=messages,
    temperature=temperature, 
    max_tokens=max_tokens)
    return response.choices[0].message.content



## Define a Prompt for the LLM
'''
class_name = "Algorithms"
class_code = "CSCI3383"
class_desc = "This course is a study of algorithms for, among other things, sorting, searching, pattern matching, and manipulation of graphs and trees. Emphasis is placed on the mathematical analysis of the time and memory requirements of such algorithms and on general techniques for improving their performance."
class_credit = 3
class_prereqs = "CSCI2243(Logic and Computation) and CSCI1102 and CSCI2244(Randomness and Computation)"

'''
class_name = "Computer Science 2"
class_code = "CSCI1102"
class_desc = "In this course, the student will write programs that employ more sophisticated and efficient means of representing and manipulating information. Part of the course is devoted to a continued study of programming. The principal emphasis, however, is on the study of the fundamental data structures of computer science (lists, stacks, queues, trees, etc.). Both their abstract properties and their implementations in computer programs and the study of the fundamental algorithms for manipulating these structures. Students will use Java for programming."
class_credit = 3
class_prereqs = "CSCI1101"




# User Input
input = f""" 
            Give some feedback to a student who is reading about {class_name}. The feedback does not have to be all positive. You should not suggest a class if the student is missing any prerequisites.
            For prerequisite checking, check each class one at a time and when the prerequisites are mentioned, put the year it was taken, if it was, in parentheses after. 
            The students previous courses will be listed by course code and title. Typically freshman at Boston College take either 1000 or 2000 level courses, and upperclassmen tend to have higher level courses.
            Look at the different classes the student as already taken in the previous courses section below. 

            ## Class in Question
            Title: {class_name}
            Code: {class_code}
            Description: {class_desc}
            Prerequisites: {class_prereqs}
            Credit: {class_credit}

            ## Student Information
            Year: Freshman
            Semester: 2
            School: Morissey College of Arts and Sciences
            Program: Bachelor of Science in Computer Science
            

            ## Student Previous Courses
            -these will be organized by semester and year.
            
            Year: Freshman
            Semester: 1
            Classes: (CSCI1101, Computer Science), (MATH1120, Calculus 2), (PHYS1101, Intro to Physics 1), (SPAN1101, Elementary Spanish 1), (ENGL1110, Literature Core)

            
            ## Output Format
            Explain your thinking throughout the process of analyzing the classes fit, such as prerequisite checking, etc. Once you are ready to output a summary of your thoughts, put a title: Feedback for {class_name}. Follow this by a short paragraph with the final advice. 


            


        





        """

# Function to process input with retrieval of most similar documents from the database
def process_input_with_retrieval(user_input):
    delimiter = "```"

    #Step 1: Get documents related to the user input from database

    # Step 2: Get completion from OpenAI API
    # Set system message to help set appropriate tone and context for model

    # TODO: HERE IS WHERE WE PUT REQUIREMENTS
    system_message = f"""
    You are an academic advisor helping students get feedback on why a class might be a good fit or not. \
    You work with undergraduates at Boston College. \
    You are taking in various information about the student you are speaking with, such as previous classes, programs and year. \
    You respond in an academic and advisory tone. \
    """

    assistant_content = """


"""
        #Setup a couple chats so we know what a good and bad response

    # Prepare messages to pass to model
    # We use a delimiter to help the model understand the where the user_input starts and ends

    # {"role": "assistant", "content": assistant_content } 
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": f"{delimiter}{user_input}{delimiter}"},
    ]

    final_response = get_completion_from_messages(messages)
    return final_response


response = process_input_with_retrieval(input)
print(" \n")

#print(input)
print(response)