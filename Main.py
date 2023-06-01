from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QVBoxLayout, QWidget
from CountryListWidget import CountryListWidget
from AirportListWidget import AirportListWidget
from AirportInfoWidget import AirportInfoWidget
from ViewDataMapWidget import ViewDataMapWidget


import sys
#TODO: a chaque clique effacer derriere pour ne pas générer une double liste
# Faire en sorte de récupérer le pays pour que la map monde s'affiche en fonction
class win(QWidget): 
    """Créer la fenêtre principale

    """
    def __init__(self): 
        super().__init__()
        self.setMinimumSize(1250, 500)

        # TODO Changer le nom du logiciel
        self.setWindowTitle("UI Avions")

        # Layout comprenant l'ensemble des widgets/layouts
        self.__mainLayout = QHBoxLayout()

        # Crée le widget affichant les pays
        self.__countryList : CountryListWidget = CountryListWidget()
        # Récupère le signal et le redirige vers la fonction setSelectedCountry
        self.__countryList.countryClicked.connect(self.setSelectedCountry)
        self.__mainLayout.addWidget(self.__countryList)

        # Crée le widget affichant les aeroports
        self.__airportList : AirportListWidget = AirportListWidget()
        self.__mainLayout.addWidget(self.__airportList)
        self.__airportList.airportClicked.connect(self.setSelectedAiroprt)

        # Crée le widget affichant les informations sur un aeroport
        self.__airportInfo = AirportInfoWidget()
        self.__airportInfo.setFixedSize(200, 500)
        self.__mainLayout.addWidget(self.__airportInfo)

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

    def setSelectedAiroprt(self, airport :str):
        print(airport)
        self.__airportInfo.setInfoByAeroport(airport)

if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())