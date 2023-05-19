from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from CountryListLayout import CountryListLayout
from AirportListLayout import AirportListLayout
from AirportInfoWidget import AirportInfoLayout

import sys

class win(QWidget): 
    def __init__(self): 
        super().__init__() 
        self.setWindowTitle("UI Avions")

        self.__mainLayout = QHBoxLayout()

        self.__countryList = CountryListLayout()
        self.__countryList.countryClicked.connect(self.setSelectedCountry)
        self.__mainLayout.addLayout(self.__countryList)

        self.__airportList = AirportListLayout()
        self.__mainLayout.addLayout(self.__airportList)

        self.__airportInfo = AirportInfoLayout()
        self.__mainLayout.addLayout(self.__airportInfo)

        self.setLayout(self.__mainLayout)
        self.show()

    def setSelectedCountry(self, country):
        # On récupère le pays selectionne dans la vue CountryListLayout (country)
        print(country)

if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())