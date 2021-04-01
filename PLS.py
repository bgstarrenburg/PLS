import classes
#main PLS file


publicLibrary = classes.PublicLibrary()
publicLibrary.startLibrary(open("./booksset.json", encoding= "UTF8"), (open("./customersset.csv", "r")), (open("./loanitemsset.json", encoding= "UTF8")), (open("./bookitemsset.json", encoding= "UTF8")))
 
#Navigation Methods
def customerNavigation():
    global publicLibrary
    ## search for a book, loan a book
    print("\nWhat would you like to do?\n1: Search for a book.\n2: Loan a book.\n3: Exit.")
    choice = classes.choice(["1", "2", "3"])
    while (choice !=3):
        if (choice == 1):
            classes.Customer.searchBook(publicLibrary)
        else:
            classes.Customer.loanABook(publicLibrary)
        print("\nWhat would you like to do?\n1: Search for a book.\n2: Loan a book.\n3: Exit.")
        choice = classes.choice(["1", "2", "3"])
    classes.saveLibrary(publicLibrary)
        

def librarianNavigation():
    global publicLibrary
    ## add a new customer, add a new book item, make a book loan, make a backup, restore from backup
    print("\nWhat would you like to do?.\n1: Show all customers\n2: Add a new customer.\n3: Remove a customer\n4: Look at all books.\n5: Add a book.\n6: Remove a Book\n7: Look at all book items.\n8: Add a new book item.\n9: Remove a book item.\n10: Look at all book loans.\n11: make a new book loan.\n12: Remove a book loan.\n13: Make a backup.\n14: Restore from a backup.\n15: Exit.")
    choice = classes.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",  "11", "12", "13", "14", "15"])
    while (choice != 15):
        if (choice ==1):
            classes.Librarian.showAllCustomers(publicLibrary)
        elif (choice == 2):
            classes.Librarian.addCustomer(publicLibrary)
        elif (choice == 3):
            classes.Librarian.removeCustomer(publicLibrary)
        elif (choice == 4):
            classes.Librarian.showAllBooks(publicLibrary)
        elif (choice == 5):
            classes.Librarian.addBook(publicLibrary)
        elif (choice == 6):
            classes.Librarian.removeBook(publicLibrary)
        elif (choice == 7):
            classes.Librarian.showAllBookItems(publicLibrary)
        elif (choice == 8):
            classes.Librarian.addBookItem(publicLibrary)
        elif (choice == 9):
            classes.Librarian.removeBookItem(publicLibrary)
        elif (choice == 10):
            classes.Librarian.showAllLoanItems(publicLibrary)
        elif (choice == 11):
            classes.Customer.loanABook(publicLibrary)
        elif (choice == 12):
            classes.Librarian.removeBookLoan(publicLibrary)
        elif (choice == 13):
            classes.Backup.CreateBackup(publicLibrary)
        else:
            publicLibrary = classes.Backup.loadFromBackup()
        print("\nWhat would you like to do?.\n1: Show all customers\n2: Add a new customer.\n3: Remove a customer\n4: Look at all books.\n5: Add a book.\n6: Remove a Book\n7: Look at all book items.\n8: Add a new book item.\n9: Remove a book item.\n10: Look at all book loans.\n11: make a new book loan.\n12: Remove a book loan.\n13: Make a backup.\n14: Restore from a backup.\n15: Exit.")
        choice = classes.choice(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",  "11", "12", "13", "14", "15"])
    classes.saveLibrary(publicLibrary)

#UI
print("What role are you?\n1: Customer.\n2: Librarian.")
choice = classes.choice(["1", "2"])

if (choice == 1):
    customerNavigation()
else:
    librarianNavigation()
