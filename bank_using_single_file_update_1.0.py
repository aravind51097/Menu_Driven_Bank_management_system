"""creating menu based Bank management system , all the information has stored in csv file to operate the data
                and all the operation are performed by using holder account number"""

import os
import csv
from pathlib import Path
import re
import sys
import datetime


class Bank:

    def __init__(self):

        print("""

                  ***WELCOME TO THE BANK***
            --->please choose action to perform<---

                1.create a new account
                2.Edit the current details
                3.view the customer details
                4.for transactions
                5.remove your account
                6.exit

        """)

    def main_menu(self):

        """creating main menu and calling the modules according to the user wish"""

        try:

            user = input("Enter your choice : ")
            if user == "1":
                bank.create_account()
            elif user == "2":
                bank.edit_account()
            elif user == "3":
                bank.view_account_details()
            elif user == "4":
                bank.transaction()
            elif user == "5":
                bank.delete_account()
            elif user == "6":
                sys.exit(1)
            else:
                print("incorrect choice please enter valid choice ")
                Bank()
                bank.main_menu()
        except(ValueError, TypeError):
            print("please choice valid option...")
            Bank()
            bank.main_menu()

    def create_account(self):

        """This module creates the account by getting necessary information from the user """

        path = Path("account.csv")  # creating the path where to store all the necessary information

        """ This section takes the all necessary information """

        accNum = int(input("please enter your account number  : "))
        name = input("Enter your name :")
        name = name.title()

        "validating the DOB"

        Date_of_birth = input("Enter Date_Of_Birth as [DD/MM/YYYY] : ")
        try:
            Date_of_birth = datetime.datetime.strptime(Date_of_birth, "%d/%m/%Y")
        except ValueError:
            print("Incorrect Date_of_birth .Please enter valid one")
            sys.exit(1)

        ph_num = input("Enter you Phone_Number :  ")

        "validating the Phone_number"

        regex = "^[6-9][0-9]{9}$"
        if re.match(regex, ph_num):
            pass
        else:
            print("Invalid Phone_number")
            sys.exit(1)

        Aadhaar_number = input("Enter your 12 digit Aadhaar_number : ")

        regex = "^[0-9]{12}$"

        if re.match(regex, Aadhaar_number):
            pass
        else:
            print("invalid Aadhaar")
            sys.exit(1)

        address = input("Enter your current address : ")
        deposit = int(input("enter the deposit amount : "))
        if deposit >= 1000:
            pass
        else:
            print("Sorry..Minimum Deposit is 1000.Try again")
            sys.exit(1)

        account_type = input('choose the account type [current/savings] : ')
        details_of_user = accNum, name, Date_of_birth, ph_num, Aadhaar_number, address, deposit, account_type

        if path.exists():  # if file exists in directory appending the inputs to the file
            file = open("account.csv", 'a+', newline="\r\n")
            writer = csv.writer(file)
            writer.writerow(details_of_user)
            file.close()

        else:  # if file does not exist creating the new file and writing the inputs to the file using csv writer
            file = open("account.csv", 'a+', newline="\r\n")
            writer = csv.writer(file)

            writer.writerow(details_of_user)
            file.close()
        print("""

        do you want to do any other operation...
                    press 1 to continue...
                    press any other key to exit...""")
        con = input("            >>> ")
        if con == "1":
            Bank()
            bank.main_menu()
        else:
            print("exiting........ :-)")

    def edit_account(self):

        """ this module allows user to edit the ph_num and address based on the account number"""

        accNum = input("Enter your account number : ")
        print("""

               1.To change the ph_num
               2.To change the address

               """)
        file = open("account.csv", "r+", newline="\r\n")  # reading the file for data
        read = csv.reader(file)

        """creating the empty file which will store the data remaining users"""

        newfile = open("newaccount.csv", "a+", newline="\r\n")
        writer = csv.writer(newfile)
        choice = int(input("enter choice "))  # input to chose the operation
        if choice == 1:
            for i in read:
                if accNum != i[0]:  # appending the accounts details which are not to operate with
                    writer.writerow(i)
                elif accNum == i[0]:  # fetching the account data
                    print("your ph_num is...", i[3])
                    ph_num = input("please enter your ph_num here : ")
                    i[3] = ph_num  # changing the ph_num and store them into variable
                    writer.writerow(i)  # writing the updated data to file

        elif choice == 2:
            for i in read:
                if accNum != i[0]:
                    writer.writerow(i)
                elif accNum == i[0]:
                    print("your current address is : ", i[5])
                    address = input("enter your current address : ")
                    i[5] = address  # changing the ph_num and store them into variable
                    writer.writerow(i)  # writing the updated data to file

        else:
            print("sorry invalid choice try again :-) ")
            bank.edit_account()

        file.close()
        newfile.close()
        os.remove("account.csv")  # removing the old file
        os.rename("newaccount.csv", "account.csv")  # rename the new file as old file

    def view_account_details(self):

        """this module allows you to view all the details whih regards to user"""

        accNum = input("Enter your account number : ")

        file = open("account.csv", "r+", newline="\r\n")
        read = csv.reader(file)

        for columns in read:

            """ if account number matches with data then fetching the all data which are non 
                                credential to view"""

            if accNum == columns[0]:
                print("""
                    ****account Holder details**** 
                    """)
                print("Account number       : ", columns[0])
                print("Account Holder  name : ", columns[1])
                print("account type         : ", columns[7])
                print("Balance against your passbook :", columns[6])
        file.close()

        print("""
        do you want to see any other details...
                           press 1 for  continue....
                           press any other key to exit....""")
        con = input("                               >>>>")
        if con == "1":
            file.close()

            Bank()
            bank.main_menu()
        else:
            print("exiting........ :-)")

    def transaction(self):

        """All the user transactions are done using this module  """

        accNum = input("Enter your account number : ")
        print("""
        choice the operation to continue with
            1.Balance enquiry
            2.Deposit the amount
            3.Withdrawal of amount
                """)
        file = open("account.csv", "r+", newline="\r\n")  # getting the user details from file
        read = csv.reader(file)
        newfile = open("newaccount.csv", "a+", newline="\r\n")
        writer = csv.writer(newfile)
        choice = int(input("enter choise "))
        if choice == 1:  # fetching the available balance and displaying it to user
            for i in read:
                if accNum == i[0]:
                    print("your balance is :", i[6])
        if choice == 2:  # performing the deposit operation
            for i in read:
                if accNum != i[0]:  # if acc_num doesn't match the appending to the new file
                    writer.writerow(i)
                elif accNum == i[0]:  # if acc_num matches then proceeding
                    deposit = int(input("enter the amount to deposite :  "))
                    total_balance = deposit + int(i[6])
                    print("total balance is :", total_balance)
                    i[6] = str(total_balance)
                    writer.writerow(i)
        if choice == 3:  # performing the withdrawal operation
            for i in read:
                if accNum != i[0]:  # if acc_num doesn't match the appending to the new file
                    writer.writerow(i)
                elif accNum == i[0]:  # if acc_num matches then proceeding
                    withdraw = int(input("enter the amount want to withdraw : "))
                    if withdraw <= int(i[6]):  # operation only allows if withdrawal lesser than the balance
                        total_balance_1 = int(i[6]) - withdraw
                        print("total balance is :", total_balance_1)
                        i[6] = str(total_balance_1)
                    else:
                        print("sorry insufficient funds :-( ")

                    writer.writerow(i)
        else:
            print("please enter valid choice")

        file.close()
        newfile.close()
        os.remove("account.csv")  # removing the old file
        os.rename("newaccount.csv", "account.csv")  # rename the new file as old file

        print("exiting........ :-)")
        return exit(1)

    def delete_account(self):

        """This module deletes the account from the bank"""

        accNum = input("Enter your account number : ")

        print("""Are you sure to remove account
                if yes press 1.. """)

        file = open("account.csv", "r+", newline="\r\n")
        read = csv.reader(file)
        newfile = open("newaccount.csv", "a+", newline="\r\n")
        writer = csv.writer(newfile)
        choice = int(input("enter choice here "))  # confirming from the user to remove the account
        if choice == 1:
            for i in read:
                if accNum != i[0]:  # if account number available then removing it from the database
                    writer.writerow(i)
            print("""

            account successfully removed...
                        Thank you :-)""")
        else:  # if account number not available displaying the message
            print("invalid account number exiting............")
        file.close()
        newfile.close()
        os.remove("account.csv")
        os.rename("newaccount.csv", "account.csv")

        print("""

        do you want to do any other operation...
                           press 1 to continue
                           press any other key to exit..""")
        con = input(">>> ")
        if con == "1":
            file.close()
            newfile.close()
            Bank()
            bank.main_menu()
        else:
            print("exiting........ :-)")


bank = Bank()  # creating the bank object from Bank class
bank.main_menu()  # calling the main menu module in run time
