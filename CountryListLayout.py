from PyQt6.QtWidgets import QLabel, QVBoxLayout, QListWidget, QListWidgetItem
from PyQt6.QtCore import pyqtSignal
from Bdd import Bdd

class CountryListLayout(QVBoxLayout):

    countryClicked : pyqtSignal = pyqtSignal(str)

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

        # A retirer (TODO)
        self.__list.addItem("Test")

        self.__bdd.closeConnection()

        # Redirection du signal vers la fonction countryClickedFunc
        self.__list.itemClicked.connect(self.countryClickedFunc)

        self.addWidget(self.__label)
        self.addWidget(self.__list)


    def countryClickedFunc(self, item : QListWidgetItem):
        """Fonction qui emmet le texte du pays dans un signal

        Args:
            item (QListWidgetItem): Element de QListWidget
        """
        self.countryClicked.emit(item.text())