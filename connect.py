import psycopg2
from psycopg2 import OperationalError
from flask import Flask, render_template,request,session

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection



connection=create_connection("website_evaluator","postgres",None,"localhost",5432)
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

new_url="https://www.zara.com/"
insert_query = "UPDATE websites SET web_recom1 = '{}', web_recom2 = '{}', web_recom3 = '{}' , web_recom4 = '{}' , cnn_grade = '{}' , svm_grade = '{}' WHERE url = '{}' AND dev_id = '{}'".format(1,1,1,1,1,1,new_url,1)
connection.rollback()
connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query)


