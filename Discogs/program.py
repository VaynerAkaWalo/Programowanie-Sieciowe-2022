import requests
import time
import re
import sys
import json

address = 'https://api.discogs.com/artists/'

def requestDiscogs(id):
    request = address + str(id)
    res = requests.get(request)
    if(res.status_code == 429):
        return 429
    if(res.status_code == 200):
        found = re.search(".\"name\".", res.text)
        headerOK = re.search("application\/json", res.headers["Content-Type"])
        if((found != None) and (headerOK != None)):
            return res.text     
    sys.exit(1)

def dictsort(e):
    return idDict[e]

idDict = {}
bandDict = {}


if len(sys.argv) != 2:
    print("Nie prawidłowa liczba argumentów")
    sys.exit(1)

bandId = sys.argv[1]

for _ in range(1):
    res = requestDiscogs(bandId)
    if(res == 429):
        time.sleep(60)
        continue
    jsonText = json.loads(res)
    if(len(jsonText['members'])):
        for member in jsonText['members']:
                idDict[member['id']] = member['name']

        keys = list(idDict.keys())
        for id in keys:
            i = 0
            res = 429
            while 1:
                res = requestDiscogs(id)
                if(res == 429):
                    time.sleep(60)
                else:
                    break
            jsonText = json.loads(res)
            if(len(jsonText['groups'])):
                for group in jsonText['groups']:
                    if(bandDict.get(group['id'], 0) == 0):
                        memberSet = {id}
                        bandDict[group['id']] = memberSet
                    else:
                        x = bandDict[group['id']]
                        x.add(id)
                        bandDict[group['id']] = x
                    idDict[group['id']] = group['name']
        bandDict.pop(int(bandId))
        keys = list(bandDict.keys())
        keys.sort(key = dictsort)
        for key in keys:
            x = list(bandDict[key])
            if len(x) > 1:
                string = ""
                for member in x:
                    string += str(idDict[member]) + ", "
                string += "grali razem w zespole: " + str(idDict[key])
                print(string)
sys.exit(1)
