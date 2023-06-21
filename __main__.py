import os
import YellowPages as yp
import sys
from datetime import datetime
import pyinputplus as pyip

def mainMenu(database, pathCsv, pathRecord):
    """
    Function to run the whole program

    Args:
        database (dictionary): data in your database
        pathCsv : variable that stored your path of csv file
        pathRecord : variable that stored your path of record file
    """
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # write record.txt
    file = open(pathRecord, 'a')
    file.write(f'(IN) user has been logged in the program at {dt_string}\n')
    file.close()

    while True:
        print("""
    ======================= YELLOW PAGES IN INDONESIA =======================
    """)
        # choices Menu
        choices = ['Show Data','Add Data', 'Update Data', 'Delete Data', 'Log database','Exit Program']

        # user Input
        userInput = pyip.inputMenu(prompt='Choose the menu that you want to run:\n', choices=choices, numbered=True)

        # Run selected Menu
        if userInput != 'Exit Program':
            if userInput == 'Show Data':
                yp.readMenu(database)
            elif userInput == 'Add Data':
                database = yp.addMenu(database, pathRecord) # return latest database
            elif userInput == 'Update Data':
                database = yp.updateMenu(database, pathRecord) # return latest database
            elif userInput == 'Delete Data':
                database = yp.deleteMenu(database, pathRecord, pathCsv) # return latest database
            elif userInput == 'Log database':
                yp.record(pathRecord)
        # Otherwise, exit from the menu
        else:
            # keep database up to date
            yp.writeCsv(database, pathCsv)

            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            # write record.txt
            file = open(pathRecord, 'a')
            file.write(f'(OUT) user has been logged out of the program at {dt_string}\n')
            file.close()
            print('Have a great one!')
            break

    sys.exit()

if __name__ == '__main__':
    # first, read database's path
    path_csv = r'C:\Users\faisa\Desktop\DataSciencePurwadhika\Modul1\CapstoneProjectModul1\dbYellowPages.csv'

    # second, read record's path
    path_record = r'C:\Users\faisa\Desktop\DataSciencePurwadhika\Modul1\CapstoneProjectModul1\recordYellowPages.txt'

    if os.path.getsize(path_csv) == 0:
        print('Database doesnt exist, please enter some data!')
    else:
        # read csv file
        yp.readCsv(path_csv)

        # run the program
        mainMenu(yp.readCsv(path_csv), path_csv, path_record)
    # close the program
    sys.exit()