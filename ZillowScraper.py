import requests
from bs4 import BeautifulSoup
import json
import time
import pandas as pd

def fetch_parse(pages, url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
    df = pd.DataFrame()

    #Iterate over list of urls. See readme for details about URL format.
    for i in range(1,int(pages)+1):
        url = url+str(i)+'_p/'
        soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
        data = json.loads(soup.select_one('script[data-zrr-shared-data-key]').contents[0].strip('!<>-'))

        #List of features desired about each listing
        address = []
        price = []
        beds = []
        baths = []
        area = []

        #Iterate through retrieved data and append desired features to lists
        for result in data['cat1']['searchResults']['listResults']:
            address.append(result['address'])
            price.append(result['price'])
            beds.append(result['beds'])
            baths.append(result['baths'])
            area.append(result['area'])

        #Create dataframe
        d = {'address': address, 'price': price, 'beds': beds, 'baths': baths, 'area': area}
        df = df.append(pd.DataFrame(d))
        time.sleep(5)

    return df

fetch_parse(5,'https://www.zillow.com/la-porte-in/')
