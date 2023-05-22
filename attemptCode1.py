import csv
import os
import sys
import pyinputplus as pyip
import tabulate
## fungsi sorting based on companyName, businessField, or city --> diubah dulu ke dictionary datanya
## select sub-menu in each Menu still doesn't work properly (looping doesnt work properly)

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
file.close()
# print(db.values())
# columns = list(db.values())[0]
# data = list(db.values())[1:]
# for i in data:
#     print(i)
# print(tabulate.tabulate(data[0:1], headers=columns, tablefmt="github"))

def mainMenu():
    """
    The main program to run the whole process
    """
    global db # perubahan db di local akan memengaruhi db di global
    while True:
        # prompt choose mainMenu
        prompt = '\nChoose the menu that you want to run:\n'

        # print choices Menu
        choices = ['Show Data','Add Data', 'Update Data', 'Delete Data', 'Exit Program']
        for index,values in enumerate(choices):
            print(f'{index+1}. {values}')

        # user Input ## Maybe you have to try pyip.inputMenu, so notification will comes out as same as in instructions ##
        userInput = pyip.inputInt(prompt=prompt, max=len(choices))

        # Run selected Menu
        if userInput != 5:
            if userInput == 1:
                readMenu(db)
            elif userInput == 2:
                addMenu(db)
                db = addMenu(db) # return db terbaru
            elif userInput == 3:
                updateMenu()
            elif userInput == 4:
                deleteMenu()
            # eval(userInput)
        # Otherwise, exit from the menu
        else:
            print('Have a great day!')
            break

    # Open database in write condition
    file = open(path, 'w')

    # Keep the database update
    writer = csv.writer(file, lineterminator='\n', delimiter=';') ## timpa data masih SALAH ##
    columns = list(db.values())[0] # termasuk kolom dan data
    data = list(db.values())[1:]
    writer.writerow(columns) #db.values()
    data = list(db.values())[1:]
    for i in data:
         writer.writerow(i)

    # Close Program
    file.close()


# Show data function ## MASIH KURANG : APAKAH DATA AKAN DI SAVE ? JIKA, show 'Data successfully saved!' !!
def readMenu(database):
    """Fungsi untuk menampilkan database ke prompt

    Args:
        database (dictionary): database yang akan ditampilkan
    """
    # print title
    print('Yellow Pages created by @Wajul\n')

    # table coloumns
    columns = database['columns']
    data = list(database.values())[1:]

    # print db in tabular format
    print(tabulate.tabulate(data, headers=columns, tablefmt="github"))
    print('\n')

    # select menu inside readMenu:
    while True:
        choices = ['Tampilkan detail perusahaan', 'Kembali ke Main Menu']
        userInput = pyip.inputMenu(prompt='Select Read Menu:\n', choices=choices, numbered=True) ## userInput di-return sebagai string
        if userInput == 'Tampilkan detail perusahaan':
            choices1 = [id for id in range(len(data))]
            userInput1 = int(input("Which ID do you want to return ?\n"))
            #userInput1 = pyip.inputInt(prompt='Which ID do you want to return ?\n', blockRegexes=[r'a-zA-Z'], lessThan=len(data))
            # if ID (index) doesn't exist in database
            if userInput1 not in choices1:
                print('Data does not exist!\n')
                readMenu(database)
            # if ID (index) exist in database
            else:
                print(tabulate.tabulate(data[userInput1:userInput1+1], headers=columns, tablefmt="github"))
                print('\n')
        # back to main menu ('Kembali ke Main Menu')
        else:
            break
    
    # does data exist ? ## still ERROR!!! ##
    # print('company ID')
    # choices1 = [id for id in range(len(data))]
    # for index in choices1:
    #     print(index)
    # userInput1 = int(input("Which ID do you want to return ?\n")) ## change into pyinputpus validation
    # if userInput1 in choices1:
    #     print(tabulate.tabulate(data[userInput1:userInput1+1], headers=columns, tablefmt="github"))
    #     print('\n')
    # else:
    #     print('Data does not exist!\n')
    #     readMenu(database)

# add data
def addMenu(database):
    #print('addMenu In Progress')
    """
    Fungsi untuk menambahkan item ke dalam database

    Args:
        database (dict): database yang akan diolah

    Returns:
        dict: data terbaru
    """
    # list of data
    data = list(database.values())[1:]

    while True:
        choices = ['Menambahkan data Yellow Pages', 'Kembali ke Main Menu']
        userInput = pyip.inputMenu(prompt='Select Add Menu:\n', choices=choices, numbered=True)
        if userInput != 'Menambahkan data Yellow Pages':
            break
        # check the ID does exist or not ?
        else:
            choices = [id for id in range(len(data))]
            userInputIndex = pyip.inputInt(prompt='Masukkan ID (index) yang ingin ditambahkan: ') # input ID
            # if data already exist, show notification 'Data already exist!'
            if userInputIndex in choices:
                print('Data already exist!')
            # if ID doesnt exist, add to database
            else:
                companyName = pyip.inputStr(prompt='input company name: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                businessField = pyip.inputStr(prompt='input business field: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                city = pyip.inputStr(prompt='input city: ', applyFunc=lambda x: x.capitalize(), blockRegexes='1234567890@')
                phoneNumber = pyip.inputInt(prompt='input phone number: ')
                email = pyip.inputStr(prompt='input email: ')
                database.update(
                    {f'{userInputIndex}': [len(database)-1, companyName, businessField, city, phoneNumber, email]}
                )
                readMenu(database)
    return database


# update data
def updateMenu():
    print('updateMenu In Progress')

# delete data
def deleteMenu():
    print('deleteMenu In Progress')

mainMenu()
