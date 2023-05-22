from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidget
from PyQt6.QtCore import Qt

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

        # Liste d'aeroports randoms (venant du pays countryListLayout sélectionné)
        self.__list.addItem("Charles de Gaulle")
        self.__list.addItem("Orly")
        self.__list.addItem("Roissy")
        self.__list.addItem("Beauvais")
        self.__list.addItem("Lyon")

        # Ajout des widgets dans le layout
        self.addWidget(self.__label)
        self.addWidget(self.__list)
