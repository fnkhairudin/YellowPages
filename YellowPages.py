import csv
import pyinputplus as pyip
import tabulate
from datetime import datetime

def readCsv(pathCsv):
    """Function to read your csv file

    Args:
        pathCsv (path) : path of your csv file

    Return:
        db : return your data from database as dictionary data type

    Warning:
        pay attention to the number of your columns in database. Need adjusment in updating dictionary data
    """
    # Read csv file
    file = open(pathCsv, 'r')
    reader = csv.reader(file, delimiter=';')

    # columns
    columns = next(reader)

    # make dictionary data type. db as a variable of dictionary data
    db = {'columns':columns}
    for row in reader: # updating dictionary data
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
    # return the dictionary data
    return db

def writeCsv(database, pathCsv):
    """Function to overwrite your csv file

    Args:
        pathCsv (path) : path of your csv file
        database : dictionary data
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

def record(pathRecord):
    """Function for showing what user does in the program

    Args:
        pathRecord : variable that stored your path of record file
    """
    file = open(pathRecord, "r")
    print(file.read())
    file.close()

"""CURD FUNCTION: 
    1. Create : addMenu(arg1,arg2,...)
    2. Update : updateMenu(arg1,arg2,...)
    3. Read   : readMenu(arg1,arg2,...)
    4. Delete : deleteMenu(arg1,arg2,...)
"""

# Show data function
def readMenu(database):
    """Function to show your data as tabular format

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
                # print title
                print("""
=============================================== Yellow Pages created by @Wajul ===============================================\n
                      """)
                print(tabulate.tabulate(data, headers=database['columns'], tablefmt="github"))
                print("\nData doesn't exist!")
            else:
                # print title
                print("""
=============================================== Yellow Pages created by @Wajul ===============================================\n
                      """)
                # print database in tabular format
                print(tabulate.tabulate(data, headers=database['columns'], tablefmt="github"))
                print('\n')
        # If user choose 2nd option
        elif userInput == 'Show database in detail':
            if data == []:
                # only display columns without any data
                print(tabulate.tabulate(data, headers=database['columns'], tablefmt="github"))
                print("\nData doesn't exist!")
            else:
                choicesDetail = ['Detail ID', 'businessField', 'City', 'sorted companyName', 'sorted ID']
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
                        print(tabulate.tabulate(list([database[str(userInput1)]]), headers=database['columns'], tablefmt="github"))
                        print('\n')
                
                # data detailing based on businessField            
                elif inputChoicesDetail == 'businessField':
                    # Available businessField stored in set data type, hence there's no duplication, then convert into list data type
                    businessFieldSet = {data[index][2] for index in range(len(data))}
                    businessFieldList = list(businessFieldSet)
                    # user choose city
                    userInput = pyip.inputMenu(prompt="Input the businessField you're looking for\n", choices=businessFieldList, numbered=True)
                    # find the keys of dictionary data
                    keysTarget = [str(i[0]) for i in data if i[2] == userInput]

                    # data target in 2D list based on keysTarget
                    dataTarget = [database[i] for i in keysTarget]

                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=database['columns'], tablefmt='github'))
                
                # data detailing based on city
                elif inputChoicesDetail == 'City':
                    # Available city stored in set data type, hence there's no duplication, the convert into list data type
                    citySet = {data[index][3] for index in range(len(data))}
                    cityList = list(citySet)
                    # user choose city
                    userInput = pyip.inputMenu(prompt="Input the city you're looking for\n", choices=cityList, numbered=True)
                    # find the keys of dictionary
                    keysTarget = [str(i[0]) for i in data if i[3] == userInput]

                    # data target in 2D list based on keysTarget
                    dataTarget = [database[i] for i in keysTarget]

                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=database['columns'], tablefmt='github'))
                
                # sorting based on companyName (A-Z)
                elif inputChoicesDetail == 'sorted companyName':
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
                    dataTarget = [database[str(i)] for i in keysTarget]

                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=database['columns'], tablefmt='github'))
                
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
                    dataTarget = [database[str(i)] for i in keysTarget]

                    # show dataTarget in tabular format
                    print(tabulate.tabulate(dataTarget, headers=database['columns'], tablefmt='github'))

        # back to main menu
        else:
            break


# add data
def addMenu(database, pathRecord):
    """Function to add data into your database

    Args:
        database (dict): database yang akan diolah
        pathRecord: variable that stored your path of record file

    Return:
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
                email = pyip.inputEmail(prompt='input email: ')
                
                # display added data in tabular format
                tabularAddedData = [userInputIndex, companyName, businessField, city, phoneNumber, email]
                print(tabulate.tabulate(list([tabularAddedData]), headers=database['columns'], tablefmt="github"))

                ## saving menu option
                savingMenuInput = pyip.inputYesNo(prompt='Are you sure want to save the data ? (Yes/No):')
                if savingMenuInput == 'yes':
                    database.update(
                        {f'{userInputIndex}': [userInputIndex, companyName, businessField, city, phoneNumber, email]})
                    
                    # show data after added data in database
                    data.append(tabularAddedData)
                    print(tabulate.tabulate(data, headers=database['columns'], tablefmt="github"))
                 
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
def deleteMenu(database, pathRecord, pathCsv):
    """Function to delete data in your database

    Args:
        database (dict): database yang akan diolah
        pathRecord: variable that stored your path of record file
        pathCsv : variable that stored your path of csv file
    
    Returns:
        database: latest database
    """

    # select delete menu
    while True:
        # read latest database
        readCsv(pathCsv)

        # list of data
        data = list(database.values())[1:]

        # available ID
        choices = [data[index][0] for index in range(len(data))]

        # run sub-delete menu
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
                    print(tabulate.tabulate(list([database[str(userInput2)]]), headers=database['columns'], tablefmt="github"))
                    # Ensure user whether to delete or not ?
                    deletingMenuInput = pyip.inputYesNo(prompt='Are you sure want to delete the data ? (Yes/No):')
                    # if 'Yes' delete data from database
                    if deletingMenuInput == 'yes':
                        del database[str(userInput2)]
                        # show database after data is deleted
                        print(tabulate.tabulate(list(database.values())[1:], headers=database['columns'], tablefmt="github"))
                        
                        # run writeCsv function
                        writeCsv(database, pathCsv)

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

                # list of data
                data = list(database.values())[1:]

                # available ID
                choices2 = [data[index][0] for index in range(len(data))]

                # ensure the user what is the exact amount of ID that user want to delete
                userInput3 = pyip.inputInt(prompt='Specify the exact amount of ID that you want to delete ?\n', greaterThan=1, lessThan=len(data))
                # store IDs that user want to delete in a variable
                userInput4 = []
                for i in range(userInput3):
                    userInput5 = pyip.inputMenu(prompt=f'Enter ID ke-{i+1} that you want to delete: \nThese are the available ID:\n', 
                                                choices=valueInttoStr(choices2), lettered=True)
                    # in order to showing the data that user want to delete
                    userInput4.append(userInput5)
                    # Delete the ID from the list of available ID because of ID has been selected, so that the user does not duplicate input 
                    choices2.remove(int(userInput5))

                # display IDs that user want to delete
                displayDeleteData = [database[i] for i in userInput4]
                print(tabulate.tabulate(displayDeleteData, headers=database['columns'], tablefmt="github"))

                # Ensure user whether to delete or not ?
                deletingMenuInput = pyip.inputYesNo(prompt='Are you sure want to delete the data ? (Yes/No):\n')
                # if 'Yes' delete data from database
                if deletingMenuInput == 'yes':
                    # delete multiple ID
                    for i in userInput4:
                        del database[str(i)]
                    # show database after data is deleted
                    print(tabulate.tabulate(list(database.values())[1:], headers=database['columns'], tablefmt="github"))

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
def updateMenu(database, pathRecord):
    """Functio to update certain column and ID of your data in database

    Args:
        database (dict): databases yang akan diolah
        pathRecord: variable that stored your path of record file
    
    Returns:
        database: latest database
    """
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
                print(tabulate.tabulate(list([database[str(userInputIndex)]]), headers=database['columns'], tablefmt="github"))
                updateMenuInput = pyip.inputYesNo(prompt='\nDo you want to continue to update the data ? (Yes/No):') 
                if updateMenuInput == 'yes':
                    # print columns options
                    userInputColumn = pyip.inputMenu(prompt='Which column do you want to update ?\n', choices=database['columns'][1:], numbered=True) # output string
                    # if the user selects a column that contains integer data type (phoneNumber)
                    if type(database[str(userInputIndex)][database['columns'].index(userInputColumn)]) == int:
                        # number of digits of phone number must be less than or equal to 11 digits
                        while True:
                            database[str(userInputIndex)][database['columns'].index(userInputColumn)] = pyip.inputInt(prompt='Enter new value:')
                            if len(str(database[str(userInputIndex)][database['columns'].index(userInputColumn)])) <= 11:
                                break
                            else:
                                print("number of digits of the phone number must be less than or equal to 11 digits")      
                    # if user choose 'Email' column
                    elif userInputColumn == 'Email':
                        database[str(userInputIndex)][database['columns'].index(userInputColumn)] = pyip.inputEmail(prompt='Enter new valu: ')
                    # if the user selects a column that contains string data type
                    else:
                        database[str(userInputIndex)][database['columns'].index(userInputColumn)] = pyip.inputStr(prompt='Enter new value:', applyFunc=lambda x: x.title(), blockRegexes='1234567890@')
                    # show updated row
                    print(tabulate.tabulate(list([database[str(userInputIndex)]]), headers=database['columns'], tablefmt="github"))
                    # Update data or not ?
                    updateMenuInput1 = pyip.inputYesNo(prompt='\nAre you sure want to update the data ? (Yes/No):') 
                    if updateMenuInput1 == 'yes':
                    # show updated database
                        print(tabulate.tabulate(list(database.values())[1:], headers=database['columns'], tablefmt="github"))
                        
                        # notification that data 'Data successfully updated!'
                        print('\nData successfully updated!\n')

                        # datetime object containing current date and time
                        now = datetime.now()
                        # dd/mm/YY H:M:S
                        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

                        # write record.txt
                        file = open(pathRecord, 'a')
                        file.write(f"(UPDATE) User has updated data with ID number {userInputIndex} in the {userInputColumn} column, then change the value into {database[str(userInputIndex)][database['columns'].index(userInputColumn)]} at {dt_string}\n")
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