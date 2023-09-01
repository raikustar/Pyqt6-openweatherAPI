import typing
import weatherapi as wapi
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtWidgets import QLabel, QListWidget, QLineEdit, QApplication, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setFixedSize(QSize(800,350))
        self.setWindowTitle("OpenWeather API App")
        #self.setStyleSheet("background-color: snow")

        self.searchLabel = QLabel("Search location: ", self)
        self.searchLabel.setFixedSize(180,40)
        self.searchLabel.move(100,10)
        self.searchLabel.setFont(QFont("Times New Roman", 20))

        self.searchInput = QLineEdit("London",self)
        #self.searchInput.textChanged.connect(self.get)
        self.searchInput.setFont(QFont("Times New Roman", 18))
        self.searchInput.setFixedSize(300,40)
        self.searchInput.move(290,10)

        self.testButton = QPushButton("Search", self)
        self.testButton.clicked.connect(self.get)
        self.testButton.setFont(QFont("Times New Roman", 14))
        self.testButton.setFixedSize(70,40)
        self.testButton.move(600,10)

        self.listWidget = QListWidget()
        self.listWidget.setParent(self)
        self.listWidget.move(1000,500)
        self.listWidget.setWindowFlags(Qt.WindowType.Window)

        self.locationName = QLabel("Location: ", self)
        self.locationName.move(100,50)
        self.locationName.setFixedSize(400,40)

        self.coordLat = QLabel("Latitude:", self)
        self.coordLat.move(300,50)
        self.coordLat.setFixedSize(400,40)

        self.coordLon = QLabel("Longitude:", self)
        self.coordLon.move(500,50)
        self.coordLon.setFixedSize(400,40)

        self.weatherLabel = QLabel("Weather: ", self)
        self.weatherLabel.setFont(QFont("Times New Roman", 18))
        self.weatherLabel.setFixedSize(400,100)
        self.weatherLabel.move(450,80)

        self.tempLabel = QLabel("Temperature: ", self)
        self.tempLabel.setFont(QFont("Times New Roman", 18))
        self.tempLabel.setFixedSize(400,100)
        self.tempLabel.move(50,80)

        self.fLTempLabel = QLabel("Feels: ", self)
        self.fLTempLabel.setFont(QFont("Times New Roman", 18))
        self.fLTempLabel.setFixedSize(400,100)
        self.fLTempLabel.move(270,80)

        self.pressureLabel = QLabel("Air pressure: ", self)
        self.pressureLabel.setFont(QFont("Times New Roman", 14))
        self.pressureLabel.setFixedSize(400,100)
        self.pressureLabel.move(60,130)

        self.humidityLabel = QLabel("Humidity: ", self)
        self.humidityLabel.setFont(QFont("Times New Roman", 14))
        self.humidityLabel.setFixedSize(400,100)
        self.humidityLabel.move(60,160)

        self.visibilityLabel = QLabel("Visibility: ", self)
        self.visibilityLabel.setFont(QFont("Times New Roman", 14))
        self.visibilityLabel.setFixedSize(400,100)
        self.visibilityLabel.move(60,190)

        self.windSpeedLabel = QLabel("Wind speed: ", self)
        self.windSpeedLabel.setFont(QFont("Times New Roman", 14))
        self.windSpeedLabel.setFixedSize(400,100)
        self.windSpeedLabel.move(60,220)

        self.windDirection = QLabel("Wind direction: ", self)
        self.windDirection.setFont(QFont("Times New Roman", 14))
        self.windDirection.setFixedSize(400,100)
        self.windDirection.move(60,250)

        self.weatherIcon = QImage()
        self.weatherIcon.loadFromData(wapi.getIcon("10d"))

        self.weatherImage = QLabel("image", self) 
        self.weatherImage.setPixmap(QPixmap(self.weatherIcon))
        self.weatherImage.setFixedSize(100,100)
        self.weatherImage.move(300,200)
        self.weatherImage.setStyleSheet("border: 1px solid #555; border-radius: 50%")


    def get(self):
        searchText = self.searchInput.text()
        firstSearchResult = wapi.geoCodingApiResult(searchText)
        self.value = firstSearchResult[0]
        self.locationName.setText("Location: " + self.value["name"] + ", " + self.value["country"])
        self.lat = str(self.value["lat"])
        self.lon = str(self.value["lon"])
        self.coordLat.setText("Latitude: " + self.lat)
        self.coordLon.setText("Longitude: " + self.lon)

        self.weatherLabel.setText("Weather: " + self.getValueFromNestDict("weather", "main") + ", " + self.getValueFromNestDict("weather", "description"))
        self.tempLabel.setText("Temperature: " + self.getTemp("main", "temp") + "°C")
        self.fLTempLabel.setText("Feels: " + self.getTemp("main", "feels_like") + "°C")
        self.humidityLabel.setText("Humidity: " + self.getHumidity("main", "humidity") + "%")

        self.pressureLabel.setText("Air pressure: " + self.getValueFromDict("main", "pressure") + " hPa")

        self.visibilityLabel.setText("Visibility: " + self.getVisibility("visibility") + "km")
        
        self.windSpeedLabel.setText("Wind speed: " + self.getWindSpeed("wind", "speed") + "m/s")
        self.windDirection.setText("Wind direction: " + self.getValueFromDict("wind", "deg"))
        self.weatherIcon.loadFromData(self.getWeatherIcon("weather", "icon"))



        # "rain", "1h" 


    def getValueFromNestDict(self,string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        data = getDictResult[string]
        x = 0
        makeDict = dict()
        if x in range(0, len(data)):  
            makeDict[x] = data[x] 
        return makeDict[0][attribute]

    def getHumidity(self, string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat, self.lon)
        ret = round(float(getDictResult[string][attribute]))
        return str(ret)
    
    def getVisibility(self, string):
        getDictResult = wapi.weatherApiRequest(self.lat, self.lon)
        ret = round((getDictResult[string]) / 1000, 2)
        return str(ret)
    
    def getTemp(self, string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        ret = round(float(getDictResult[string][attribute]) * 0.1 ,1) 
        return str(ret)


    def getWindSpeed(self,string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        ret = float(getDictResult[string][attribute]) 
        return str(ret)

    def getWeatherIcon(self, string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        data = getDictResult[string]
        x = 0
        makeDict = dict()
        if x in range(0, len(data)):  
            makeDict[x] = data[x] 

        val = makeDict[0][attribute]
        ret = wapi.getIcon(val)
        return ret

    def getValueFromDict(self,string, attribute):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        ret = float(getDictResult[string][attribute]) 
        return str(ret)
    
    
    def getValueFromNoDict(self,string):
        getDictResult = wapi.weatherApiRequest(self.lat,self.lon)
        ret = round(float(getDictResult[string]) * 0.1, 1)
        return str(ret)
        

# press enter to search

# In app window to show search results
# pick from list of options which then turns into self.value
# create normal QListWidget in app / QSortFilterProxyModel.core

# Wind direction 0-359 converted to compass direction i.e. NW





def main():
    app = QApplication(sys.argv) # [] if no cmd usage

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()



