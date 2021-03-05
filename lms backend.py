import csv
import mysql.connector
import time
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="lms"
)

mycursor = mydb.cursor()

# mycursor.execute("CREATE DATABASE test")
# mycursor.execute("select * from stock")
# i = 1
# for x in mycursor:
# print(i, x)
# i += 1
#h = 1

with open('Data_test.csv', 'r', newline='') as csvDataFile:
    csvDReader = csv.DictReader(csvDataFile)
    for column, row in enumerate(csvDReader):
        for i in range(0, csvDReader.line_num):
            if column == i:
                Time = str((row["Time"]))
                data1 = str((row["PDS_KB_NO"]))
                data2 = str((row["PART_NO"]))
                data3 = str(row["PART_NAME"])
                sql_data = "UPDATE stock SET amout = amout-1 WHERE PDS_KB_NO ="+"\'"+data1+"\'"
                print(sql_data)
                mycursor.execute(sql_data)
                mydb.commit()
                time.sleep(60)
                #mycursor.execute("SELECT * FROM stock")
                #for x in mycursor:
                    #print(h, x)
                    #h += 1
