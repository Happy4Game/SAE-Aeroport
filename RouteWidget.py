from PyQt6.QtWidgets import QWidget, QHBoxLayout
from AirportListWidget import AirportListWidget
from ViewDataRouteWidget import ViewDataRouteWidget
from BddControler import BddControler

class RouteWidget(QWidget):

    def __init__(self, bdd : BddControler):
        super().__init__()

        self.bdd = bdd

        self.__airportSrc : str = ""
        self.__airportDest : str = ""

        self.__mainLayout : QHBoxLayout = QHBoxLayout()

        self.__airportSrcList : AirportListWidget = AirportListWidget(bdd, "Aeroport de depart", "Rechercher un aeroport de depart", True)
        self.__airportSrcList.airportClicked.connect(self.setSrcAirport)
        self.__airportSrcList.airportSearched.connect(self.setSrcAirportList)
        self.__mainLayout.addWidget(self.__airportSrcList)

        self.__airportDestList : AirportListWidget = AirportListWidget(bdd, "Aeroport de destination", "Rechercher un aeroport de destination", True)
        self.__airportDestList.airportClicked.connect(self.setDestAirport)
        self.__airportDestList.airportSearched.connect(self.setDestAirportList)
        self.__mainLayout.addWidget(self.__airportDestList)

        self.__viewDataRouteWidget : ViewDataRouteWidget = ViewDataRouteWidget(bdd, "", "")
        self.__mainLayout.addWidget(self.__viewDataRouteWidget)
        

        self.setLayout(self.__mainLayout)
        
    def setSrcAirport(self, airport : str):
        self.__airportSrc = airport
        if self.__airportSrc != "" and self.__airportDest != "":
            self.__viewDataRouteWidget.clear()
            self.__viewDataRouteWidget.view_data_route(self.__airportSrc, self.__airportDest)
    
    def setDestAirport(self, airport : str):
        self.__airportDest = airport
        if self.__airportSrc != "" and self.__airportDest != "":
            self.__viewDataRouteWidget.clear()
            self.__viewDataRouteWidget.view_data_route(self.__airportSrc, self.__airportDest)

    def setSrcAirportList(self):
        self.__airportSrcList.setAirportList()

    def setDestAirportList(self):
        self.__airportDestList.setAirportList()