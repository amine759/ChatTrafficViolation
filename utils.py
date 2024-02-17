import sqlite3
import ast
from datetime import date
import pandas as pd 
import boto3
# Connect to the SQLite database
conn = sqlite3.connect('db.sqlite3')

def extract(conn):
    records=[]
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()

    # Execute a SELECT query
    cursor.execute("select * from polls_amendes ;")

    # Fetch all rows from the result set
    rows = cursor.fetchall()

    # Iterate over the rows and print each row
    for row in rows:
        records.append(row)
    # Close the cursor and connection
    cursor.close()
    conn.close()
    return records

def transform(records):
    """
    id : int
    classe : str 
    avant : str 
    apres : str 
    point : str
    amende : str
    everything in csv file
    return csv
    """
    data = {
        "id": [],
        "day":[],
        "classe": [],
        "immediat-montant": [],
        "late-montant": [],
        "point": [],
        "amende": []
    }
    
    for rec in records:
        data["id"].append(int(rec[0]))
        classe, immediat_montant, late_montant, points = ast.literal_eval(rec[1])
        data["classe"].append(classe)
        data["immediat-montant"].append(immediat_montant)
        data["late-montant"].append(late_montant)
        data["point"].append(points)
        data["amende"].append(rec[2])
        data["day"].append(str(date.today()))

    df=pd.DataFrame(data)
    df.to_csv("s3-data/today{data['day']}.csv", sep='\t')

def load(file_name):
    s3 = boto3.resource('s3')

    # Print out bucket names
    with open(file_name, 'rb') as data:
        s3.Bucket('tchatdatathon').put_object(Key=file_name, Body=data)

records = extract(conn)
transform(records)
load("today.csv")