import requests as rq
import json as j


# Create web page with python
# 

apiKey = "0c9f8e560a36e989a0b09d6ad1dc3442"
# longitude and latitude factors

# +
def geoCodingApiResult(locationName):
    geoLink = f"http://api.openweathermap.org/geo/1.0/direct?q={locationName}&limit=5&appid={apiKey}"
    checkApi = rq.get(geoLink)
    geoContent = checkApi.json()
    jsonString = j.dumps(geoContent,indent=4)
    data = j.loads(jsonString)
    x = locationName
    locationDict = dict()
    for x in range (0,len(data)):
        locationDict[x] = data[x]
    return locationDict

# +
######### Must be shorter version than this type changing bullshit
def weatherApiRequest(lat, lon):
    setupKey = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={apiKey}"
    checkLink = rq.get(setupKey)
    getJson = checkLink.json()
    dumps = j.dumps(getJson,indent=2)
    newData = j.loads(dumps)
    dictValues = dict(newData)
    return dictValues

  
def getIcon(icon):
    w = f"https://openweathermap.org/img/wn/{icon}@2x.png"
    getW = rq.get(w).content
    return getW

# def writeJsonAndSave():
#     with open("weatherJson.json", mode="w") as outfile:
#         data = weatherApiRequest()
#         outfile.write(data)

def main():
    pass


if __name__ == "__main__":
    main()
