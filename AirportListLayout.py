from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidget
from PyQt6.QtCore import Qt
from Bdd import Bdd

class AirportListLayout(QVBoxLayout):
    """Création du layout contenant la liste des aéroports

    Args:
        QVBoxLayout (QWidget): Layout vertical
    """

    def __init__(self):
        super().__init__()

        # Label indiquant la liste des aeroports
        self.__label = QLabel("Liste des aeroports")

        self.__list = QListWidget()


        # Ajout des widgets dans le layout
        self.addWidget(self.__label)
        self.addWidget(self.__list)

    
    def setAirportListByCountry(self, country : str):
        """Définit la liste des aéroports récupérés dans la vue CountryListLayout pour la vue AirportListLayout

        Args:
            country (str): Pays pour lequel on veut récupérer les aéroports
        """
        bdd = Bdd()
        listAirport = bdd.getAirportByCountry(country)
        bdd.closeConnection()

        self.__list.clear()

        for airport in listAirport:
            self.__list.addItem(airport)