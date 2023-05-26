import csv
import os
import sys
import pyinputplus as pyip
import tabulate
# fungsi sorting based on ID, companyName, businessField, or city could be added in readMenu --> diubah dulu ke dictionary datanya
# select sub-menu in each Menu still doesn't work properly (looping doesnt work properly, especially addMenu, deleteMenu)
# input validation, double check!!
# indexing start from 1 ?
# shall we save variables "data" and "choices" in other function ?
# dictionary data type can use in tabulate format also
# DELETE MENU : pay attention if user want to change a column that not str data type
# phoneNumber : provide country phone code ?
# choices dont use len(data) [DONE]
# show latest database after add or delete [DONE]
# Read menu option 1 not yet added [DONE]

path = r'C:\Users\faisa\Desktop\DataSciencePurwadhika\Modul1\CapstoneProjectModul1\dbYellowPages.csv'

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

# print(db)
# print(db.values())
# columns = list(db.values())[0]
# data = list(db.values())[1:]
# print(data)
# for i in data:
#     print(i)
# print(tabulate.tabulate(data[0:1], headers=columns, tablefmt="github"))

def mainMenu(): ## input validation ##
    """
    The main program to run the whole process
    """
    global db # perubahan db di local akan memengaruhi db di global
    while True:
        # print choices Menu
        choices = ['Show Data','Add Data', 'Update Data', 'Delete Data', 'Exit Program']
        for index,values in enumerate(choices):
            print(f'{index+1}. {values}')

        # user Input ## Maybe you have to try pyip.inputMenu, so notification will comes out as same as in instructions ##
        userInput = pyip.inputInt(prompt='\nChoose the menu that you want to run:\n', max=len(choices))

        # Run selected Menu
        if userInput != 5:
            if userInput == 1:
                readMenu(db)
            elif userInput == 2:
                # addMenu(db)
                db = addMenu(db) # return latest db
                continue
            elif userInput == 3:
                updateMenu()
            elif userInput == 4:
                # deleteMenu(db)
                db = deleteMenu(db) # return latest db
            # eval(userInput)
        # Otherwise, exit from the menu
        else:
            print('Have a great one!')
            break

    # Open database in write condition
    file = open(path, 'w')

    # Keep the database up to date
    writer = csv.writer(file, lineterminator='\n', delimiter=';')
    columns = list(db.values())[0] # termasuk kolom dan data
    data = list(db.values())[1:]
    writer.writerow(columns) #db.values()
    data = list(db.values())[1:]
    for i in data:
         writer.writerow(i)

    # Close Program
    file.close()


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
            if os.path.getsize(path) == 0:
                print("Data doesn't exist!")
            else:
                # print title
                print('Yellow Pages created by @Wajul\n')

                # print db in tabular format
                print(tabulate.tabulate(data, headers=columns, tablefmt="github"))
                print('\n')
        # If user choose 2nd option
        elif userInput == 'Show database in detail':
            choices1 = [data[index][0] for index in range(len(data))]
            userInput1 = int(input("Which ID do you want to return ?\n"))
            #userInput1 = pyip.inputInt(prompt='Which ID do you want to return ?\n', blockRegexes=[r'a-zA-Z'], lessThan=len(data))
            # if ID (index) doesn't exist in database
            if userInput1 not in choices1:
                print('Data does not exist!\n')
            # else: ID (index) exist in database
            else:
                print(tabulate.tabulate(list([database[str(userInput1)]]), headers=columns, tablefmt="github"))
                print('\n')

        # back to main menu ('Kembali ke Main Menu')
        else:
            break

# add data ## MASIH KURANG : (1). WHILE LOOP DOESNT WORK PROPERLY !!!!
def addMenu(database):
    """
    Fungsi untuk menambahkan item ke dalam database

    Args:
        database (dict): database yang akan diolah

    Returns:
        database: latest database
    """
    # flag = True

    # list of data
    data = list(database.values())[1:]

    while True:
        choices = ['Menambahkan data Yellow Pages', 'Kembali ke Main Menu']
        userInput = pyip.inputMenu(prompt='Select Add Menu:\n', choices=choices, numbered=True)
        if userInput == 'Menambahkan data Yellow Pages':
        # check the ID does exist or not ?
            choices = [data[index][0] for index in range(len(data))]
            userInputIndex = pyip.inputInt(prompt='Masukkan ID (index) yang ingin ditambahkan: ') # input ID
            # if data already exist, show notification 'Data already exist!'
            if userInputIndex in choices:
                print('ID already exist!')
            # if ID doesnt exist, you can add to database
            else:
                companyName = pyip.inputStr(prompt='input company name: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                businessField = pyip.inputStr(prompt='input business field: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                city = pyip.inputStr(prompt='input city: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                phoneNumber = pyip.inputInt(prompt='input phone number: ')
                email = pyip.inputEmail(prompt='input email: ')
                
                # print added data in tabular format
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
                    # readMenu(database)
                    print('\nData successfully saved!')
                else:
                    print('\nOkey double check your input data!')
        else: # Still doesnt work properly
            # print('doesnt work properly')
            # flag = False
            break
            
    # return latest database after added new data
    return database

# delete data ## WHILE LOOP DOESNT WORK PROPERLY !!!!
def deleteMenu(database):
    #print('deleteMenu In Progress')
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
            userInput = pyip.inputInt(prompt='Enter ID that you want to delete in database:')
            if userInput in choices:
                # print data that you want to delete in tabular format
                print(tabulate.tabulate(list([database[str(userInput)]]), headers=columns, tablefmt="github"))
                
                # Ensure user whether to delete or not ?
                deletingMenuInput = pyip.inputYesNo(prompt='Are you sure want to delete the data ? (Yes/No):')
                # if 'Yes' delete data from database
                if deletingMenuInput == 'yes':
                    del database[str(userInput)]
                    # show database after data is deleted
                    print(tabulate.tabulate(list(database.values())[1:], headers=columns, tablefmt="github"))
                    print('\nData successfully deleted!')
                else:
                    print('Okey double check your input!\n')
            else:
                print("ID doesn't exist!")
        else:
            break
    return database

# update data
def updateMenu(database):
    print('updateMenu In Progress')
    # # list of data
    # data = list(database.values())[1:]

    # # available ID
    # choices = [id for id in range(len(data))]

    # # select update menu
    # while True:
    #     choices1 = ['Update data in Yellow Pages database', 'Back to Main Menu']
    #     userInput = pyip.inputMenu(prompt='Select Update Menu:\n', choices=choices1, numbered=True)
    #     if userInput == 'Update data in Yellow Pages database':
    #         userInputIndex = pyip.inputInt(prompt='Enter ID that you want to update in database:')
    #         if userInputIndex not in choices:
    #             print("Data doens't exist!")
    #         else:
    #             print(tabulate.tabulate(data[userInputIndex:userInputIndex+1], headers=columns, tablefmt="github"))
    #             inputContinueUpdate = pyip.inputYesNo(prompt='Do you want continue to update ? (yes/no): ')
    #             if inputContinueUpdate == 'no':
    #                 continue
    #             else:
    #                 columns = list(db.values())[0] 
    #                 # ['ID', 'companyName', 'businessField', 'City', 'phoneNumber', 'Email']

    #                 inputUserColumn = pyip.inputMenu(prompt='Which column do you want to update ?', choices=columns, numbered=True) # output string
    #                 if inputUserColumn == 'ID':
                    
    #                 elif inputUserColumn == 'companyName':

    #                 elif inputUserColumn == 'businessField':
                    
    #                 elif inputUserColumn == 'city':
                    
    #                 elif


mainMenu()