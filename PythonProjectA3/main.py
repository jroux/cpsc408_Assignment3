import DataIngest as di

# Execute and run program/functions
def runAssignment3():
    di.importData()
    di.menu()
    di.conn.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    runAssignment3()

