from Train import Train
import json, sys, requests
stdout = sys.stdout
while True:
    trainNo = input("Enter the Train Number: ")
    train = ''
    try:
        train = Train(trainNo)
        trainData = {
                    'trainName': train.getName(), 
                    'trainOrigin': train.getOrigin(), 
                    'trainDestination': train.getDestination(), 
                    'trainWeekDays': train.getWeekDays(), 
                    'trainType': train.getType(),
                    'trainSchedule': train.getSchedule()
                    }
        sys.stdout = open(trainNo+'.json', 'w')
        print(json.dumps(trainData))
        sys.stdout = stdout

    except IndexError as e:
        print("No such Train found.")
        continue
    except requests.ConnectionError as e:
        print("Connection Error occurred. Looking for data in local storage..")
        try:
            f = open(trainNo+'.json','r')
            trainData = json.load(f)
            f.close()
        except FileNotFoundError as e:
            print("Internet Connection is required to fetch Train Info.")
            continue
        except json.JSONDecodeError as e:
            print("Internet Connection is required to fetch Train Info.")
            continue
    
    
    print()
    print("Train Name: " + trainData['trainName'])
    print("Origin Station: " + trainData['trainOrigin'])
    print("Destination Station: " + trainData['trainDestination'])
    print("Runs on: " + (', '.join(trainData['trainWeekDays'])))
    print()
    print('STATION\tARRIVAL\t DEPARTURE\n')
    for i in trainData['trainSchedule']:
        print(i['stationCode']+'\t '+
                i['arrivalTime']+'\t  '+
                i['departureTime'])
    print('\nA JSON file named \''+trainNo+'.json\' is saved for reference.')
    print()
