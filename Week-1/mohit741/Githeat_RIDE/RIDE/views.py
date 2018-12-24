import requests
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
import pandas as pd
import json


def index(request):
    # Dict to store all information
    data = {}
    if request.method == 'POST':
        train_no = str(request.POST['trainno']).strip()

        # Check if train number is valid or not
        if not is_valid(train_no):
            return render(request, 'index.html', {'err': 'Train number not valid'})

        # Urls used for scraping
        url1 = 'https://www.cleartrip.com/trains/' + train_no
        url2 = 'https://erail.in/train-fare/' + train_no + '?query=' + train_no

        try:
            r1 = requests.get(url1)
            r2 = requests.get(url2)
        except Exception as e:
            err = e.args[0]
            return render(request, 'index.html', {'err': err})

        try:
            # BeautifulSoup object
            soup = BeautifulSoup(r1.text, 'html.parser')
            train = soup.find('h1').text.split('\n')[1].strip()
            train_meta = soup.find('h1').text.split('\n')[4].strip()
            train_name = train + ' ' + train_meta
            table = soup.find('table', class_='results')
        except Exception as e:
            err = e.args[0]
            if e.args[0] == 'list index out of range':
                err = 'Train number not valid'
            return render(request, 'index.html', {'err': err})

        # Pandas DataFrame object
        df = pd.read_html(str(table))

        # DataFrame to JSON string
        res = df[0].to_json()
        data['train_name'] = train_name
        data['stations'] = json.loads(res)
        li = soup.find('ul', class_='list-unstyled info-summary').find_all('li')

        # Dict to store details
        details = {}
        for i in range(0, 2):
            key = li[i].text.split(':')[0]
            value = li[i].text.split(':')[1]
            details[key.strip()] = value.strip()

        span = li[2].find_all('span')
        for i in range(0, len(span)):
            key = span[i].text.split(':')[0]
            value = span[i].text.split(':')[1]
            details[key.strip()] = value.strip()
        data['details'] = details
        soup = BeautifulSoup(r2.text, 'html.parser')
        table = soup.find('div', class_='panel panel-warning').find('table')
        df = pd.read_html(str(table))
        res = df[0].to_json()
        data['fare'] = json.loads(res)

        # Store JSON string in session variable
        request.session['train'] = json.dumps(data)
        return redirect('/details')

    else:
        return render(request, 'index.html', {'err': ''})


def train_details(request):
    if not request.session['train']:
        return redirect('/')

    # Get JSON data back
    json_data = request.session['train']

    # Load it to a dictionary
    data = json.loads(json_data)
    name = data['train_name']
    stations = data['stations']
    fares = data['fare']
    details = data['details']
    return render(request, 'details.html', {'name': name, 'stations': stations, 'fares': fares, 'details': details})


# Download JSON file
def download_json(request):
    json_string = request.session['train']
    response = HttpResponse(json_string, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename=train_info.json'
    return response


# Check validity of train number
def is_valid(train_no):
    if len(train_no) != 5:
        return False

    # Check if it is number
    try:
        int(train_no)
    except Exception:
        return False
    return True
