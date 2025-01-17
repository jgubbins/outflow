#outlay functions
import mysql.connector
import pandas as pd
from datetime import datetime

#  connect to database
def connect_to_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="Cepseg-netqiw-3restu",
        database="outlay"
        )
    try:
        cursor = db.cursor()
    except mysql.connector.Error as e:
        print(f"MySQL Error: {e}")
    except Exception as ex:
        print(f"General Error: {ex}")
        cursor = None
    finally:
        return db


# remove unwanted rows
def remove_null_rows(df, column_name):
    return df[df[column_name].notnull()]

# reads a date string, reformats it, and returns a datetime obj
def datestr2date(date_str):
    # check for 4-digit year, add if necessary
    if date_str[-4:-2] != '20':
        date_str = f'{date_str[:-2]}20{date_str[-2:]}'
    date_str = date_str.lstrip()
    date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()
    return date_obj


# gets distinct dates from a table and returns a list of stromg
def get_loaded_dates(cursor, field, table):
    # Execute the SQL query to get distinct entries from a column

    cursor.execute(f"SELECT DISTINCT {field} FROM {table}")
    # Fetch all distinct values and insert them into a list
    distinct_values = ( [row[0] for row in cursor.fetchall()])

    justDate = []
    for i in range(len(distinct_values)):
        dv = distinct_values[i].strftime("%m-%d-%Y")
        dv = dv.replace('-', '/')
        justDate.append(dv)
    return justDate
