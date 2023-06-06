from PyQt6.QtWidgets import QWidget
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout
from CountryListWidget import CountryListWidget
from AirportListWidget import AirportListWidget
from AirportInfoWidget import AirportInfoWidget
from ViewDataMapWidget import ViewDataMapWidget
from ViewDataBarWidget import ViewDataBarWidget
import sys

class win(QWidget): 
    """Créer la fenêtre principale

    """
    
    def __init__(self): 
        super().__init__()

        self.country : str = ""

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
        self.__airportList.airportClicked.connect(self.setSelectedAirport)
        self.__airportList.airportSearched.connect(self.setAirportBySearch)

        # Crée le widget affichant les informations sur un aeroport
        self.__airportInfo : AirportInfoWidget = AirportInfoWidget()
        self.__airportInfo.setFixedSize(200, 500)
        self.__mainLayout.addWidget(self.__airportInfo)

        #Crée le layout affichant les data visualisation
        # self.__viewData : ViewDataMapWidget = ViewDataMapWidget()
        # self.__viewData.setFixedSize(500, 500)
        # self.__mainLayout.addWidget(self.__viewData)
        
        #Crée le layout affichant les data visualisation du nombre de passenger
        # Layout comportant les radio box avec la view
        self.__viewLayout : QVBoxLayout = QVBoxLayout()
        
        self.__viewDataPassenger : ViewDataBarWidget = ViewDataBarWidget()
        self.__viewDataPassenger.qRadioBtnSignal.connect(self.refreshViewDataPassengerByCountry)
        
        self.__viewLayout.addWidget(self.__viewDataPassenger)

        self.__mainLayout.addLayout(self.__viewLayout, 1)

        
        # Affiche le layout principal
        self.setLayout(self.__mainLayout)
        self.show()

    def setSelectedCountry(self, country : str):
        """Défini le pays pour la liste des aeroports et pour la viewdata

        Args:
            country (str): _description_
        """
        self.country = country
        self.__airportList.setAirportByCountry(country)

        # Supprimer le widget précédent s'il existe
        # if self.__viewData is not None:
        #     self.__mainLayout.removeWidget(self.__viewData)
        #     self.__viewData.deleteLater()
        if self.__viewDataPassenger is not None:
            self.__mainLayout.removeWidget(self.__viewDataPassenger)
            self.__viewDataPassenger.deleteLater()
        # # Créer un nouveau widget
        # self.__viewData = ViewDataMapWidget()
        # self.__viewData.setFixedSize(500, 500)
        # self.__mainLayout.addWidget(self.__viewData)

        # Afficher les données dans le nouveau widget

        #Vue de la map monde des aeroport par pays
        # self.__viewData.view_data_country(country)

        self.__viewDataPassenger : ViewDataBarWidget = ViewDataBarWidget()
        self.__viewDataPassenger.qRadioBtnSignal.connect(self.refreshViewDataPassengerByCountry)
        
        #self.__viewDataPassenger.setFixedSize(500,500)
        self.__mainLayout.addWidget(self.__viewDataPassenger)

        #vue pour les 10 aeroport qui transporte le plus de personne
        #self.__viewDataPassenger.view_data_bar_nb_passenger_transport(country)

        #vue pour les 5 aeroport les plus frequenter par pays
        self.__viewDataPassenger.refresh(country)
        #self.__viewDataPassenger.view_data_bar_airport_frequency(country)
        
    def setSelectedAirport(self, airport :str):
        """Défini l'aeroport selectionne pour la viewdata et pour les informations de l'aeroport

        Args:
            airport (str): aeroport
        """
        self.__airportInfo.setInfoByAirport(airport)

        # Supprimer le widget précédent s'il existe
        if self.__viewData is not None:
            self.__mainLayout.removeWidget(self.__viewData)
            self.__viewData.deleteLater()

        # Créer un nouveau widget
        self.__viewData = ViewDataMapWidget()
        self.__viewData.setFixedSize(500, 500)
        self.__mainLayout.addWidget(self.__viewData)

        # Afficher les données dans le nouveau widget
        self.__viewData.view_data_airport(airport)

    def setAirportBySearch(self):
        """Défini la liste des pays lors du changement de l'entrée utilisateur
        """
        self.__airportList.setAirportByCountry(self.country)

    def refreshViewDataPassengerByCountry(self):
        """Rafraichi les données de la view data passenger
        """
        self.__viewDataPassenger.refresh(self.country)

if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())