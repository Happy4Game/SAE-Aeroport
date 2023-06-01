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
        self.countryClickedText = ""
        self.addWidget(self.__label)
        self.addWidget(self.__list)

        # Redirection du signal vers la fonction countryClickedFunc
        self.__list.itemClicked.connect(self.countryClickedFunc)
        self.addCountryList()
        self.addWidget(self.__label)
        self.addWidget(self.__list)


    def countryClickedFunc(self, item : QListWidgetItem):
        """Fonction qui emmet le texte du pays dans un signal

        Args:
            item (QListWidgetItem): Element de QListWidget
        """
        self.countryClickedText = item.text()
        self.countryClicked.emit(item.text())

    def getCountryClickedText(self):
        """Fonction qui retourne le texte émis par le signal countryClicked.

        Returns:
            str: Texte émis par le signal countryClicked.
        """
        
        return self.countryClickedText
    
    def addCountryList(self):
        if self.__list.count() == 0:
            bdd = Bdd()
            info = bdd.getCountry()

            print(info)
            for country in range(len(info)):
                self.__list.addItem(info[country])
                
            bdd.closeConnection()