from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout
from CountryListLayout import CountryListLayout
from AirportListLayout import AirportListLayout
from AirportInfoWidget import AirportInfoLayout
from ViewDataLayout import ViewDataLayout # demandé pourquoi il n'importe pas juste le fichier

import sys

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

        # Crée le layout affichant les informations sur un aeroport
        self.__airportInfo = AirportInfoLayout()
        self.__mainLayout.addLayout(self.__airportInfo)

        #Crée le layout affichant les data visualisation
        self.__viewData = ViewDataLayout()
        self.__mainLayout.addLayout(self.__viewData)
        self.__viewData.load_data

        self.__airportList.airportClicked.connect(self.setSelectedAiroprt)

        self.setLayout(self.__mainLayout)
        self.show()

    def setSelectedCountry(self, country : str):
        """Définit le pays récupéré dans la vue CountryListLayout pour la vue AirportListLayout

        Args:
            country (str): _description_
        """
        # TODO Envoyer vers AirportListLayout
        print(country)

    def setSelectedAiroprt(self, airport :str):
        print(airport)
        self.__airportInfo.setInfoByAeroport(airport)

if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())