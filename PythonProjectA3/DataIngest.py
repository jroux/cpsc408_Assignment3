#Jessica Roux
#Student ID: 2317255
#Chapman Email: jroux@chapman.edu
#Course: 408-01
#Assignment 3


#imports
import sqlite3
import pandas as pd
from pandas import DataFrame

#Connect to student database
conn = sqlite3.connect('./StudentDB.db')
mycursor = conn.cursor()

#Function that provides user a menu to select which option they would like to execute
def menu():
    while True:
        print("\n")
        print("Welcome! Below are your options: ")
        print("1) Display all students and their information")
        print("2) Add a new student")
        print("3) Update a student's information")
        print("4) Delete a student")
        print("5) Search/Display students by Major, GPA, City, State or Advisor")
        print("6) Exit program")
        menuInput = input("Please select which option you would like to execute. Enter the corresponding digit: ")
        if menuInput == "1":
            print("\n")
            displayStudents()
            continue
        elif menuInput == "2":
            print("\n")
            addStudent()
            continue
        elif menuInput == "3":
            print("\n")
            updateStudent()
            continue
        elif menuInput == "4":
            print("\n")
            deleteStudent()
            continue
        elif menuInput == "5":
            print("\n")
            searchStudent()
            continue
        elif menuInput == "6":
            print("\n")
            print("Quitting...Goodbye!")
            quit()
        else:
            print("\n")
            print("Please enter the single digit of your desired option")
            continue


#Function that imports data from students.csv, reads in data, inserts data into Students table
def importData():
    #making sure data does repeat everytime ran
    mycursor.execute("SELECT * FROM Students")
    data1 = mycursor.fetchall()
    if (data1 == []):
        with open("./students.csv") as inputfile:
            records = 0
            for row in inputfile:
                if records != 0:
                    mycursor.execute("INSERT INTO Students(FirstName, LastName, Address, City, State, ZipCode, MobilePhoneNUmber, Major, GPA) VALUES (?,?,?,?,?,?,?,?,?)",
                    row.split(","))
                    conn.commit()
                records += 1


#Function that prints and displays the full Students table with all students and attributes
def displayStudents():
    mycursor.execute('SELECT * FROM Students;')
    Allrecords = mycursor.fetchall()
    #use pd.set_option to display full table with all attributes
    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
    #use DataFrame for cleaner display
    df = DataFrame(Allrecords, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
    print(df)


#Function to add a new student to the Students table
#Included exception error handling to ensure correct data type is inputed by user
def addStudent():
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
    test = True
    while (test == True):
        try:
            userZipCode = int(input("Enter student's zipcode: "))
            count = 0
            #All zip codes are 5 digits, checking to ensure input is 5 digits long
            while (userZipCode > 0):
                userZipCode = userZipCode // 10
                count += 1
            if (count == 5):
                test = False
            else:
                print("Please enter all 5 digits of zip code. Try again: ")
                continue
            break
        except ValueError:
            print("Please enter digits. Try again: ")
    while True:
        try:
            userMobilePhoneNumber = input("Enter the student's phone number: ")
            break
        except ValueError:
            print("Please enter all digits of phone number. Try again: ")
    mycursor.execute("INSERT INTO Students (FirstName, LastName, GPA, Major, FacultyAdvisor, Address, City, State, ZipCode, MobilePhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (userFirstName, userLastName, userGPA, userMajor, userFacultyAdvisor, userAddress, userCity, userState, userZipCode, userMobilePhoneNumber,))
    print("The student was successfully added.")
    conn.commit()


#Function to update a student's major, advisor or mobile phone number
def updateStudent():
    test = True
    while (test == True):
        #Check to make sure the enter student id is in the Students table
        userUpdate = input("Please enter the student ID of the student you would like to update: ")
        mycursor.execute("SELECT DISTINCT StudentId FROM Students WHERE StudentId = ?", [userUpdate])
        records = mycursor.fetchall()
        if records == []:
            print("Please enter a valid student ID")
            continue
        else:
            option = True
            while (option == True):
                userChoice = input("Would you like to update major(1), advisor(2), mobile phone number(3). Please type in the corresponding number: ")
                if userChoice == "1":
                    majorUpdate = input("Please enter the new updated major: ")
                    mycursor.execute("UPDATE Students SET Major = ? WHERE StudentId = ?", (majorUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                elif userChoice == "2":
                    advisorUpdate = input("Please enter the new updated advisor: ")
                    mycursor.execute("UPDATE Students SET FacultyAdvisor = ? WHERE StudentId = ?", (advisorUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                elif userChoice == "3":
                    while True:
                        try:
                            phoneUpdate = input("Please enter the new updated phone number: ")
                            break
                        except ValueError:
                            print("Please enter all digits of phone number. Try again: ")
                    mycursor.execute("UPDATE Students SET MobilePhoneNumber = ? WHERE StudentId = ?", (phoneUpdate, userUpdate,))
                    print("Successfully updated!")
                    test = False
                    option = False
                else:
                    print("Please enter a valid option.")
                    continue
    conn.commit()


#Function to soft delete a student by setting isDeleted to 1
def deleteStudent():
    test = True
    while (test == True):
        #Check to make sure the enter student id is in the Students table
        deleteID = input("Which student would you like to remove from the database? Please enter the student ID: ")
        mycursor.execute("SELECT DISTINCT StudentId FROM Students WHERE StudentId = ?", [deleteID])
        records = mycursor.fetchall()
        if records == []:
            print("Please enter a valid student ID")
            continue
        else:
            test = False
            mycursor.execute("UPDATE Students SET isDeleted = 1 WHERE StudentId = ?", (deleteID,))
            print("The student has been deleted from the database.")
            conn.commit()


#Function to search and display students information from major, gpa, city, state, or faculty advisor
def searchStudent():
    print("Which field would you like to display student by?")
    print("1) major")
    print("2) GPA")
    print("3) city")
    print("4) state")
    print("5) faculty advisor")
    checkWhile = True
    while (checkWhile == True):
        fieldInput = input("Please enter the corresponding number: ")
        if fieldInput == "1":
            #show user their options to choose from
            mycursor.execute("SELECT DISTINCT Major FROM Students")
            print(mycursor.fetchall())
            test = True
            while (test == True):
                majorDisplay = input("What major would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE Major = ?", (majorDisplay,))
                records = mycursor.fetchall()
                if records == []:
                    print("Please enter a valid major from the list")
                    continue
                else:
                    test = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
                    print(df)
                    checkWhile = False
        elif fieldInput == "2":
            #show user their options to choose from
            mycursor.execute("SELECT DISTINCT GPA FROM Students")
            print(mycursor.fetchall())
            test = True
            while (test == True):
                GPADisplay = input("What gpa would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE GPA = ?", (GPADisplay,))
                records = mycursor.fetchall()
                if records == []:
                    print("Please enter a valid GPA from the list")
                    continue
                else:
                    test = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
                    print(df)
                    checkWhile = False
        elif fieldInput == "3":
            #show user their options to choose from
            mycursor.execute("SELECT DISTINCT City FROM Students")
            print(mycursor.fetchall())
            test = True
            while (test == True):
                CityDisplay = input("What city would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE City = ?", (CityDisplay,))
                records = mycursor.fetchall()
                if records == []:
                    print("Please enter a valid city from the list")
                    continue
                else:
                    test = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
                    print(df)
                    checkWhile = False
        elif fieldInput == "4":
            #show user their options to choose from
            mycursor.execute("SELECT DISTINCT State FROM Students")
            print(mycursor.fetchall())
            test = True
            while (test == True):
                StateDisplay = input("What state would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE State = ?", (StateDisplay,))
                records = mycursor.fetchall()
                if records == []:
                    print("Please enter a valid state from the list")
                    continue
                else:
                    test = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
                    print(df)
                    checkWhile = False
        elif fieldInput == "5":
            #show user their options to choose from
            mycursor.execute("SELECT DISTINCT FacultyAdvisor FROM Students")
            print(mycursor.fetchall())
            test = True
            while (test == True):
                FacultyDisplay = input("What faculty would you like to search by: ")
                mycursor.execute("SELECT * FROM Students WHERE FacultyAdvisor = ?", (FacultyDisplay,))
                records = mycursor.fetchall()
                if records == []:
                    print("Please enter a valid faculty advisor from the list")
                    continue
                else:
                    test = False
                    pd.set_option("display.max_rows", None, "display.max_columns", None, "display.width", None)
                    df = DataFrame(records, columns=['StudentId', 'FirstName', 'LastName', 'GPA', 'Major', 'FacultyAdvisor', 'Address', 'City', 'State', 'ZipCode', 'MobilePhoneNUmber',  'isDeleted'])
                    print(df)
                    checkWhile = False
        else:
            print("Please enter a valid input.")
            continue
    conn.commit()