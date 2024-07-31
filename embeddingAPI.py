import csv
import os
import tiktoken
import pandas as pd
import numpy as np
import psycopg2
import ast
import pgvector
import math
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from courseloadAPI import get_all_courses
from openai import OpenAI



client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def courses_to_csv():
    count = 0
    with open('courses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        courses, departments = get_all_courses()
        writer.writerow(["title", "code", "description"])
        for course in courses:
            writer.writerow([str(courses[course].title), 
                            str(courses[course].code),
                                str(courses[course].description)])

            if (count % 200) == 0:
                print("Course Added: " + courses[course].title)
            count += 1


# Helper function: get embeddings for a text
def get_embeddings(text):
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input = text.replace("\n"," "))
    embedding = response.data[0].embedding
    return embedding

def get_essay_length(essay):
    word_list = essay.split()
    num_words = len(word_list)
    return num_words

def num_tokens_from_string(string: str, encoding_name = "cl100k_base") -> int:
    if not string:
        return 0
    # Returns the number of tokens in a text string
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# Helper function: calculate cost of embedding num_tokens
# Assumes we're using the text-embedding-ada-002 model
# See https://openai.com/pricing
def get_embedding_cost(num_tokens):
    return num_tokens/1000*0.0001

def get_total_embeddings_cost(df):
    total_tokens = 0
    for i in range(len(df.index)):
        text = str(df['title'][i]) + "(" + str(df['code'][i]) + "): " + str(df['description'][i])
        token_len = num_tokens_from_string(text)
        total_tokens = total_tokens + token_len
    total_cost = get_embedding_cost(total_tokens)
    return total_cost

def embed_courses_to_csv():
    df = pd.read_csv('courses.csv')
    df.head()

    new_list = []

    print('Chunk Text')
    for i in range(len(df.index)):
        text = str(df['title'][i]) + "(" + str(df['code'][i]) + "): " + str(df['description'][i])
        token_len = num_tokens_from_string(text)
        if token_len <= 512:
            new_list.append([df['title'][i], df['description'][i], df['code'][i], token_len])
        else:
            print("test check" + str(df['title'][i]))
            # add content to the new list in chunks
            start = 0
            ideal_token_size = 512
            # 1 token ~ 3/4 of a word
            ideal_size = int(ideal_token_size // (4/3))
            end = ideal_size
            #split text by spaces into words
            words = text.split()

            #remove empty spaces
            words = [x for x in words if x != ' ']

            total_words = len(words)

            #calculate iterations
            chunks = total_words // ideal_size
            if total_words % ideal_size != 0:
                chunks += 1

            new_content = []
            for j in range(chunks):
                if end > total_words:
                    end = total_words
                new_content = words[start:end]
                new_content_string = ' '.join(new_content)
                new_content_token_len = num_tokens_from_string(new_content_string)
                if new_content_token_len > 0:
                    new_list.append([df['title'][i], new_content_string, df['code'][i], new_content_token_len])
                start += ideal_size
                end += ideal_size
   
    # Create embeddings for each piece of content
    total_embeddings = len(new_list)
    print("Create " + str(total_embeddings) +  " embeddings")
    embed_time = (total_embeddings / 100) * .267
    print("This will take " + str(round(embed_time, 3)) + "ish minutes and cost: $" + str(get_total_embeddings_cost(df)) )
    

    for i in range(len(new_list)):
        text = str(new_list[i][0]) + "(" + str(new_list[i][2]) + "): " + str(new_list[i][1])
        embedding = get_embeddings(text)
        new_list[i].append(embedding)
        if ( i % 100 == 0):
            print(str(i) + " / " + str(len(new_list)))

    # Create a new dataframe from the list
    # TODO - edited to reference my format
    df_new = pd.DataFrame(new_list, columns=["title", "code", "description", 'tokens', 'embeddings'])
    df_new.head()

    # Save the dataframe with embeddings as a CSV file
    print("make new csv file")
    df_new.to_csv('courses_and_embeddings.csv', index=False)


def create_database_if_not_exists():
    # Connect to the default postgres database
    conn = psycopg2.connect("host='localhost' dbname='postgres' user='newuser' password='password'")
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  # Required to create a new database
    cur = conn.cursor()

    # Check if the CourseEmbeddings database exists
    cur.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'CourseEmbeddings'")
    exists = cur.fetchone()

    if not exists:
        print("Database CourseEmbeddings does not exist, creating it...")
        cur.execute('CREATE DATABASE "CourseEmbeddings"')

    cur.close()
    conn.close()

def courses_to_database():
    create_database_if_not_exists()
    print("Converting to embedding lists, may take a while")
    df_new = pd.read_csv('courses_and_embeddings.csv', converters={'embeddings': pd.eval})
    df_new.head()
    print("Done opening CSV file")

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
    CREATE TABLE IF NOT EXISTS embeddings (
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

    # Remind ourselves of the dataframe structure
    #df_new.head()


    #Batch insert embeddings and metadata from dataframe into PostgreSQL database

    # Prepare the list of tuples to insert
    #data_list = [(row['title'], row['code'], row['description'], int(row['tokens']), np.array(row['embeddings'])) for index, row in df_new.iterrows()]


    data_list = []


    for index, row in df_new.iterrows():
        # Extract data from the row
        title_insert = row['title']
        code_insert = row['code']
        description_insert = row['description']
        tokens_insert = int(row['tokens'])
        #print(type(row["embeddings"]))
        #print("uhhhhh")
        embedding_insert = np.array(row['embeddings'])
        
        # Validate that the embedding is one-dimensional
        if embedding_insert.ndim != 1:
            raise ValueError(f'Embedding at index {index} is not one-dimensional: {embedding_insert.ndim}')
        
        # Append the tuple to the data_list
        data_list.append((title_insert, code_insert, description_insert, tokens_insert, embedding_insert))

    # Print the first item for verification
    print(data_list[0])



    # Use execute_values to perform batch insertion
    #print(data_list[0])
    #print(df_new.dtypes)

    # Uncomment this if new embeddings need to be created
    execute_values(cur, "INSERT INTO embeddings (title, code, description, tokens, embedding) VALUES %s", data_list)
    # Commit after we insert all embeddings
    conn.commit()

    cur.execute("SELECT COUNT(*) as cnt FROM embeddings;")
    num_records = cur.fetchone()[0]
    print("Number of vector records in table: ", num_records,"\n")

    # print the first record in the table, for sanity-checking
    cur.execute("SELECT * FROM embeddings LIMIT 1;")
    records = cur.fetchall()
    #print("First record in table: ", records)

    # Create an index on the data for faster retrieval
    # this isn't really needed for 129 vectors, but it shows the usage for larger datasets
    # Note: always create this type of index after you have data already inserted into the DB

    #calculate the index parameters according to best practices
    num_lists = num_records / 1000
    if num_lists < 10:
        num_lists = 10
    if num_records > 1000000:
        num_lists = math.sqrt(num_records)

    #use the cosine distance measure, which is what we'll later use for querying
    cur.execute(f'CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = {num_lists});')
    conn.commit() 



# Get courses into the csv
#courses_to_csv()


# Get Embeddings
#embed_courses_to_csv()

# Push to Database
courses_to_database()





