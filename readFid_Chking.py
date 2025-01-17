# readFid_Chkng.py  reads in checking account statements
import pandas as pd
import outlay_func as of

# open Fidelity Checking acc't activity
filename = r"/Users/jeff/Downloads/History_for_Account_X64898317-2.csv"
df = pd.read_csv(filename)

# clean file
df = of.remove_null_rows(df, 'Action')
# Reverse the order of the DataFrame
df = df.iloc[::-1]

# keep only Run Date, Action,Amount ($) fields
columns_to_keep = ['Run Date', 'Action', 'Amount ($)']
df = df.drop(columns=[col for col in df.columns if col not in columns_to_keep])

# open db outlay
db = of.connect_to_db()
cursor = db.cursor()

# get a list of dates already in the table
datesNtable = of.get_loaded_dates(cursor, "date", "fid_chkg")

#Step through the DataFrame one row at a time
for index, row in df.iterrows():
    date_str = row['Run Date']
    date_obj = of.datestr2date(date_str)
    action = row['Action']
    amount = row['Amount ($)']

    # exclude rows with dates already in the table
    if date_str.strip() not in datesNtable:
        insert_query = "INSERT INTO fid_chkg (date, action, amount) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (date_obj, action, amount))
        # Commit every 25 entries
        if index % 25 == 0:
            db.commit()

db.commit()
# Closing the cursor
cursor.close()
# Closing the connection
db.close()
