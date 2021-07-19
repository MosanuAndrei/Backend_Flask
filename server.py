from flask import Flask, request
from datetime import datetime
import register_and_login
import book_management
import library_interactions
import json

app = Flask(__name__)

@app.route("/register", methods = ["POST"])
def Register_user():
    if request.method == "POST":
        data = request.get_json()
        last_name = data["last_name"]
        first_name = data["first_name"]
        email = data["email"]
        password = data["password"]
        user_type = data["user_type"]
        return register_and_login.Add_user(last_name,first_name,email,password,user_type)
    else:
        return "Only POST works here!"

@app.route("/login", methods = ["POST"])
def Login_user():
    if request.method == "POST":
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        return register_and_login.Login_user(email,password)
    else:
        return "Only POST works here!"

@app.route('/add/book',methods = ["POST"])
def Add_book():
    if request.method == "POST":
        data = request.get_json()
        auth_token = data["auth_token"]
        book_name = data["book_name"]
        book_author = data["book_author"]
        book_description = data["book_description"]
        return book_management.Add_book(auth_token,book_name,book_author,book_description)
    else:
        return "Only POST works here!"

@app.route('/add/books',methods = ["POST"])
def Add_books():
    if request.method == "POST":
        data = request.get_json()
        auth_token = data["auth_token"]
        books = data["books"]
        return book_management.Add_books(auth_token,books)
    else:
        return "Only POST works here!"

@app.route('/get/book',methods = ["GET"])
def Get_book():
    if request.method == "GET":
        data = request.get_json()
        book_id = data["book_id"]
        return book_management.Get_book(book_id)
    else:
        return "Only GET works here!"

@app.route('/get/books',methods = ["GET"])
def Get_books():
    if request.method == "GET":
        return book_management.Get_books()
    else:
        return "Only GET works here!"

@app.route("/transaction", methods = ["POST"])
def add_transaction():
    if request.method == "POST":
        data = request.get_json()
        auth_token = data["auth_token"]
        book_id = data["book_id"]
        borrow_time = data["borrow_time"]
        return library_interactions.Transaction(auth_token,book_id,borrow_time)
    else:
        return "Only POST works here!"

@app.route("/transaction/status", methods = ["GET"])
def Get_transaction_info():
    if request.method == "GET":
        data = request.get_json()
        transaction_id = data["transaction_id"]
        return library_interactions.Get_transaction_info(transaction_id)
    else:
        return "Only GET works here!"

if __name__ == "__main__":
    app.run(debug=True)