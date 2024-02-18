import geopy
import urllib.request
import re
from bs4 import BeautifulSoup
import pandas as pd

#uses latitude and longitude to get DNO 
geo_locator = geopy.Nominatim(user_agent='something_other')

data_df = pd.read_excel("coord_output.xlsx")

df_length = len(data_df['Name'])

southwest_postcode = [0]*df_length
northeast_postcode = [0]*df_length

for i in range(df_length):

    southwest = geo_locator.reverse((data_df['Southwest Lat'][i], data_df['Southwest Long'][i]))
    northeast = geo_locator.reverse((data_df['Northeast Lat'][i], data_df['Northeast Long'][i]))

    southwest_postcode[i] = southwest.raw['address']['postcode']
    northeast_postcode[i] = northeast.raw['address']['postcode']

#r = geo_locator.reverse((50.880,-2.493))

postcode_data = {'Southwest Postcode': southwest_postcode, 'Northeast Postcode': northeast_postcode}

data_df = data_df.assign(**postcode_data)

for j in range(len(southwest_postcode)):

    southwest = southwest_postcode[j].replace(' ', '+')
    northeast = northeast_postcode[j].replace(' ', '+')
    
    southwest_postcode[j] = southwest
    northeast_postcode[j] = northeast
 
print(southwest_postcode, '\n', northeast_postcode)

#post_code = s_post_code[:3]+ '+' + s_post_code[4:]

southwest_dno = [0]*df_length
northeast_dno = [0]*df_length

for i in range(df_length):

    dno_url = 'https://www.ssen.co.uk/distributor-results/Index?distributorTerm=' + southwest_postcode[i]

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(dno_url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)

    html = response.read().decode('UTF-8')

    soup = BeautifulSoup(html, "html.parser")

    label_result = soup.find("dd", {"class":"c-results-list__value"})

    try:
        southwest_dno[i] = label_result.get_text()
    except AttributeError:
        southwest_dno[i] = 'N/A'

for j in range(df_length):

    dno_url = 'https://www.ssen.co.uk/distributor-results/Index?distributorTerm=' + northeast_postcode[j]

    user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

    headers={'User-Agent':user_agent,} 

    request=urllib.request.Request(dno_url,None,headers) #The assembled request
    response = urllib.request.urlopen(request)

    html = response.read().decode('UTF-8')

    soup = BeautifulSoup(html, "html.parser")

    label_result = soup.find("dd", {"class":"c-results-list__value"})

    try:
        northeast_dno[j] = label_result.get_text()
    except AttributeError:
        northeast_dno[j] = 'N/A'

dno_data = {'Southwest DNO': southwest_dno, 'Northeast DNO': northeast_dno}

data_df = data_df.assign(**dno_data)

data_df.to_excel("DNO_output.xlsx")

