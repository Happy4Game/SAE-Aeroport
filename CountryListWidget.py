from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit
from PyQt6.QtCore import pyqtSignal
from BddControler import BddControler

class CountryListWidget(QWidget):

    countryClicked : pyqtSignal = pyqtSignal(str)

    def __init__(self, bdd : BddControler):
        super().__init__()

        self.bdd : BddControler = bdd

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Label indiquant la liste des pays
        self.__label = QLabel("Liste des pays")

        # Ligne de saisie de texte
        self.__line_edit : QLineEdit = QLineEdit()
        self.__line_edit.setPlaceholderText("Rechercher un pays")
        self.__line_edit.textChanged.connect(self.addCountryList)

        self.__list = QListWidget()
        self.countryClickedText = ""
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__list)

        # Redirection du signal vers la fonction countryClickedFunc
        self.__list.itemClicked.connect(self.countryClickedFunc)
        self.addCountryList()
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__line_edit)
        self.__layout.addWidget(self.__list)


    def countryClickedFunc(self, item : QListWidgetItem) -> None:
        """Fonction qui emmet le texte du pays dans un signal

        Args:
            item (QListWidgetItem): Element de QListWidget
        """
        self.countryClickedText = item.text()
        self.countryClicked.emit(item.text())

    def getCountryClickedText(self) -> str:
        """Fonction qui retourne le texte émis par le signal countryClicked.

        Returns:
            str: Texte émis par le signal countryClicked.
        """
        
        return self.countryClickedText
    
    def addCountryList(self) -> None:
        """Fonction qui ajoute la liste des pays dans QListWidget
        """
        self.__list.clear()
        text = self.__line_edit.text()
        if self.__list.count() == 0:
            info = self.bdd.getCountry(text)
            
            for country in range(len(info)):
                self.__list.addItem(info[country])