# The Ride

A program which retrieves information of a train (Indian Railways) from the internet and stores the data in a .json file.

# Language 
1. Python

# Packages Used
1. Beautiful Soup
2. Requests
3. Pandas
4. Json

# How to use?
There are two ways to use this program.
1. From Command Line - Run the program from the command line in the following way
               
               \> py Train_Schedule.py <train_number> <start day>

(Instead of py use the command for running python files.)
train_number - This is a five digit train number.
    If train number is not provided it will ask for it during runtime.
Start day - It is the day when train starts from source station.(Ex - today , yesterday , etc.)
    If start day is not provided, start day will be considered today

2. Open the Train_Schedule.py file by double clicking and enter the train number.

# Output
1. A {train_number}.json file which contains all the informations regarding the train.
2. A {train_number}.csv file which contains a spreadsheet of the stations the train stops at.


(Make sure you have an active internet connection and the packages mentioned above.)