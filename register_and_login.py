from datetime import datetime
import json
import re
import hashlib

users_file = "Data/users.txt"
user_log = "Data/logged_users.txt"
auth_token = 123
users_type = [0,1]

def Email_exists(email):
    with open(users_file,"r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if email == line[0]:
            return True
    return False

def Check_email(email):
    """This function checks if the email structure is soemthing@something.something . """
    
    regex = "^\w+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$"
    result = re.findall(regex,email)
    return bool(result)

def Check_password(password):
    """This function checks if password contains at least 8 characters, at least one letter and one special character."""
    
    regex = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
    result = re.findall(regex,password)
    return bool(result)
    
def Encrypt_password(password):
    enq_pass = hashlib.sha256(password.encode()).hexdigest()
    return enq_pass
    
def Write_user(last_name,first_name,email,password,user_type):
    """This function writes the user in users.txt file found in Data folder."""

    enq_pass = Encrypt_password(password)
    created_on = datetime.now().strftime("%d/%m/%Y")
    to_write = email + ";" + enq_pass + ";" + last_name + ";" + first_name + ";" + str(user_type) + ";" + created_on + "\n"
    with open(users_file,"a+") as f:
        f.write(to_write)
        
def Add_user(last_name,first_name,email,password,user_type):
    """This function adds a new user once every criteria is met."""

    if Email_exists(email) == True:
        return "ERROR: User already exists!"
    if Check_email(email) == False:
        return "ERROR: Invalid email!"
    if Check_password(password) == False:
        return "ERROR: Invalid password! Minimum eight characters, at least one letter, one number and one special character!"
    if user_type not in users_type:
        return "ERROR: User Type does not exist!"
    
    Write_user(last_name,first_name,email,password,user_type)
    return "User added succesfully"      

def Generate_token():
    global auth_token
    auth_token+=1
    return auth_token

def Get_user_info(email):
    """This function return a json with the user's password, user type and when it was created."""

    with open(users_file,"r") as f:
        lines = f.readlines()
    for line in lines:
        line = line.split(";")
        if line[0] == email:
            result = {
                "password":line[1],
                "user_type":line[4],
                "created_on":line[5]
            }
            return result
    return None

def Write_user_log(email,user_type,auth_token):
    """This function writes the 'logged' user in a new file log_users.txt found in Data folder. """

    logged_on = datetime.now().strftime("%d/%m/%Y")
    to_write =str(auth_token) + ";" + email + ";" + str(user_type) + ";" + logged_on + "\n"
    with open(user_log,"a+") as f:
        f.write(to_write)

def Login_user(email,password):
    """This function 'logs in' the user by giving him the auth_token."""

    if Email_exists(email) == False:
        return "ERROR: No user with this email exists!"
    info = Get_user_info(email)
    if Encrypt_password(password) != info["password"]:
        return "ERROR: Wrong Password!"

    auth_token = Generate_token()
    Write_user_log(email,info["user_type"],auth_token)
    
    current_user = {
        "Login Status":"Success",
        "Here is your authentication token":auth_token
    }
    return json.dumps(current_user)