''' 
This is the driver program it takes the train number and start day (optional) to create a json file for the train details.
Train number can be provided as a command line argument or as input in the program
'''


import sys              # To get the input from command line

import Train            # Module which retrivees and stores data of a particluar train

import os , errno       # To make the Train-Details-Json and Train-Details-Json directory (This stores all the json files)


''' Create a new directory if it doesn't exist ''' 
try:
    os.makedirs("Train-Details-Json" ) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.makedirs("Train-Details-CSV" )
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
    
''' Checks if train number was provided in the command line or not '''
if len(sys.argv) > 1:
    train_number = sys.argv[1]
else:
    train_number = input("Enter train number : ")


start_day = "today"
''' Checks if start day was provided in the command line or not '''
if len(sys.argv) > 2:
    start_day = sys.argv[2].strip()


train = Train.Train(train_number = train_number , start = start_day)  # Initialising Train object
train.retrieve_details()                                              # Retrieve Train details
train.store_to_json()                                                 # Store the details in {train number}.json file
train.store_to_csv()                                                  # Store the details in {train number}.json file  
