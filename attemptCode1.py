import csv
import os
import sys
import pyinputplus as pyip
import tabulate
from datetime import datetime

# input validation, double check!!
# ID start from 1 ?
# shall we save variables "data" and "choices" in other function ?
# phoneNumber : provide country phone code ?
# limit nomor telepon di bagian input ?

# add sub-menu in log database ? clear all log ? [NO NEEDED]
# Delete beberapa ID atau berdasarkan menu lain --> looping delete atau sesuai index inputan user [DONE]
# select sub-menu in each Menu still doesn't work properly (looping doesnt work properly, especially addMenu, deleteMenu) [DONE]
# dictionary data type can use in tabulate format also [DONE]
# DELETE MENU : pay attention if user want to change a column that not str data type [DONE]
# choices dont use len(data) [DONE]
# show latest database after add or delete [DONE]
# Read menu option 1 not yet added [DONE]
# debugging csv file [DONE]
# fungsi sorting based on ID, companyName, businessField, or city could be added in readMenu [DONE]
# log database [DONE]
# make writeCsv function [DONE]
# write directly after added, deleted, or updated by using write code that stored in a function called writeCsv(database, pathCsv)? [DONE]

def writeCsv(database, pathCsv):
    """
    Fungsi untuk write CSV file

    Args:
        database (dictionary): database yang akan di-write
        path: path dari csv file
    """
    # Open database in write condition
    file = open(pathCsv, 'w')

    # Keep the database up to date
    writer = csv.writer(file, lineterminator='\n', delimiter=';')
    columns = list(database.values())[0] # termasuk kolom dan data
    data = list(database.values())[1:]
    writer.writerow(columns) #db.values()
    data = list(database.values())[1:]
    for i in data:
        writer.writerow(i)

    # close Program
    file.close()


def valueInttoStr(intlistData):
    """Fungsi untuk mengubah semua item yg berupa integer 
        menjadi string yang terdapat di dalam list
    Args:
        intlistData (list): list yang berisi item integer
    Returns:
        strChoices: list yang semua value itemnya berubah menjadi string
    """
    strChoices = []
    for i in intlistData:
        a = str(i)
        strChoices.append(a)
    return strChoices


# print(db)
# print(db.values())
# columns = list(db.values())[0]
# data = list(db.values())[1:]
# print(data)
# for i in data:
#     print(i)
# print(tabulate.tabulate(data[0:1], headers=columns, tablefmt="github"))

def record():
    """
    Fungsi untuk menampilkan record apa saja yang telah dilakukan user
    """
    file = open(pathRecord, "r")
    print(file.read())
    file.close()

def mainMenu():
    """
    The main program to run the whole process
    """
    # datetime object containing current date and time
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

    # write record.txt
    file = open(pathRecord, 'a')
    file.write(f'(IN) user has been logged in the program at {dt_string}\n')
    file.close()

    # perubahan db di local akan memengaruhi db di global
    global db 

    while True:
        # choices Menu
        choices = ['Show Data','Add Data', 'Update Data', 'Delete Data', 'Log database','Exit Program']

        # user Input
        userInput = pyip.inputMenu(prompt='\nChoose the menu that you want to run:\n', choices=choices, numbered=True)

        # Run selected Menu
        if userInput != 'Exit Program':
            if userInput == 'Show Data':
                readMenu(db)
            elif userInput == 'Add Data':
                # addMenu(db)
                db = addMenu(db) # return latest db
                continue
            elif userInput == 'Update Data':
                db = updateMenu(db) # return latest db
            elif userInput == 'Delete Data':
                # deleteMenu(db)
                db = deleteMenu(db) # return latest db
            elif userInput == 'Log database':
                record()
        # Otherwise, exit from the menu
        else:
            # datetime object containing current date and time
            now = datetime.now()
            # dd/mm/YY H:M:S
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

            # write record.txt
            file = open(pathRecord, 'a')
            file.write(f'(X) user has been logged out of the program at {dt_string}\n')
            file.close()
            print('Have a great one!')
            break

    sys.exit()


# Show data function
def readMenu(database):
    """
    Fungsi untuk menampilkan database ke prompt

    Args:
        database (dictionary): database yang akan ditampilkan
    """
    # 2D list of database from csv file
    data = list(database.values())[1:]
    # select menu inside readMenu:
    while True:
        choices = ['Show all data in database','Show database in detail', 'Back to Main Menu']
        userInput = pyip.inputMenu(prompt='Select Read Menu:\n', choices=choices, numbered=True) ## userInput di-return sebagai string
        # If user choose 1st option
        if userInput == 'Show all data in database':
            # if data in database doesnt exist
            if data == []:
                # only display columns without any data
                print(tabulate.tabulate(data, headers=columns, tablefmt="github"))
                print("\nData doesn't exist!")
            else:
                # print title
                print('Yellow Pages created by @Wajul\n')
                # print database in tabular format
                print(tabulate.tabulate(data, headers=columns, tablefmt="github"))
                print('\n')
        # If user choose 2nd option
        elif userInput == 'Show database in detail':
            if data == []:
                # only display columns without any data
                print(tabulate.tabulate(data, headers=columns, tablefmt="github"))
                print("\nData doesn't exist!")
            else:
                choicesDetail = ['Detail ID', 'businessField', 'City', 'companyName', 'sorted ID']
                inputChoicesDetail = pyip.inputMenu(prompt='Filter or sort data according to the: \n', choices=choicesDetail, numbered=True)
                # data detailing based on ID
                if inputChoicesDetail == 'Detail ID':
                    choices1 = [data[index][0] for index in range(len(data))]
                    userInput1 = pyip.inputInt(prompt="Which ID do you want to return ?\n")
                    #userInput1 = pyip.inputInt(prompt='Which ID do you want to return ?\n', blockRegexes=[r'a-zA-Z'], lessThan=len(data))
                    # if ID (index) doesn't exist in database
                    if userInput1 not in choices1:
                        print('Data does not exist!\n')
                    # else: ID (index) exist in database
                    else:
                        print(tabulate.tabulate(list([database[str(userInput1)]]), headers=columns, tablefmt="github"))
                        print('\n')
                
                # data detailing based on businessField            
                elif inputChoicesDetail == 'businessField':
                    # Available businessField stored in set data type, hence there's no duplication, then convert into list data type
                    businessFieldSet = {data[index][2] for index in range(len(data))}
                    businessFieldList = list(businessFieldSet)
                    # user choose city
                    userInput = pyip.inputMenu(prompt="Input the businessField you're looking for\n", choices=businessFieldList, numbered=True)
                    # find the keys of dictionary data
                    keysTarget = []
                    for i in data:
                        if i[2] == userInput:
                            keysTarget.append(str(i[0]))
                    # data target in 2D list based on keysTarget
                    dataTarget = []
                    for i in keysTarget:
                        dataTarget.append(database[i])
                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=columns, tablefmt='github'))
                
                # data detailing based on city
                elif inputChoicesDetail == 'City':
                    # Available city stored in set data type, hence there's no duplication, the convert into list data type
                    citySet = {data[index][3] for index in range(len(data))}
                    cityList = list(citySet)
                    # user choose city
                    userInput = pyip.inputMenu(prompt="Input the city you're looking for\n", choices=cityList, numbered=True)
                    # find the keys of dictionary
                    keysTarget = []
                    for i in data:
                        if i[3] == userInput:
                            keysTarget.append(str(i[0]))
                    # data target in 2D list based on keysTarget
                    dataTarget = []
                    for i in keysTarget:
                        dataTarget.append(database[i])

                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=columns, tablefmt='github'))
                
                # sorting based on companyName (A-Z)
                elif inputChoicesDetail == 'companyName':
                    # sorted company Name
                    companyNameList = [data[index][1] for index in range(len(data))]
                    companyNameSort = sorted(companyNameList) # order by companyName A-Z #

                    # find the keys of dictionary
                    keysTarget = []
                    for valuesI in companyNameSort: # compare sorted companyName with 2D list[1] which is companyName of database, 
                        for valuesJ in data:         # when match, return index[0] which is similar with keys
                            if valuesI == valuesJ[1]:
                                keysTarget.append(valuesJ[0])

                    # data target in 2D list based on keysTarget
                    dataTarget = []
                    for i in keysTarget:
                        dataTarget.append(database[str(i)])
                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=columns, tablefmt='github'))
                
                # sorting based on ID (0-9)
                else:
                    # sorted ID
                    idList = [data[index][0] for index in range(len(data))]
                    idSort = sorted(idList) # order by ID 0-9 #

                    # find the keys of dictionary
                    keysTarget = []
                    for valuesI in idSort: # compare sorted ID with 2D list[0] which is ID of each data in database, 
                        for valuesJ in data:         # when match, return index[0] which is similar with keys
                            if valuesI == valuesJ[0]:
                                keysTarget.append(valuesJ[0])

                    # data target in 2D list based on keysTarget
                    dataTarget = []
                    for i in keysTarget:
                        dataTarget.append(database[str(i)])
                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=columns, tablefmt='github'))

        # back to main menu
        else:
            break


# add data
def addMenu(database):
    """
    Fungsi untuk menambahkan item ke dalam database

    Args:
        database (dict): database yang akan diolah

    Returns:
        database: latest database
    """
    # list of data
    data = list(database.values())[1:]

    while True:
        choices = ['Menambahkan data Yellow Pages', 'Kembali ke Main Menu']
        userInput = pyip.inputMenu(prompt='Select Add Menu:\n', choices=choices, numbered=True)
        if userInput == 'Menambahkan data Yellow Pages':
        # check the ID does exist or not ?
            choices1 = [data[index][0] for index in range(len(data))]
            userInputIndex = pyip.inputInt(prompt='Masukkan ID (index) yang ingin ditambahkan: ') # input ID
            # if data already exist, show notification 'Data already exist!'
            if userInputIndex in choices1:
                print('ID already exist!')
            # if ID doesnt exist, you can add to database
            else:
                companyName = pyip.inputStr(prompt='input company name: ', applyFunc=lambda x: x.title(), blockRegexes='1234567890@')
                businessField = pyip.inputStr(prompt='input business field: ', applyFunc=lambda x: x.title(), blockRegexes='1234567890@')
                city = pyip.inputStr(prompt='input city: ', applyFunc=lambda x: x.title(), blockRegexes='1234567890@')
                # number of digits of phone number must be less than or equal to 11 digits
                while True:
                    phoneNumber = pyip.inputInt(prompt='input phone number: ')
                    if len(str(phoneNumber)) <= 11:
                        break
                    else:
                        print("number of digits of the phone number must be less than or equal to 11 digits")
                #phoneNumber = pyip.inputInt(prompt='input phone number: ')
                email = pyip.inputEmail(prompt='input email: ')
                
                # display added data in tabular format
                tabularAddedData = [userInputIndex, companyName, businessField, city, phoneNumber, email]
                print(tabulate.tabulate(list([tabularAddedData]), headers=columns, tablefmt="github"))

                ## saving menu option
                savingMenuInput = pyip.inputYesNo(prompt='Are you sure want to save the data ? (Yes/No):')
                if savingMenuInput == 'yes':
                    database.update(
                        {f'{userInputIndex}': [userInputIndex, companyName, businessField, city, phoneNumber, email]})
                    
                    # show data after added data in database
                    data.append(tabularAddedData)
                    print(tabulate.tabulate(data, headers=columns, tablefmt="github"))

                    # added into csv file ## database is db, path is csv file path
                    writeCsv(db,path)
                    
                    # notification that data 'Data successfully saved!'
                    print('\nData successfully saved!\n')
                    
                    # datetime object containing current date and time
                    now = datetime.now()
                    # dd/mm/YY H:M:S
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                    # write record.txt
                    file = open(pathRecord, 'a')
                    file.write(f'(ADD) User has added data with ID number {userInputIndex} at {dt_string}\n')
                    file.close()
                else:
                    print('\nOkey double check your input data!')
        
        # back to Main Menu
        else:
            break
            
    # keep database up to date
    return database


# delete data
def deleteMenu(database):
    """Fungsi untuk menghapus item dari database

    Args:
        database (dict): databases yang akan diolah

    Returns:
        database: latest database
    """
    # list of data
    data = list(database.values())[1:]

    # available ID
    choices = [data[index][0] for index in range(len(data))]

    # select delete menu
    while True:
        choices1 = ['Delete data in Yellow Pages database', 'Back to Main Menu']
        userInput = pyip.inputMenu(prompt='Select Delete Menu:\n', choices=choices1, numbered=True)
        if userInput == 'Delete data in Yellow Pages database':
            # ensure user how many ID that user want to delete
            userInput1 = pyip.inputChoice(prompt='How many ID that you want to delete ?\nPlease select one of: one or more than one ? ', 
                             choices=['one', 'more than one'])
            
            # if user want to delete only one ID
            if userInput1 == 'one':
                userInput2 = pyip.inputInt(prompt='Enter ID that you want to delete in database:')
                if userInput2 in choices:
                    # display data that you want to delete in tabular format
                    print(tabulate.tabulate(list([database[str(userInput2)]]), headers=columns, tablefmt="github"))
                    # Ensure user whether to delete or not ?
                    deletingMenuInput = pyip.inputYesNo(prompt='Are you sure want to delete the data ? (Yes/No):')
                    # if 'Yes' delete data from database
                    if deletingMenuInput == 'yes':
                        del database[str(userInput2)]
                        # show database after data is deleted
                        print(tabulate.tabulate(list(database.values())[1:], headers=columns, tablefmt="github"))
                        
                        # deleted data in csv file ## database as db, path as csv file path
                        writeCsv(db, path)

                        # notification that data 'Data successfully deleted!'
                        print('\nData successfully deleted!')

                        # datetime object containing current date and time
                        now = datetime.now()
                        # dd/mm/YY H:M:S
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        # write record.txt
                        file = open(pathRecord, 'a')
                        file.write(f'(DELETE) User has deleted data with ID number {userInput2} at {dt_string}\n')
                        file.close()
                        
                    else:
                        print('Okey double check your input!\n')
                else:
                    print("ID doesn't exist!")

            # if user want to delete more than one ID
            else:
                # ensure the user what is the exact amount of ID that user want to delete
                userInput3 = pyip.inputInt(prompt='Specify the exact amount of ID that you want to delete ?\n', greaterThan=1, lessThan=len(data))
                userInput4 = []
                # available ID
                choices2 = [data[index][0] for index in range(len(data))] # [0, 1, 2, 3, 56]
                for i in range(userInput3):
                    userInput5 = pyip.inputMenu(prompt=f'Enter ID ke-{i+1} that you want to delete: \nThese are the available ID:\n', 
                                                choices=valueInttoStr(choices2), lettered=True)
                    # in order to showing the data that user want to delete
                    userInput4.append(userInput5)
                    # Delete the ID from the list of available ID because of ID has been selected, so that the user does not duplicate input 
                    choices2.remove(int(userInput5))

                # display IDs that user want to delete
                displayDeleteData = []
                for i in userInput4:
                    displayDeleteData.append(database[i])
                print(tabulate.tabulate(displayDeleteData, headers=columns, tablefmt="github"))

                # Ensure user whether to delete or not ?
                deletingMenuInput = pyip.inputYesNo(prompt='Are you sure want to delete the data ? (Yes/No):\n')
                # if 'Yes' delete data from database
                if deletingMenuInput == 'yes':
                    # delete multiple ID
                    for i in userInput4:
                        del database[str(i)]
                    # show database after data is deleted
                    print(tabulate.tabulate(list(database.values())[1:], headers=columns, tablefmt="github"))
                    
                    # deleted data in csv file ## database as db, path as csv file path
                    writeCsv(db, path)

                    # notification that data 'Data successfully deleted!'
                    print('\nData successfully deleted!')

                    # datetime object containing current date and time
                    now = datetime.now()
                    # dd/mm/YY H:M:S
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                    # write record.txt
                    file = open(pathRecord, 'a')
                    file.write(f"(DELETE) User has deleted data with ID number {','.join(userInput4)} at {dt_string}\n")
                    file.close()
                    
                else:
                    print('Okey double check your input!\n')
        # Back to main menu
        else:
            break
    # keep database up to date
    return database


# update data
def updateMenu(database):
    # list of data
    data = list(database.values())[1:]

    # available ID
    choices = [data[index][0] for index in range(len(data))]

    # select update menu
    while True:
        choices1 = ['Edit data in Yellow Pages database', 'Back to Main Menu']
        userInput = pyip.inputMenu(prompt='Select Update Menu:\n', choices=choices1, numbered=True)
        if userInput == 'Edit data in Yellow Pages database':
            userInputIndex = pyip.inputInt(prompt='Which ID do you want to update ?\n')
            # if userInputIdex does exist in database
            if userInputIndex in choices:
                # show row that user want to update
                print(tabulate.tabulate(list([database[str(userInputIndex)]]), headers=columns, tablefmt="github"))
                updateMenuInput = pyip.inputYesNo(prompt='\nDo you want to continue to update the data ? (Yes/No):') 
                if updateMenuInput == 'yes':
                    # print columns options
                    userInputColumn = pyip.inputMenu(prompt='Which column do you want to update ?\n', choices=columns[1:], numbered=True) # output string
                    # if the user selects a column that contains integer data type
                    if type(database[str(userInputIndex)][columns.index(userInputColumn)]) == int:  
                        database[str(userInputIndex)][columns.index(userInputColumn)] = pyip.inputInt(prompt='Enter new value:')
                    # if user choose 'Email' column
                    elif userInputColumn == 'Email':
                        database[str(userInputIndex)][columns.index(userInputColumn)] = pyip.inputEmail(prompt='Enter new valu: ')
                    # if the user selects a column that contains string data type
                    else:
                        database[str(userInputIndex)][columns.index(userInputColumn)] = pyip.inputStr(prompt='Enter new value:', applyFunc=lambda x: x.title(), blockRegexes='1234567890@')
                    # show updated row
                    print(tabulate.tabulate(list([database[str(userInputIndex)]]), headers=columns, tablefmt="github"))
                    # Update data or not ?
                    updateMenuInput1 = pyip.inputYesNo(prompt='\nAre you sure want to update the data ? (Yes/No):') 
                    if updateMenuInput1 == 'yes':
                    # show updated database
                        print(tabulate.tabulate(list(database.values())[1:], headers=columns, tablefmt="github"))
                        
                        # deleted data in csv file ## database is db, path is csv file path
                        writeCsv(db, path)

                        # notification that data 'Data successfully updated!'
                        print('\nData successfully updated!\n')

                        # datetime object containing current date and time
                        now = datetime.now()
                        # dd/mm/YY H:M:S
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        # write record.txt
                        file = open(pathRecord, 'a')
                        file.write(f'(UPDATE) User has updated data with ID number {userInputIndex} in the {userInputColumn} column, then change the value into {database[str(userInputIndex)][columns.index(userInputColumn)]} at {dt_string}\n')
                        file.close()
                        
                    else:
                        print('Okey double check again your input data!\n')           
                # user does not continue to update data
                else:
                    print('\nOkey double check your input data!')
            # if ID doesnt exist            
            else:
                print("The data you're looking for doesn't exist\n")
        # Back to main Menu
        else:
            break

    # keep database up to date
    return database


# first, read path database
path = r'C:\Users\faisa\Desktop\DataSciencePurwadhika\Modul1\CapstoneProjectModul1\dbYellowPages.csv'

# second, read path record
pathRecord = r'C:\Users\faisa\Desktop\DataSciencePurwadhika\Modul1\CapstoneProjectModul1\recordYellowPages.txt'

if os.path.getsize(path) == 0:
    print('Database doesnt exist, please enter some data!')
else:
    # Read csv file
    file = open(path, 'r')
    reader = csv.reader(file, delimiter=';')

    # columns
    columns = next(reader)

    # make dictionary data type. db as a variable of dictionary data
    db = {'columns':columns}
    for row in reader: # updating dictionary data
        #print(row[1])
        db.update({
            str(row[0]) : [int(row[0]), 
                    str(row[1]),
                    str(row[2]), 
                    str(row[3]),
                    int(row[4]),
                    str(row[5])
                    ]})
    # close program
    file.close()

    # run the program
    mainMenu()
# close the program
sys.exit()