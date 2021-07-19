from datetime import datetime
import json
import re

transaction_log = "Data/transaction_log.txt"
user_log = "Data/logged_users.txt"
library_file = "Data/library.txt"
transaction_id = 762

def Generate_transaction_id():
    global transaction_id
    transaction_id+=1
    return transaction_id

def Check_user(auth_token):
    """This function checks if the user is logged in."""

    with open(user_log,"r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[0] == str(auth_token):
            return str(auth_token)
    return None

def Book_exists(book_id):
    """This function returns the current book's id if it exists."""

    with open(library_file, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[0] == str(book_id):
            return line[0]
    return None

def Check_book_availability(book_id):
    """This function checks if the current book is available for the transaction."""

    with open(transaction_log, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[2] == str(book_id):
            return False
    return True

def Write_Transaction(auth_token,book_id,borrow_time,transaction_id):
    """This function adds the transaction in transaction_log.txt file."""

    transaction_date = datetime.now().strftime("%d/%m/%Y")
    to_write = auth_token + ";" + str(transaction_id) + ";" + book_id + ";" + str(borrow_time) + ";" + transaction_date + ";" + "\n"
    with open(transaction_log,'a+') as f:
        f.write(to_write)

def Transaction(auth_token,book_id,borrow_time):
    """This function adds a transaction once every criteria is met."""

    book_info = Book_exists(book_id)
    
    if book_id != book_info:
        return "ERROR: Book does not exist in our library!"
    if Check_book_availability(book_id) == False:
        return "ERROR: Book unavailable for transaction!"
    if Check_user(auth_token) != str(auth_token):
        return "ERROR: This user does not exist or is not logged, please login before doing any transactions!"
    if borrow_time <= 0 or borrow_time > 20:
        return "ERROR: Borrow time must be between 1 and 20 days!"

    transaction_id = Generate_transaction_id()
    Write_Transaction(auth_token,book_id,borrow_time,transaction_id)

    json_obj = {
        "Status":"Succsesfull transaction!",
        "Here is your transaction id":transaction_id
    }
    return json_obj

def Get_transaction_info(transaction_id):
    """This function return details about the current transaction_id."""

    with open(transaction_log, "r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[1] == transaction_id:
            result = {
                "auth_token":line[0],
                "transaction_id":line[1],
                "book_id":line[2],
                "borrowed_time":line[3],
                "added_on":line[4]
            }
            return json.dumps(result)
    return False