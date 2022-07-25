import requests
import re
import sys
import json
from bs4 import BeautifulSoup

url = "https://www.bankier.pl/waluty/kursy-walut/nbp/USD"
res = requests.get(url)
if(res.status_code == 200):
    found = re.search(".USD.", res.text)
    headerOK = re.search("text\/html.*", res.headers["Content-Type"])
    if((found != None) and (headerOK != None) ):
        soup = BeautifulSoup(res.content, 'html.parser')
        price = soup.select(".profilLast")
        if(len(price)):
            onlynumbers = re.search("[0-9]*,[0-9]+", price[0].get_text())
            if(onlynumbers != None):
                number = onlynumbers.group().replace(",",".")
                usd = float(number)
                print(usd)
                sys.exit(0)

sys.exit(1)