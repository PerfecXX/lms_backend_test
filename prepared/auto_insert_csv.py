import csv
import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="lms"
)
mycursor = mydb.cursor()
with open('test.csv', 'r', newline='') as csvDataFile:
    csvDReader = csv.DictReader(csvDataFile)
    for column, row in enumerate(csvDReader):
        for i in range(0, csvDReader.line_num):
            if column == i:
                Time = str((row["Time"]))
                data1 = str((row["PDS_KB_NO"]))
                data2 = str((row["PART_NO"]))
                data3 = str(row["PART_NAME"])
                sql_data = "INSERT INTO stock values (\'{}\',\'{}\',\'{}\',100)".format(data1,data2,data3)
                print(sql_data)
                mycursor.execute(sql_data)
                mydb.commit()
                
