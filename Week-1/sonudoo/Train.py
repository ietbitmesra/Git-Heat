import requests
class Train:
    """
        This is the class which represents a Train identified by a Train Number
    """
    def __stripWhiteSpaces(self, s):
        #   This method removes spaces in the String except for the Quoted part.
        #   E.g.: 'My name is "S K Gupta"' is converted to 'Mynameis"S K Gupta"'
        l = len(s)
        r = ""
        ok = True
        for i in range(l):
            if (s[i]=='\n' or s[i]==' ' or s[i]=='\t') and ok==True:
                pass
            elif s[i]=='"':
                ok = not ok
                r += s[i]
            else:
                r += s[i]
        return r
    
    def __filterData(self, response):
        """
            This method filters out the Train data fetched from NTES.
        """
        rawTrainData = self.__stripWhiteSpaces(
                        response.text
                        .split('=[ {')[1]
                        .split('rakes')[0]
                        )
        scheduleData = (rawTrainData
                            .split(',trainSchedule:{stations:[{')[1]
                            .split('}]},')[0]
                            .split('},{')
                        )
        basicTrainData = (rawTrainData
                            .split(',trnName')[0]
                            .split(',')
                        )

        basicTrainDataDictionary = {}
        scheduleDataDictionary = {}
        for trainData in basicTrainData:
            try:
                key = trainData.split(':"')[0]
                value = trainData.split(':"')[1]
                value = value[0:len(value)-1]
                basicTrainDataDictionary[key] = value
            except:
                pass
        if 'trainDataFound' in basicTrainDataDictionary:
            del basicTrainDataDictionary['trainDataFound']
        
        if 'prfFlag' in basicTrainDataDictionary:
            del basicTrainDataDictionary['prfFlag']

        tmp = []
        for scheduleDatum in scheduleData:
            d = {}
            for x in scheduleDatum.split(','):
                try:
                    key = x.split(':"')[0]
                    value = x.split(':"')[1]
                    value = value[:len(value)-1]
                    d[key] = value
                except IndexError as e:
                    key = x.split(':')[0]
                    value = x.split(':')[1]
                    d[key] = value
            tmp.append(d)

        self.scheduleData = tmp
        self.trainData = basicTrainDataDictionary

    def __fetchData(self, trainNo):
        """
            This method fetches Train data from NTES
        """
        url = 'https://enquiry.indianrail.gov.in/ntes/SearchTrain?trainNo='+trainNo
        response = requests.get(url)
        cookies = response.headers['Set-Cookie'].split(', ')
        headers = {}
        request_cookies = ""
        for cookie in cookies:
            key, value = cookie.split('; ')[0].split('=')
            request_cookies += key+"="+value+"; "
        headers['Cookie'] = request_cookies[:len(request_cookies)-2]
        url = 'https://enquiry.indianrail.gov.in/ntes/NTES?action=getTrainData&trainNo='+trainNo
        response = requests.get(url, headers=headers)
        return response

    def __init__(self, data):
        self.__filterData(self.__fetchData(data))
    
    def getName(self):
        """
            Returns name of the Train
        """
        return self.trainData['trainName']
    
    def getOrigin(self):
        """
            Returns originating station of the Train
        """
        return self.trainData['from']

    def getDestination(self):
        """
            Returns destination of the Train
        """
        return self.trainData['to']
    
    def getWeekDays(self):
        """
            Returns the week days on which the Train runs
        """
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 
                'Friday', 'Saturday']
        ret = []
        for i in range(len(self.trainData['runsOn'])):
            if self.trainData['runsOn'][i]=='1':
                ret.append(days[i])
        return ret
    
    def getType(self):
        """
            Returns the type of the Train
        """
        return self.trainData['trainType']
    
    def getSchedule(self):
        """
            Returns the schedule of the Train
        """
        ret = []
        for i in self.scheduleData:
            ret.append({'stationCode': i['stnCode'], 
                        'arrivalTime': i['arrTime'], 
                        'departureTime': i['depTime']})
        return ret
    

if __name__ == "__main__":
    trainNo = input("Enter the Train Number: ")
    train = Train(trainNo)
    print(train.trainData)
