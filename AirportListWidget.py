from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSignal
from Bdd import Bdd

class AirportListWidget(QWidget):
    airportClicked : pyqtSignal = pyqtSignal(str)

    """Création du widget contenant la liste des aéroports

    """

    def __init__(self):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Label indiquant la liste des aeroports
        self.__label = QLabel("Liste des aeroports")

        self.__list = QListWidget()

        # Liste d'aeroports randoms (venant du pays countryListLayout sélectionné)
        # self.__list.addItem("Charles de Gaulle International Airport")
        # self.__list.addItem("Orly")
        # self.__list.addItem("Roissy")
        # self.__list.addItem("Beauvais")
        # self.__list.addItem("Lyon")

        # Ajout des widgets dans le layout
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__list)

        self.__list.itemClicked.connect(self.airportClickedFunc)

        

    def airportClickedFunc(self, item : QListWidget):
        self.airportClicked.emit(item.text())
    
    def setAeroportByCountry(self, country: str):
        self.__list.clear()
        if self.__list.count() == 0:
            bdd = Bdd()
            info = bdd.getAirportByCountry(country)
            print(info)
            for airport in range(len(info)):
                self.__list.addItem(info[airport])
                
            bdd.closeConnection()
