import json
import csv
import datetime
from pathlib import Path
#classes

def writeToJSON(filename, data):
    filePathNameWithExtension = filename + ".json"
    with open(filePathNameWithExtension, "w") as fp:
        json.dump(data, fp)

def choice(choiceList):
    choice = input("Please select a option.\n")
    while (choice not in choiceList):
        choice = input("Invalid input, please try again!\n")
    return int(choice)

def stringInput(message):
    string = input(message + "\n")
    while (not string.strip()):
        string = input("Invalid input, please try afain!\n")
    return string

currentBookID = 0
def generateBookID():
    global currentBookID
    currentBookID += 1
    return "b" + str(currentBookID)

currentBookItemID = 0
def generateBookItemID():
    global currentBookItemID
    currentBookItemID += 1
    return "bi" + str(currentBookItemID)

currentloanItemID = 0
def generateLoanItemID():
    global currentloanItemID
    currentloanItemID += 1
    return "li" + str(currentloanItemID)

class PublicLibrary:
    def __init__(self):
        self.catalog = Catalog()
        self.loanAdministation = LoanAdministation()
        self.customers = {}

    def startLibrary(self, bookfile, customerfile, loanitemfile, bookitemfile):
        customerList = csv.reader(customerfile)
        customerList.__next__()
        for row in customerList:
            if (row !=[]):
                Customer(self, row)
        booklist = json.load(bookfile)
        for d in booklist:
            if (d != {}):
                book = Book(self, **d)
        bookItemList = json.load(bookitemfile)
        for bi in bookItemList:
            if (bi != []):
                book = self.catalog.bookDict[bi["bookID"]]
                bookItem = BookItem(book , bi["id"], bi["takenOrNot"])
                self.catalog.bookItemDict[bookItem.id] = bookItem
        loanItemList = json.load(loanitemfile)
        for li in loanItemList:
            if (li != []):
                LoanItem(self, li["customerID"], li["bookItemID"])

class Librarian:
    @staticmethod
    def showAllCustomers(publicLibrary):
        for i in publicLibrary.customers:
            c = publicLibrary.customers[i]
            print(i + " : " + c.username + " , " + c.streetAdress + " , " + c.zipCode + " , " + c.city + " , " + c.email + " , " + c.telephoneNumber)

    @staticmethod
    def addCustomer(publicLibrary):
        customerID = len(publicLibrary.customers) + 1
        gender = stringInput("Gender? ")
        nationality = stringInput("Nationality? ")
        firstName = stringInput("Fist name? ")
        surname = stringInput("Surname? ")
        streetAdress = stringInput("Street adress? ")
        zipCode = stringInput("Zip code? ")
        city = stringInput("City? ")
        email = stringInput("Email? ")
        username = stringInput("username? ")
        telephoneNumber = stringInput("Telephone number? ")
        data = [customerID, gender, nationality, firstName, surname, streetAdress, zipCode, city, email, username, telephoneNumber]
        Customer(publicLibrary, data)

    @staticmethod
    def removeCustomer(publicLibrary):
        customerID = stringInput("Pleas enter his / her customerID: ")
        while (customerID not in publicLibrary.customers):
            customerID = input("Please enter a correct customerID.\n")
        publicLibrary.customers.pop(customerID)
    
    @staticmethod
    def showAllBooks(publicLibrary):
        for i in publicLibrary.catalog.bookDict:
            b = publicLibrary.catalog.bookDict[i]
            print(b.id + ": " + b.title + ", " + b.author + ", " + str(b.pages) + ", " + b.language + ", " + str(b.year))

    @staticmethod
    def showAllBookItems(publicLibrary):
        for i in publicLibrary.catalog.bookItemDict:
            bi = publicLibrary.catalog.bookItemDict[i]
            takenOrNot = "not taken"
            if (bi.taken):
                takenOrNot = "taken"
            print(bi.id + ": " + takenOrNot + ", " + bi.book.title)

    @staticmethod
    def addBookItem(publicLibrary):
        bookID = stringInput("Pleas enter the BookID: ")
        while (bookID not in publicLibrary.catalog.bookDict):
            bookID = input("Please enter a correct bookID.\n")
        b = publicLibrary.catalog.bookDict[bookID]
        bi = BookItem(b)
        publicLibrary.catalog.bookItemDict[bi.id] = bi
        
    @staticmethod
    def removeBookItem(publicLibrary):
        BookItemID = stringInput("Pleas enter the BookItemID: ")
        while (BookItemID not in publicLibrary.catalog.bookItemDict):
            BookItemID = input("Please enter a correct BookItemID.\n")
        publicLibrary.catalog.bookItemDict.pop(BookItemID)

    @staticmethod
    def addBook(publicLibrary):
        author = stringInput("author? ")
        country = stringInput("country? ")
        imagelink = input("imagelink (can remain empty)?\n")
        language = stringInput("language? ")
        link = input("link(can remain empty)?\n")
        pages = stringInput("pages? ")
        title = stringInput("title? ")
        year = stringInput("year? ")
        data = {"author" : author, "country" : country,  "imageLink" : imagelink,  "language" : language,  "link" : link,   "pages" : pages,   "title" : title,   "year" : year}
        Book(publicLibrary, **data)

    @staticmethod
    def removeBook(publicLibrary):
        BookID = stringInput("Pleas enter the BookID: ")
        while (BookID not in publicLibrary.catalog.bookDict):
            BookID = input("Please enter a correct BookID.\n")
        publicLibrary.catalog.bookDict.pop(BookID)
        biList = []
        for bi in publicLibrary.catalog.bookItemDict:
            if (publicLibrary.catalog.bookItemDict[bi].book.id == BookID):
                biList.append(bi)
        for i in range(len(biList)):
            publicLibrary.catalog.bookItemDict.pop(biList[i])

    @staticmethod
    def showAllLoanItems(publicLibrary):
        if (publicLibrary.loanAdministation.allLoanItems == {}):
            print("There are no loan items.")
        for i in publicLibrary.loanAdministation.allLoanItems:
            print(i + ": " + publicLibrary.loanAdministation.allLoanItems[i].customerID + "_" + publicLibrary.customers[publicLibrary.loanAdministation.allLoanItems[i].customerID].username + " - " + publicLibrary.loanAdministation.allLoanItems[i].item.id + "_" + publicLibrary.catalog.bookItemDict[publicLibrary.loanAdministation.allLoanItems[i].item.id].book.title)
    
    @staticmethod
    def removeBookLoan(publicLibrary):
        BookItemID = stringInput("Pleas enter the BookItemID: ")
        while (BookItemID not in publicLibrary.catalog.bookitemDict):
            BookItemID = input("Please enter a correct BookItemID.\n")
        publicLibrary.catalog.bookItemDict[BookItemID].taken = False
        publicLibrary.loanAdministation.allLoanItems.pop(BookItemID)

class Customer:
    def __init__(self, publicLibrary, row):
        self.gender = row[1]
        self.nationality = row[2]
        self.firstName = row[3]
        self.surname = row[4]
        self.streetAdress = row[5]
        self.zipCode = row[6]
        self.city = row[7]
        self.email = row[8]
        self.username = row[9]
        self.telephoneNumber = row[10]
        publicLibrary.customers["c" + str(row[0])] = self
    
    @staticmethod
    def searchBook(publicLibrary):
        publicLibrary.catalog.SearchBook(publicLibrary)
    
    @staticmethod
    def loanABook(publicLibrary):
        bookItemID = stringInput("Please enter the bookItemID.")
        while (bookItemID not in publicLibrary.catalog.bookItemDict):
            bookItemID = input("Please enter a correct bookItemID.\n")
        customerID = stringInput("Please enter your customerID.")
        while (customerID not in publicLibrary.customers):
            customerID = input("Please enter a correct cutomerIDn\n")
        publicLibrary.loanAdministation.addLoanItem(publicLibrary, bookItemID, customerID)

class LoanAdministation:
    #allLoans
    def __init__(self):
        self.allLoanItems = {}

    def addLoanItem(self, publicLibrary, bookItemID, customerID):
        if (publicLibrary.catalog.bookItemDict[bookItemID].taken == False):
            LoanItem(publicLibrary, customerID, bookItemID)
            print("The loan has been done.\n")
        else:
            print("This bookitem is taken.\n")

class LoanItem:
    #loaner, item
    def __init__(self, publicLibrary, customerID, itemID):
        self.customerID = customerID
        self.item = publicLibrary.catalog.bookItemDict[itemID]
        self.item.taken = True
        publicLibrary.loanAdministation.allLoanItems[generateLoanItemID()] = self

class Book:
    def __init__(self, publicLibrary, **attributeDict):
        self.id = generateBookID()
        for key in attributeDict:
            if (key != "bookID"):
                setattr(self, key, attributeDict[key])
            else:
                self.id = attributeDict["bookID"]
        publicLibrary.catalog.bookDict[self.id] = self

class BookItem:
    def __init__(self, book, biID = "", taken = ""):
        if (biID == ""):
            self.id = generateBookItemID()
        else:
            self.id = biID
        if (taken == ""):
            self.taken = False
        else:
            self.taken = taken
        self.book = book

class Catalog:
    def __init__(self):
        self.bookDict = {}
        self.bookItemDict = {}
    
    def SearchBook(self, publicLibrary):
        searchAttributes = dict()
        data = input("\nEnter keywords + values(seperated by a ',').\n")
        if (data.split()):
            data = data.split(",")
            if (len(data) > 1 and len(data) % 2 == 0):
                for i in range(0, len(data), 2):
                    searchAttributes[data[i]] = data[i+1]
            else:
                print("Invalid Input")

        a = [id for id in self.bookDict if all(searchAttributes[k] == str(getattr(self.bookDict[id], k)) for k in searchAttributes)]
        print("\Books:")
        for i in range(len(a)):
            print(publicLibrary.catalog.bookDict[a[i]].id + ": " + publicLibrary.catalog.bookDict[a[i]].title)

class Backup:
    @staticmethod
    def CreateBackup(publicLibrary):        
        bookDict = publicLibrary.catalog.bookDict
        bookItemDict = publicLibrary.catalog.bookItemDict
        allLoanItems = publicLibrary.loanAdministation.allLoanItems
        customers = publicLibrary.customers

        ##backupID List
        backupID = ""
        count = 0
        backuplist = Path("C:/temp/backuplist.csv")
        if backuplist.exists():
            with open(backuplist, "r") as f:
                reader = csv.reader(f)
                for _ in reader:
                    count += 1

        with open("C:/temp/backuplist.csv", "a") as f:
            writer = csv.writer(f)
            backupID = "bu" + str(int(count / 2 + 1))
            writer.writerow([backupID, datetime.datetime.now()])

        ##bookBackup
        data = []
        for i in bookDict:
            book = bookDict[i]
            bookAttributes = {"bookID" : book.id ,"author" : book.author, "country" : book.country,  "imageLink" : book.imageLink,  "language" : book.language,  "link" : book.link,   "pages" : book.pages,   "title" : book.title,   "year" : book.year}
            data.append(bookAttributes)
        writeToJSON("C:/temp/" + backupID + "booksset", data)
        
        ##bookItemBackup
        data = []
        for i in bookItemDict:
            bookItem = bookItemDict[i]
            bookItemAttributes = {"id" : bookItem.id, "takenOrNot" : bookItem.taken, "bookID" : bookItem.book.id}
            data.append(bookItemAttributes)
        writeToJSON("C:/temp/" + backupID + "bookitemsset", data)

        ##customerBackup
        with open("C:/temp/" + backupID + "customersset.csv", "w") as f:
            writer = csv.writer(f)
            writer.writerow(["Number", "Gender", "NameSet", "GivenName", "Surname", "StreetAddress", "ZipCode", "City", "EmailAddress", "Username", "TelephoneNumber"])
            data = []
            count = 1
            for i in customers:
                customer = customers[i]
                customerAttributes = [str(count), customer.gender, customer.nationality, customer.firstName, customer.surname, customer.streetAdress, customer.zipCode, customer.city, customer.email, customer.username, customer.telephoneNumber]
                data.append(customerAttributes)
                count += 1
            writer.writerows(data)

        ##loanItemsBackup
        data = []
        for i in allLoanItems:
            loanItem = allLoanItems[i]
            loanItemAttributes = {"customerID" : loanItem.customerID, "bookItemID" : loanItem.item.id}
            data.append(loanItemAttributes)
        writeToJSON("C:/temp/" + backupID + "loanitemsset", data)

    @staticmethod
    def loadFromBackup():
        #check if backup exist
        backuplist = Path("C:/temp/backuplist.csv")
        if not backuplist.exists():
            print("There are no backups!\n")
        else:
            idList = []
            with open("C:/temp/backuplist.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if (row != []):
                        print(row[0] + " - " + row[1])
                        idList.append(row[0])
            backupID = stringInput("Please enter the backupID.")
            while (backupID not in idList):
                input("Invalid backupID, please try again!")

            #start library
            publicLibrary = PublicLibrary()
            publicLibrary.startLibrary(open("C:/temp/" + backupID + "booksset.json", encoding= "UTF8"), (open("C:/temp/" + backupID + "customersset.csv", "r")), open("C:/temp/" + backupID + "loanitemsset.json", encoding= "UTF8"), open("C:/temp/" + backupID + "bookitemsset.json", encoding= "UTF8"))

        #return library
        return publicLibrary

def saveLibrary(publicLibrary):    
    bookDict = publicLibrary.catalog.bookDict
    bookItemDict = publicLibrary.catalog.bookItemDict
    allLoanItems = publicLibrary.loanAdministation.allLoanItems
    customers = publicLibrary.customers

    ##bookSave
    data = []
    for i in bookDict:
        book = bookDict[i]
        bookAttributes = {"bookID" : book.id ,"author" : book.author, "country" : book.country,  "imageLink" : book.imageLink,  "language" : book.language,  "link" : book.link,   "pages" : book.pages,   "title" : book.title,   "year" : book.year}
        data.append(bookAttributes)
    writeToJSON("./booksset", data)
    
    ##bookItemSave
    data = []
    for i in bookItemDict:
        bookItem = bookItemDict[i]
        bookItemAttributes = {"id" : bookItem.id, "takenOrNot" : bookItem.taken, "bookID" : bookItem.book.id}
        data.append(bookItemAttributes)
    writeToJSON("./bookitemsset", data)

    ##customerSave
    with open("./customersset.csv", "w") as f:
        writer = csv.writer(f)
        writer.writerow(["Number", "Gender", "NameSet", "GivenName", "Surname", "StreetAddress", "ZipCode", "City", "EmailAddress", "Username", "TelephoneNumber"])
        data = []
        count = 1
        for i in customers:
            customer = customers[i]
            customerAttributes = [str(count), customer.gender, customer.nationality, customer.firstName, customer.surname, customer.streetAdress, customer.zipCode, customer.city, customer.email, customer.username, customer.telephoneNumber]
            data.append(customerAttributes)
            count += 1
        writer.writerows(data)

    ##loanItemsSave
    data = []
    for i in allLoanItems:
        loanItem = allLoanItems[i]
        loanItemAttributes = {"customerID" : loanItem.customerID, "bookItemID" : loanItem.item.id}
        data.append(loanItemAttributes)
    writeToJSON("./loanitemsset", data)
