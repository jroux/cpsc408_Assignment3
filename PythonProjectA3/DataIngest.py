#do we need to include error handling for if user enters int in first name
#updating w primary key?
#check soft delete

import sqlite3

import pandas as pd
from pandas import DataFrame

#Connect to student database
conn = sqlite3.connect('./StudentDB.db')
mycursor = conn.cursor()


#import data from csv and read in data, inserting into Students table
with open("./students.csv") as inputfile:
    records = 0
    for row in inputfile:
        if records != 0:
            mycursor.execute("INSERT INTO Students(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNUmber, Major, GPA) VALUES (?,?,?,?,?,?,?,?,?)",
            row.split(","))
            conn.commit()
        records += 1



#print table with all students and attributes
mycursor.execute('SELECT * FROM Students;')
Allrecords = mycursor.fetchall()
#use pd.set_option to display full table with all attributes
pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
df = DataFrame(Allrecords, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
print(df)


#Adding a new student to the database "Students"
#Included exception error handling to ensure correct data type is inputed by user
userFirstName = input("Enter the first name of the student you would like to add to database: ")
userLastName = input("Enter the last name of the student: ")
while True:
    try:
        userGPA = float(input("Enter student's GPA: "))
        break
    except ValueError:
        print("Please enter a decimal: " )
userMajor = input("Enter student's major: ")
userFacultyAdvisor = input("Enter student's faculty advisor: ")
userAddress = input("Enter student's address: ")
userCity = input("Enter student's city: ")
userState = input("Enter the state the student lives in: ")
while True:
    try:
        userZipCode = int(input("Enter student's zipcode: "))
        break
    except ValueError:
        print("Please enter digits. Try again: ")
#ensuring that the user enters the full phone number
while True:
    try:
        userMobilePhoneNumber = int(input("Enter the student's phone number: "))
        count = 0
        while (userMobilePhoneNumber > 0):
            userMobilePhoneNumber = userMobilePhoneNumber // 10
            count += 1
        if (count == 10):
            break
        else:
            print("Please enter all 10 digits of phone number with no -. Try again: ")
            continue
        break
    except ValueError:
        print("Please enter all 10 digits of phone number with no -. Try again: ")

mycursor.execute("INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (userFirstName, userLastName, userGPA, userMajor, userFacultyAdvisor, userAddress, userCity, userState, userZipCode, userMobilePhoneNumber,))
conn.commit()


#Allow user to update major, advisor or mobile phone number
while True:
    try:
        userUpdate = int(input("Please enter the student ID of the student you would like to update: "))
        break
    except ValueError:
        print("Please enter the digits of the student ID: ")

while True:
    userChoice = int(input("Would you like to update major(1), advisor(2), mobile phone number(3). Please type in the corresponding number: "))
    if userChoice == 1:
        majorUpdate = input("Please enter the new updated major: ")
        mycursor.execute("UPDATE Students SET Major = ? WHERE StudentId = ?", (majorUpdate, userUpdate,))
        print("Successfully updated!")
        break
    elif userChoice == 2:
        advisorUpdate = input("Please enter the new updated advisor: ")
        mycursor.execute("UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?", (advisorUpdate, userUpdate,))
        print("Successfully updated!")
        break
    elif userChoice == 3:
        while True:
            try:
                phoneUpdate = int(input("Please enter the new updated phone number: "))
                count = 0
                phoneUpdateOfficial = phoneUpdate
                while (phoneUpdate > 0):
                    phoneUpdate = phoneUpdate // 10
                    count += 1
                if (count == 10):
                    break
                else:
                    print("Please enter all 10 digits of phone number with no -. Try again: ")
                    continue
                break
            except ValueError:
                print("Please enter all 10 digits of phone number with no -. Try again: ")
        mycursor.execute("UPDATE Students SET MobilePhoneNumber = ? WHERE StudentId = ?", (phoneUpdateOfficial, userUpdate,))
        print("Successfully updated!")
        break

conn.commit()

#Soft deleting a student by setting isDeleted to 1
deleteID = int(input("Which student would you like to remove from the database? Please enter the student ID: "))
mycursor.execute("UPDATE Students SET isDeleted = 1 WHERE StudentId = ?", (deleteID,))
print("The student has been deleted from the database.")
conn.commit()

conn.close()
