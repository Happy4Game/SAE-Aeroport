from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from Bdd import Bdd

class AirportInfoWidget(QWidget):
    """Création du widget contenant le sinformations des aéroports

    """
    def __init__(self):
        super().__init__()
        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        
        # Labels indiquant les informations de l'aeroport
        self.__label = QLabel("Informations de l'aeroport")
        self.__name = QLabel("Nom : ")
        self.__city = QLabel("Ville : ")
        self.__country = QLabel("Pays : ")
        self.__IATACode = QLabel("Code IATA : ")
        self.__ICAOCode = QLabel("Code ICAO : ")
        self.__latitude = QLabel("Latitude : ")
        self.__longitude = QLabel("Longitude : ")
        self.__altitude = QLabel("Altitude : ")
        self.__timezone = QLabel("Timezone : ")
        
        # Ajout des widgets dans le layout
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__name)
        self.__layout.addWidget(self.__city)
        self.__layout.addWidget(self.__country)
        self.__layout.addWidget(self.__IATACode)
        self.__layout.addWidget(self.__ICAOCode)
        self.__layout.addWidget(self.__latitude)
        self.__layout.addWidget(self.__longitude)
        self.__layout.addWidget(self.__altitude)
        self.__layout.addWidget(self.__timezone)
        
        # Initialisation des valeurs des labels
        self.labels = [self.__name, self.__city, self.__country, self.__IATACode, self.__ICAOCode, self.__latitude, self.__longitude, self.__altitude, self.__timezone]
        self.initialTexts = [label.text() for label in self.labels]

    def setInfoByAeroport(self, airport: str):
        bdd = Bdd()
        info = bdd.getInfoByAirport(airport)
        
        for label, initialText in zip(self.labels, self.initialTexts):
            label.setText(initialText)  # Réinitialisation du texte avant mise à jour

        for label, value in zip(self.labels, info):
            label.setText(label.text() + str(value))
            
        bdd.closeConnection()
