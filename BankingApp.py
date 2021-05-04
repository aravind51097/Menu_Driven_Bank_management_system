# Menu drive banking app
# PAN number is considered as Primary key for all banking operations
# Customer Name,Account Number,Balance, Date of Birth, Phone Number, Address are stored as customer details

import datetime
import os,sys
import re
import random
import csv
import pandas as pd

def create_acc():
    custName = input("Enter the account holderr name: ")
    custName = custName.title()

    # input validation for date to check if in DD/MM/YYYY format
    dob = input("Enter the date of birth in format DD/MM/YYYY: ")
    try:
        d_o_b = datetime.datetime.strptime(dob, "%d/%m/%Y")
    except:
        print("Incorrect date!")
        sys.exit(1)

    # input data validation to check if phone number is 10 digits and starts with 91 or 0
    phnum = input("Enter phone number: ")
    regex= "^(0|91)?[7-9][0-9]{9}$"
    if re.match(regex,phnum):
        pass
    else:
        print("Invalid phone number")
        sys.exit(1)
        
    # input validation to check if PAN is valid
    pan = input("Enter PAN number: ")
    regex1 = "[A-Z]{5}[0-9]{4}[A-Z]{1}"
    if re.match(regex1,pan):
        pass
    else:
        print("Invalid PAN")
        sys.exit(1)
    
    address = input("Enter address: ")

    balance = int(input("Enter a minimum deposit amount of 1000: "))

    # generate a 7 digit unique and random account number
    account_no = int(''.join(random.sample('0123456789', 5)))+int(''.join(random.sample('0123456789', 7)))

    customer_details = [custName,account_no,balance,dob,phnum,pan,address]
    
    with open(r'bank_details.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(customer_details)
    
    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()
1
    
def deposit_amt():

    pan = input("Enter your PAN number: ")
    
    deposit_amt = int(input("Enter the amount to be deposited: "))
    
    df = pd.read_csv("bank_details.csv")

    current_balance = df.loc[df['PAN'] == pan ,'Balance']
    print("Current Balance: ",current_balance)

    add_balance = int(current_balance) + int(deposit_amt)

    df.loc[df["PAN"] == pan, "Balance"] = add_balance

    df.to_csv("bank_details.csv", index=False)

    new_balance = df.loc[df['PAN'] == pan ,'Balance']
    # convert the data frame output to string to remove Name and dtype columns
    print("New Balance: ",new_balance.to_string(index=False))    
    
    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()
   

def withdraw_amt():
    pan = input("Enter your PAN number: ")
    
    withdraw_amt = int(input("Enter the amount to withdraw: "))
    
    df = pd.read_csv("bank_details.csv")

    current_balance = df.loc[df['PAN'] == pan ,'Balance']
    print("Current Balance: ",current_balance)

    # check if the amount entered doesnt exceed the current balance, abort withdrawal operation
    
    if int(current_balance) >= int(withdraw_amt):
        deduct_balance = int(current_balance) - int(withdraw_amt)
    else:
        print("WARNING: Insufficient balance in account to withdraw..!!!")
        sys.exit(1)        

    df.loc[df["PAN"] == pan, "Balance"] = deduct_balance

    df.to_csv("bank_details.csv", index=False)

    new_balance = df.loc[df['PAN'] == pan ,'Balance']
    print("New Balance: ",new_balance.to_string(index=False))    
    
    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()

def balance_enquiry():
    pan = input("Enter your PAN number: ")

    df = pd.read_csv("bank_details.csv")

    current_balance = df.loc[df['PAN'] == pan ,'Balance']
    print("Currently you balance is : ",current_balance.to_string(index=False))

    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()

def modify_acc_det():
    pan = input("Enter your PAN number: ")

    df = pd.read_csv("bank_details.csv")

    print("(1)Phone Number")
    print("(2)Address")
    
    c = int(input("Enter choice to modify account details: "))

    if c == 1:
        new_phone_num = input("Enter the phone number to be updated: ")
        df.loc[df["PAN"] == pan, "Phone Number"] = new_phone_num
        df.to_csv("bank_details.csv", index=False)
        
    elif c ==2:
        new_address = input("Enter you new residence address to be updated: ")
        df.loc[df["PAN"] == pan, "Address"] = new_address
        df.to_csv("bank_details.csv", index=False)
    else:
        print("Invalid Option...Exiting \n")
        sys.exit(1)

    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()
    

def close_acc():
    pan = input("Enter your PAN number: ")

    df = pd.read_csv("bank_details.csv")

    current_balance = df.loc[df['PAN'] == pan ,'Balance']

    # delete/close an account only if the currect balance is nil
    
    if (current_balance.to_string(index=False)) > '0':
        print("Cannot close account, as account has more than zero balance. Do appropriate withdrawal \n")
    else:
        print("Closing account")        
        df = pd.read_csv("bank_details.csv", index_col = "PAN")
        df.drop([pan], inplace = True)
        df.to_csv("bank_details.csv", index=False)

        
    print("Do you want to perform any other operation? (y / n)")
    choice = input().strip()
    if choice == "y":
        main()
    

# Main Function for Menu-Driven
def main():   
    
    
    print("(1)Create New Account")
    print("(2)Deposit")
    print("(3)Withdrawal")
    print("(4)Balance Enquiry")
    print("(5)Modify Account Details")
    print("(6)Close Account")

    choice = int(input("Enter choice: "))
       
    choice_dict = {
        1: create_acc,
        2: deposit_amt,
        3: withdraw_amt,
        4: balance_enquiry,
        5: modify_acc_det,
        6: close_acc,
    }
       
    choice_dict[choice]()
  
  
if __name__ == "__main__":
    print("----------------------Welcome to Banking App----------------------")
  
main() 
