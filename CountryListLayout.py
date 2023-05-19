from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidget
from PyQt6.QtCore import pyqtSignal
from Bdd import Bdd

class CountryListLayout(QVBoxLayout):

    countryClicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        # Label indiquant la liste des pays
        self.__label = QLabel("Liste des pays")

        self.__list = QListWidget()
        
        # Liste de pays randoms (Européens)

        # BDD
        self.__bdd = Bdd()

        list = self.__bdd.getCountry()
        for country in list:
            self.__list.addItem(country)

        self.__bdd.closeConnection()

        self.__list.itemClicked.connect(self.countryClickedFunc)

        self.addWidget(self.__label)
        self.addWidget(self.__list)


    def countryClickedFunc(self, item):
        self.countryClicked.emit(item.text())