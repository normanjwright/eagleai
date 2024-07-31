import psycopg2
import os
import math
import numpy as np
from openai import OpenAI
from pgvector.psycopg2 import register_vector
from courseloadAPI import get_all_courses


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])

# Helper function: get embeddings for a text
def get_embeddings(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input = text.replace("\n"," "))
    embedding = response.data[0].embedding
    return embedding

def get_top_similar_docs(query_embedding, conn):
    embedding_array = np.array(query_embedding)
    # Register pgvector extension
    register_vector(conn)
    cur = conn.cursor()
    # Get the top  most similar documents using the KNN <=> operator
    cur.execute("SELECT description FROM embeddings ORDER BY embedding <=> %s LIMIT 6", (embedding_array,))
    top_docs = cur.fetchall()
    #for class_code in top10_docs:
     #   temp_df = df_temp[df_new["code"] == class_code[0]]
      #  temp = temp_df.iloc[0]
       # if (temp):
        #    print(temp)
         #   print(temp["title"] + "(" + temp["code"] + "): "  + temp["description"])
    return top_docs


def semantic_search(text, courses):
    conn_string = "host='localhost' dbname='CourseEmbeddings' user='newuser' password='password'"
    conn = psycopg2.connect(conn_string)

    print("Database opened successfully")


    #conn = psycopg2.connect(database="postgres", user='newuser', password='password', host="localhost", port=5432)
    #conn = psycopg2.connect(connection_string)
    cur = conn.cursor()

    #install pgvector 
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector");
    conn.commit()

    # Register the vector type with psycopg2
    register_vector(conn)

    # Create table to store embeddings and metadata
    table_create_command = """
    CREATE TABLE IF NOT EXISTS embeddings2 (
                id bigserial primary key, 
                title text,
                code text,
                description text,
                tokens integer,
                embedding vector(1536)
                );
                """

    cur.execute(table_create_command)
    cur.close()
    conn.commit()


    register_vector(conn)
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) as cnt FROM embeddings;")
    num_records = cur.fetchone()[0]
    print("Number of vector records in table: ", num_records,"\n")

    num_lists = num_records / 1000
    if num_lists < 10:
        num_lists = 10
    if num_records > 1000000:
        num_lists = math.sqrt(num_records)

    #use the cosine distance measure, which is what we'll later use for querying
    cur.execute(f'CREATE INDEX ON embeddings2 USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')
    conn.commit() 

    related_docs = get_top_similar_docs(get_embeddings(text), conn)
    found_courses = []
    for course in related_docs:
        found_courses.append(courses[course[0]])
    return found_courses
        


course_list, dept = get_all_courses()
    

semantic_search("Spanish Inquisition", course_list )

