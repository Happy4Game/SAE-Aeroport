from PyQt6.QtWidgets import QLabel, QVBoxLayout
from Bdd import Bdd

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
        self.__city = QLabel("Ville : ")
        self.__country = QLabel("Pays : ")
        self.__IATACode = QLabel("Code IATA : ")
        self.__ICAOCode = QLabel("Code ICAO : ")
        self.__latitude = QLabel("Latitude : ")
        self.__longitude = QLabel("Longitude : ")
        self.__altitude = QLabel("Altitude : ")
        self.__timezone = QLabel("Timezone : ")
        

        # Ajout des widgets dans le layout
        self.addWidget(self.__label)
        self.addWidget(self.__name)
        self.addWidget(self.__city)
        self.addWidget(self.__country)
        self.addWidget(self.__IATACode)
        self.addWidget(self.__ICAOCode)
        self.addWidget(self.__latitude)
        self.addWidget(self.__longitude)
        self.addWidget(self.__altitude)
        self.addWidget(self.__timezone)
        


    def setInfoByAeroport(self, airport :str):
        bdd = Bdd()
        list = bdd.getInfoByAirport(airport)
        
        labels = [self.__name, self.__city, self.__country, self.__IATACode, self.__ICAOCode, self.__latitude, self.__longitude, self.__altitude, self.__timezone]

        
        
        for i in range(len(labels)):
            labels[i].setText(labels[i].text() + list[i])
                
        bdd.closeConnection()
