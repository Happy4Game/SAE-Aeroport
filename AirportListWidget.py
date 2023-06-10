from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QListWidget, QLineEdit
from PyQt6.QtCore import pyqtSignal
from BddControler import BddControler

class AirportListWidget(QWidget):
    airportClicked : pyqtSignal = pyqtSignal(str)
    airportSearched : pyqtSignal = pyqtSignal(str)

    """Création du widget contenant la liste des aéroports

    """

    def __init__(self, bdd: BddControler, name : str = "Liste des aeroports", placeHolder : str = "Rechercher un aeroport", showAllAirport : bool = False):
        super().__init__()

        self.bdd = bdd

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Label indiquant la liste des aeroports
        self.__label = QLabel(name)

        # Ligne de saisie de texte
        self.__line_edit : QLineEdit = QLineEdit()
        self.__line_edit.setPlaceholderText(placeHolder)
        self.__line_edit.textChanged.connect(self.airportSearchedFunc)

        self.__list = QListWidget()
        if (showAllAirport):
            self.setAirportList()

        # Ajout des widgets dans le layout
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__line_edit)
        self.__layout.addWidget(self.__list)

        self.__list.itemClicked.connect(self.airportClickedFunc)

        

    def airportClickedFunc(self, item : QListWidget) -> None:
        self.airportClicked.emit(item.text())
    
    def airportSearchedFunc(self) -> None:
        """Emmit the lineEdit text when changed
        """
        self.airportSearched.emit("")
    
    def setAirportByCountry(self, country: str) -> None:
        """Défini la liste des aeroports en fonction du pays

        Args:
            country (str): Nom du pays
        """
        self.__list.clear()
        if self.__list.count() == 0:
            info = self.bdd.getAirportByCountry(country, self.__line_edit.text())
            print(info)
            for airport in range(len(info)):
                self.__list.addItem(info[airport])


    def setAirportList(self) -> None:
        """Défini la liste des aeroports
        """
        self.__list.clear()
        if self.__list.count() == 0:
            info = self.bdd.getAirports(self.__line_edit.text())
            for airport in range(len(info)):
                self.__list.addItem(info[airport])

    def getList(self):
        return self.__list


class AirportSrcListWidget(AirportListWidget):
    def __init__(self, bdd: BddControler, name: str = "Liste des aeroports", placeHolder: str = "Rechercher un aeroport", showAllAirport: bool = False):
        super().__init__(bdd, name, placeHolder, showAllAirport)

    def updateAirportList(self, country) -> None:
        list_airport = self.getList()
        list_airport.clear()

        info = self.bdd.getAirportOnlyWithRoute(country)

        for airport in info:
            list_airport.addItem(airport)

class AirportDestListWidget(AirportSrcListWidget):
    def __init__(self, bdd: BddControler, name: str = "Liste des aeroports", placeHolder: str = "Rechercher un aeroport", showAllAirport: bool = False):
        super().__init__(bdd, name, placeHolder, showAllAirport)

    def updateAirportDestList(self, country_dest: str, airport_src :str) -> None:
        list_airport = self.getList()
        list_airport.clear()

        info = self.bdd.getAirportDestWithRoute(country_dest, airport_src)

        for airport in info:
            list_airport.addItem(airport)