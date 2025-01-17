# readFid_Visa.py  reads in excel sheet
import pandas as pd
import outlay_func as of

# open 2024 Fidelity Visa activity
filename = r"/Users/jeff/Downloads/Credit Card - 8869_01-01-2024_12-31-2024.csv"
df = pd.read_csv(filename)

# clean file
df = of.remove_null_rows(df, 'Name')

# keep only Date, Name, Amount fields
columns_to_keep = ['Date', 'Name', 'Amount']
df = df.drop(columns=[col for col in df.columns if col not in columns_to_keep])

# open db outlay
db = of.connect_to_db()
cursor = db.cursor()

# get a list of dates already in the table
datesNtable = of.get_loaded_dates(cursor, "date", "fid_visa")

# Step through the DataFrame one row at a time
for index, row in df.iterrows():
    date_str = row['Date']
    date_obj = of.datestr2date(date_str)
    name = row['Name']
    amount = row['Amount']

    # exclude rows with dates already in the table
    if date_str.strip() not in datesNtable:
        insert_query = "INSERT INTO fid_visa (date, vendor, amount) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (date_obj, name, amount))
        # Commit every 25 entries
        if index % 25 == 0:
            db.commit()

db.commit()
# Closing the cursor
cursor.close()
# Closing the connection
db.close()
