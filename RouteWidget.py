from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from AirportListWidget import AirportListWidget
from ViewDataRouteWidget import ViewDataRouteWidget
from BddControler import BddControler
from CountryListWidget import CountryListWidget

class RouteWidget(QWidget):

    def __init__(self, bdd : BddControler):
        super().__init__()

        self.bdd = bdd

        self.__airportSrc : str = ""
        self.__airportDest : str = ""

        self.__mainLayout : QHBoxLayout = QHBoxLayout()

        # Crée le widget affichant les pays src
        self.__countrySrcList : CountryListWidget = CountryListWidget(bdd)
        self.__countrySrcList.countryClicked.connect(self.setSelectedSrcCountry)
        self.__mainLayout.addWidget(self.__countrySrcList)

        # Crée le widget affichant les aeroports src
        self.__airportSrcList : AirportListWidget = AirportListWidget(bdd, "Aeroport de depart", "Rechercher un aeroport de depart", False)
        self.__airportSrcList.airportClicked.connect(self.setSrcAirport)
        self.__airportSrcList.airportSearched.connect(self.setSrcAirportList)
        self.__mainLayout.addWidget(self.__airportSrcList)

        # Crée le widget affichant les pays dest
        self.__countryDestList : CountryListWidget = CountryListWidget(bdd)
        self.__countryDestList.countryClicked.connect(self.setSelectedDestCountry)
        self.__mainLayout.addWidget(self.__countryDestList)

        # Crée le widget affichant les aeroports dest
        self.__airportDestList : AirportListWidget = AirportListWidget(bdd, "Aeroport de destination", "Rechercher un aeroport de destination", False)
        self.__airportDestList.airportClicked.connect(self.setDestAirport)
        self.__airportDestList.airportSearched.connect(self.setDestAirportList)
        self.__mainLayout.addWidget(self.__airportDestList)

        self.__viewDataRouteWidget : ViewDataRouteWidget = ViewDataRouteWidget(bdd, "", "")
        self.__rightLayout : QVBoxLayout = QVBoxLayout()
    
        self.__rightLayout.addWidget(self.__viewDataRouteWidget)
        
        self.__distance : QLabel = QLabel("Distance (km) :")
        self.__co2 : QLabel = QLabel("Emission co2 :")
        self.__rightLayout.addWidget(self.__distance)
        self.__rightLayout.addWidget(self.__co2)

        self.__mainLayout.addLayout(self.__rightLayout)

        self.infoRoute = [self.__distance, self.__co2]
        self.initialTexts = [label.text() for label in self.infoRoute]

        self.setLayout(self.__mainLayout)
        
    def setSelectedSrcCountry(self, country : str) -> None:
        """Défini le pays pour la liste des aeroports et pour la viewdata

        Args:
            country (str): Nom du pays
        """
        self.srcCountry = country
        self.__airportSrcList.setAirportByCountry(country)

    def setSelectedDestCountry(self, country : str) -> None:
        """Défini le pays pour la liste des aeroports et pour la viewdata

        Args:
            country (str): Nom du pays
        """
        self.destCountry = country
        self.__airportDestList.setAirportByCountry(country)


    def setSrcAirport(self, airport : str) -> None:
        """Défini l'aeroport de depart pour la viewdata

        Args:
            airport (str): un nom d'aeroport
        """
        self.__airportSrc = airport
        if self.__airportSrc != "" and self.__airportDest != "":
            self.__viewDataRouteWidget.clear()
            self.__viewDataRouteWidget.view_data_route(self.__airportSrc, self.__airportDest)
            info = self.bdd.getInfoRouteByAirport(self.__airportSrc, self.__airportDest)
            print(info)
            for label, initialText in zip(self.infoRoute, self.initialTexts):
                label.setText(initialText)  # Réinitialisation du texte avant mise à jour

            for label, value in zip(self.infoRoute, info):
                label.setText(label.text() + str(value))
    
    def setDestAirport(self, airport : str) -> None:
        """Défini l'aeroport de destination pour la viewdata

        Args:
            airport (str): un nom d'aeroport
        """
        self.__airportDest = airport
        if self.__airportSrc != "" and self.__airportDest != "":
            self.__viewDataRouteWidget.clear()
            self.__viewDataRouteWidget.view_data_route(self.__airportSrc, self.__airportDest)
            self.bdd.getInfoRouteByAirport(self.__airportSrc, self.__airportDest)
            info = self.bdd.getInfoRouteByAirport(self.__airportSrc, self.__airportDest)
            
            for label, initialText in zip(self.infoRoute, self.initialTexts):
                label.setText(initialText)  # Réinitialisation du texte avant mise à jour

            for label, value in zip(self.infoRoute, info):
                label.setText(label.text() + str(value))

    def setSrcAirportList(self) -> None:
        self.__airportSrcList.setAirportByCountry(self.srcCountry)

    def setDestAirportList(self) -> None:
        self.__airportDestList.setAirportByCountry(self.destCountry)