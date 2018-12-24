''' This module is used to get information for a particular train. '''

import bs4             # Beautiful Soup for web scraping.

import requests        # To get the html of a website.

import pandas as pd    # Storing data in CSV file

import json            # Storing data in JSON file

class Train:
    ''' A class which stores and retrieves informations about a Train'''
    
    def __init__(self , train_number = "" , start = "today"):
        ''' Constructor function 
            Parameters :
                train_number - Train number of the train.
                start        - Start day of the train i.e. day when it starts from source station
        '''
        
        self.train_details = {"Train Name" : "-" , "Train Number" : "-" , "Source": "-" , "Destination":"-" , "Start Day" : "-"}
        
        if not train_number.isdigit() or len(train_number) != 5 :
            raise Exception("Invalid Train Number.")
           
        self.train_details["Train Number"] = train_number
        self.train_details["Start Day"] = start
        self.stations = []
        
        
    def retrieve_details(self):
        ''' Retrieves details of the train and its route from https://runningstatus.in/ '''
        
        
        # Retrieving data from the website and creating a bs4 object.
        train_details_runningstatus_webpage = requests.get("https://runningstatus.in/status/{}-{}".format(self.train_details["Train Number"] , self.train_details["Start Day"]))
        train_details_bs4 = bs4.BeautifulSoup(train_details_runningstatus_webpage.text , 'lxml')

        self.train_details["Train Name"] = train_details_bs4.title.text.split('/')[0]
        
        
        ''' Checking if the train number provided is valid or not '''
        if self.train_details["Train Name"] == '':
            raise Exception("Invalid Train Number.")
        
        
        station_fields = ["Station Name" , "Platform" , "Scheduled Arrival" , 
                         "Scheduled Departure" , "Actual Arrival / Departure" ,
                         "Average Speed" , "Train Status"]
        
        ''' Storing the table which contains the station details and then adding all staion data to self.stations. '''
        
        table = train_details_bs4.find("table" , {"class" : "table table-striped table-bordered"})
        
        table_body = table.find('tbody')
        station_details = []
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            station_details.append([ele for ele in cols if ele])
        
        for station in station_details:
            i = 0
            current_station = {}
            for data in station:
                
                current_station[station_fields[i]] = data
                i+=1
            self.stations.append(current_station)
        
        self.train_details["Source"] = self.stations[0]["Station Name"]
        self.train_details["Destination"] = self.stations[-1]["Station Name"]
        
    def store_to_csv(self):
        '''  Stores the details of the train in a csv file in Train-Details-CSV directory. '''
        data_frame = pd.DataFrame(self.stations)

        # Handling Fields that are not present. 
        station_fields = ["Station Name" , "Platform" , "Scheduled Arrival" , 
                         "Scheduled Departure" , "Actual Arrival / Departure" ,
                         "Average Speed" , "Train Status"]
        for field in station_fields:
            if field not in data_frame:
                data_frame[field] = ['' for x in self.stations]
        
        
        data_frame = data_frame[station_fields]  #To place the fields in correct order
        ''' Storing in the csv file '''
        data_frame.to_csv("./Train-Details-CSV/{}.csv".format(self.train_details["Train Number"]) , index = False)
        
    def store_to_json(self):
        ''' Stores the details of the train in a json file in Train-Details-Json directory. '''
        with open("./Train-Details-Json/{}.json".format(self.train_details["Train Number"]) , "w") as output_file:
            json.dump(self.__dict__ , output_file)
            

            