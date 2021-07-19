from datetime import datetime
import json

user_log = "Data/logged_users.txt"
library_file = "Data/library.txt"
users_type = [0,1]
book_id = 456

def Book_exists(book_name):
    with open(library_file,'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[1] == book_name:
            return True
    return False

def Check_user(auth_token):
    """This function checks if the user is logged in using his auth_token . """

    with open(user_log,'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[0] == auth_token:
            if line[2] == "1":
                return True
    return False

def Generate_book_id():
    global book_id
    book_id+=1
    return book_id

def Write_book(book_name,book_author,book_description):
    """This function writes a book in library.txt file found in Data folder."""

    added_on = datetime.now().strftime("%d/%m/%Y")
    id = Generate_book_id()
    to_write = str(id) + ";" + book_name + ";" + book_author + ";" + book_description + "\n"
    with open(library_file,'a+') as f:
        f.write(to_write)

def Add_book(auth_token,book_name,book_author,book_description):
    """This function adds a new book once every criteria is met."""

    if Check_user(auth_token) == False:
        return "ERROR: Invalid User!"
    if Book_exists(book_name) == True:
        return "ERROE: Book already exists in our library!"
    
    Write_book(book_name,book_author,book_description)
    return "Book added successfully!"

def Write_books(books_dict):
    """This function writes a bunch of book in library.txt file found in Data folder."""

    added_on = datetime.now().strftime("%d/%m/%Y")
    for book in books_dict.items():
        for elem in book[1]:
            id = Generate_book_id()
            to_write = str(id) + ";" + elem["book_name"] + ";" + elem["book_author"] + ";" +elem["book_description"] + ";" +"\n"
            with open(library_file,'a+') as f:
                f.write(to_write)

def Add_books(auth_token, books):
    """This function adds a bunch of books once every criteria is met."""

    if Check_user(auth_token) != True:
        return "ERROR: Invalid user!"

    books = json.dumps(books)
    books_dict = json.loads(books)
    for book in books_dict.items():
        for elem in book[1]:
            if Book_exists(elem["book_name"]) == True:
                return "ERROR: One of the books already exists in our library!"

    Write_books(books_dict)

    return "Books added succesfully!"

def Get_book(book_id):
    """This function returns a book using the book's id."""

    with open(library_file,'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[0] == book_id:
            result = {
                "book_id":line[0],
                "book_name":line[1],
                "book_author":line[2],
                "book_description":line[3]
            }
            return json.dumps(result)
    return "ERROE: Book does not exist in our library!"

def Get_books():
    """This function returns all the books from the library."""

    library = []
    
    with open(library_file,'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        for i in range(len(lines)):
            result = {
                "book":[{
                    "book_id":line[0],
                    "book_name":line[1],
                    "book_author":line[2],
                    "book_description":line[3]
                }]
            }
        library.append(result)
    return json.dumps(library)