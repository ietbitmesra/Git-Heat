#Input : A 5 digit train number
#Output: A file containing JSON of the train's schedule.

import json
from bs4 import BeautifulSoup
import urllib.request
import os

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data)


train_number = input('Enter train number\n') #Input 5 digit train number
train_schedule_url = 'https://enquiry.indianrail.gov.in/xyzabc/ShowTrainSchedule?trainNo=' + str(train_number) # generates url

train_schedule_read = BeautifulSoup(urllib.request.urlopen(train_schedule_url), 'html.parser')

train_name = train_schedule_read.find('div', {'class': 'w3-col s9 m7 l6 mexTrn'}).text.replace('?', '').strip() #Stores train name
train_route = train_schedule_read.findAll('tr', {'class' : 'altRow'})

serial_number = 1
length = len(train_route)

information = []

for station in train_route: #scrapes the table

    info = station.findAll('td')

    station_details = info[1].text.split()
    station_name = station_details[0]
    station_code = station_details[1]

    times = station.findAll('span', {'class' : 'arrDepTime ui-state-default'})

    arrival_time = ""
    departure_time = ""

    distance = info[4].text

    if (serial_number == 1):
        departure_time = times[0].text
    elif (serial_number == length):
        arrival_time = times[0].text
    else:
        arrival_time = times[0].text
        departure_time = times[1].text

    data = {'Station Name': station_name, 'Station Code': station_code, 'Arrival Time': arrival_time, 'Departure Time': departure_time, 'Distance': distance}
    information.append(data)

    serial_number = serial_number + 1

if not os.path.exists('Train Routes'):
    os.mkdir('Train Routes')

with open('./Train Routes/' + train_name + '.json', 'w') as outfile:
    json.dump(information, outfile)
