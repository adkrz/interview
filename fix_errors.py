import sqlite3
import pandas as pd
import os
import pathlib

conn = sqlite3.connect("test.sqlite")
conn.execute("""CREATE TABLE IF NOT EXISTS DATA
(NAME TEXT NOT NULL,
AVERAGE REAL NOT NULL)
""")

input_files = pathlib.Path(os.getcwd()).glob('data*.txt')

# Task: read header + numbers from files in folder
# for each file, write the header and average to DB
# check, if collected averages are equal

# Start searching for errors from there:
# Imagine, this is a part of a bigger application
# Number of input files is arbitrary: 0...n
# Number of data samples in files is arbitrary: 0...m, files may be huge

def pretty_print_values(arr=[]):
    return ", ".join(str(item) for item in arr)


collected_averages = []


for file in input_files:
    log = open("log.txt", "wt")
    log.write(str(file) + "\n")
    data = pd.read_csv(str(file))
    name = data.columns[0]
    values = data[name]
    average = sum(values) / len(values)
    print(f"{name} = {average}")
    sql = f'INSERT INTO DATA (NAME, AVERAGE) VALUES ("{name}", {average})'
    mycursor = conn.cursor()
    mycursor.execute(sql)
    conn.commit()
    collected_averages.append(average)
conn.close()
are_equal = all(a == collected_averages[0] for a in collected_averages[1:])
print(f"Collected averages: {pretty_print_values(collected_averages)}")
print(f"Are all averages equal? {are_equal}")
