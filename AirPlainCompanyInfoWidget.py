from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from BddControler import BddControler

class AirPlainCompanyInfoWidget(QWidget):
    """Création du widget contenant le sinformations des aéroports

    """
    def __init__(self, bdd : BddControler):
        super().__init__()

        self.bdd = bdd

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)
        
        # Labels indiquant les informations de la compagnie aérienne
        self.__label : QLabel = QLabel("Informations de la compagnie aérienne :")
        self.__name : QLabel = QLabel("Nom : ")
        self.__country : QLabel = QLabel("Pays : ")
        self.__IATACode : QLabel = QLabel("Code IATA : ")
        self.__radioCode : QLabel = QLabel("Indicatif Radio : ")
        self.__activity : QLabel = QLabel("En activité (Y pour Oui et N pour non) : ")
        
        # Ajout des widgets dans le layout
        self.__layout.addWidget(self.__label)
        self.__layout.addWidget(self.__name)
        self.__layout.addWidget(self.__country)
        self.__layout.addWidget(self.__IATACode)
        self.__layout.addWidget(self.__radioCode)
        self.__layout.addWidget(self.__activity)
        
        # Initialisation des valeurs des labels
        self.labels = [self.__name, self.__country, self.__IATACode, self.__radioCode, self.__activity]
        self.initialTexts = [label.text() for label in self.labels]

    def setInfosByCompany(self, company: str) -> None:
        info = self.bdd.getInfoByCompany(company)
        
        for label, initialText in zip(self.labels, self.initialTexts):
            label.setText(initialText)  # Réinitialisation du texte avant mise à jour

        for label, value in zip(self.labels, info):
            label.setText(label.text() + str(value))
