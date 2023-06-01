from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget
from CountryListLayout import CountryListLayout
from AirportListLayout import AirportListLayout
from AirportInfoWidget import AirportInfoLayout
from ViewDataMapWidget import ViewDataMapWidget

import sys
#TODO: a chaque clique effacer derriere pour ne pas générer une double liste
# Faire en sorte de récupérer le pays pour que la map monde s'affiche en fonction
class win(QWidget): 
    """Créer la fenêtre principale

    """
    def __init__(self): 
        super().__init__()

        # TODO Changer le nom du logiciel
        self.setWindowTitle("UI Avions")

        # Layout comprenant l'ensemble des widgets/layouts
        self.__mainLayout = QHBoxLayout()

        # Crée le layout affichant les pays
        self.__countryList : CountryListLayout = CountryListLayout()
        # Récupère le signal et le redirige vers la fonction setSelectedCountry
        self.__countryList.countryClicked.connect(self.setSelectedCountry)

        self.__mainLayout.addLayout(self.__countryList)

        # Crée le layout affichant les aeroports
        self.__airportList = AirportListLayout()
        self.__mainLayout.addLayout(self.__airportList)
        self.__airportList.airportClicked.connect(self.setSelectedAiroprt)

        # Crée le layout affichant les informations sur un aeroport
        self.__airportInfo = AirportInfoLayout()
        self.__mainLayout.addLayout(self.__airportInfo)

        #Crée le layout affichant les data visualisation
        self.__viewData = ViewDataMapWidget()
        self.__viewData.setFixedSize(500, 500)
        self.__mainLayout.addWidget(self.__viewData)

        

        self.setLayout(self.__mainLayout)
        self.show()

    def setSelectedCountry(self, country : str):
        
        self.__airportList.setAeroportByCountry(country)
        return country

    def setSelectedAiroprt(self, airport :str):
        print(airport)
        self.__airportInfo.setInfoByAeroport(airport)

if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())