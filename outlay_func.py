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

def datestr2date(date_str):
    # check for 4-digit year, add if necessary
    if date_str[-4:-2] != '20':
        date_str = f'{date_str[:-2]}20{date_str[-2:]}'
    date_obj = datetime.strptime(date_str, "%m/%d/%Y").date()
    return date_obj

