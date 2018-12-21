
# coding: utf-8

# In[10]:


import bs4 as bs
import urllib.request
import pandas as pd
from selenium import webdriver


url = 'https://www.cleartrip.com/trains/'
x = input() #Takes train number as input in the variable x
finalUrl = url + x + '/'

sauce = urllib.request.urlopen(finalUrl).read()

soup = bs.BeautifulSoup(sauce,'lxml')
trainDetails = soup.h1.text

print('Train Details: ',trainDetails)

for spans in soup.find_all('span' , class_ = 'days-op'):
    print('Operational Days: ', spans.text)

df1=pd.read_html(finalUrl, header=0)[0]
out = df1.to_json(orient = 'records')

print(out, '\n\n\n\n\n')
print(df1[['Station name (code)', 'Arrives', 'Departs', 'Stop time',
            'Distance travelled', 'Day', 'Route']])

driver = webdriver.Firefox() #Opens the site from where information
driver.get(finalUrl)         #is taken.

