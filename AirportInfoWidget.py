from PyQt6.QtWidgets import QLabel, QVBoxLayout

class AirportInfoLayout(QVBoxLayout):
    """Création du layout contenant le sinformations des aéroports

    Args:
        QVBoxLayout (QtWidgets): Layout vertical
    """
    def __init__(self):
        super().__init__()
        # Labels indiquant les informations de l'aeroport
        self.__label = QLabel("Informations de l'aeroport")
        self.__name = QLabel("Nom : ")
        self.__IATACode = QLabel("Code IATA : ")
        self.__ICAOCode = QLabel("Code ICAO : ")
        self.__radioCode = QLabel("Code radio : ")
        self.__location = QLabel("Lieu : ")

        # Ajout des widgets dans le layout
        self.addWidget(self.__label)
        self.addWidget(self.__name)
        self.addWidget(self.__IATACode)
        self.addWidget(self.__ICAOCode)
        self.addWidget(self.__radioCode)
        self.addWidget(self.__location)

