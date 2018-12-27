# Githeat_RIDE
Django Web-app for IET, BIT, Mesra's 4-week challenge GitHeat.

----------------- <b>RIDE</b> ---------------------
<br>
This Web-App provides details of trains using 5-digit train number. Details include stoppages, classes, pantry service and fares. 
<br>
Using <b>python 3.6</b>
<br>
Web scraping is done using BeautifulSoup and HTML tables are converted to dictionary format using 'pandas' library.
<br>
All web scraping logic is inside 'views.py' module in RIDE folder.
<br>

Websites scraped :
<br>
1. cleartrip.com
<br>
2. erail.in
<br>

To use follow the steps:

1) Install all required python packages using command "pip install -r requirements.txt". Open command line or bash in cloned directory.
( It's better if you use virtualenv )
2) Run command "python manage.py runserver" in same directory where 'manage.py' exists.
3) Open http://127.0.0.1:8000

That's it.

It stores JSON string in a session variable in 'tmp' folder. You can also download the JSON file by using the 
download button in details page.
