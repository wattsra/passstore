from databaseinterface import *
from passhandler import *
import getpass
from random import randint
##init variables
database = r"pass-store2.db"
#service_name = "test service name"
#service = ("name",str(randint(0,999)))
from datetime import datetime, timedelta
import getpass

####temp variables####
username = "ABCD@gmail.com"
dbpassword = b"1234"  ### need to implement password on database
salt = b'salt_'

def main():

    service_name = input("What service do you want to create?:\n")
    time = now = str(datetime.now().isoformat())
    ###to be implemented
    # if input("Create with current time ({})?\n Choose [Y/N]?\n".format(now)) in ["y","Y",""]:
    #         print("time set = {}".format(time))
    # else:
    #     time = input("What time would you like to set for the creation of this service?:\n")
        ### THIS DOESN'T WORK, NEEDS AMENDING TO USE STRPTIME to take in a string and output as a datetime object
    print("creation date/time set = {}.".format(now))
    #service_id = service_creation(database, (service_name, time))
    service_id = 4
    ## now getting username and password to store
    salt = os.urandom(16)
    usernamehash = hash(dbpassword,getpass.getpass("Input username to store: ").encode(),salt)
    passwordhash = hash(dbpassword,getpass.getpass("Input password to store: ").encode(),salt)
    expiry_time = (datetime.now() + timedelta(days=90)).isoformat()
    ###to be implemented
    # if input("Create with 90 day expiry date ({})?\n Choose [Y/N]?\n".format(ninety_days)) in ["y","Y",""]:
    #         print("expiry set = {}".format(ninety_days))
    #         expiry_time = ninety_days
    # else:
    #     time = input("What time would you like to set for the creation of this service?:\n")
    ### THIS DOESN'T WORK, NEEDS AMENDING TO USE STRPTIME to take in a string and output as a datetime object
    identity = (usernamehash, passwordhash, salt, service_id, time,expiry_time)
    ##store in database
    password_creation(database,identity)
    #print(select_passwords_table(database))
    print("\n\n\n")
    print("Current services saved in the database:\n")
    allservices = select_service_table(database)
    for service in allservices:
        print(service)
    selected_service = input("Which service would you like to get the passwords for?:\n")
    service_id, service_name, usernamehash, passwordhash, salt, expiry_date = select_all_service_passwords(database,selected_service)
    print(dehash(dbpassword,passwordhash,salt))



if __name__ == '__main__':
    main()