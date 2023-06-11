from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QComboBox
from PyQt6.QtCore import Qt
from BddControler import BddControler
from AirPlainCompanyInfoWidget import AirPlainCompanyInfoWidget
from CompanyListWidget import CompanyListWidget
from PyQt6.QtGui import QPixmap
import numpy as np
import matplotlib.pyplot as plt

class AirPlainCompanyWidget(QWidget):

    def __init__(self, bdd : BddControler):
        super().__init__()

        self.__bdd : BddControler = bdd

        self.__layout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__companyLayout : QVBoxLayout = QVBoxLayout()
        self.__companyLayout.addWidget(QLabel("Souhaitez vous voir les aéroports:"))


        # Layout accueillant les boutons Actif/Inactif
        self.__companyActiveLayout : QHBoxLayout = QHBoxLayout()
        self.__companyActiveLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Widget comportant les boutons Monde/Europe
        self.__regionSelectedWidget : QComboBox = QComboBox()
        self.__regionSelectedWidget.addItem("Monde")
        self.__regionSelectedWidget.addItem("Europe")
        self.__regionSelectedWidget.setCurrentIndex(0)
        self.__regionSelectedWidget.currentIndexChanged.connect(self.setCompanyList)

        #Boutons Actif/Inactif
        self.__companyActiveButton : QRadioButton = QRadioButton("Actif")
        self.__companyActiveButton.setChecked(True)
        self.__companyActiveButton.clicked.connect(self.setCompanyList)
        self.__commpanyInactiveButton : QRadioButton = QRadioButton("Inactif")
        self.__commpanyInactiveButton.clicked.connect(self.setCompanyList)


        self.__companyActiveLayout.addWidget(self.__regionSelectedWidget)
        self.__companyActiveLayout.addWidget(self.__companyActiveButton)
        self.__companyActiveLayout.addWidget(self.__commpanyInactiveButton)


        self.__companyLayout.addLayout(self.__companyActiveLayout)


        self.__companyList : CompanyListWidget = CompanyListWidget(self.__bdd)
        self.__companyList.qSelectedCompany.connect(self.setInfosByCompany)

        self.__companyLayout.addWidget(self.__companyList)
        self.__layout.addLayout(self.__companyLayout)
        

        self.__companyInfosWidget : AirPlainCompanyInfoWidget = AirPlainCompanyInfoWidget(self.__bdd)
        self.__companyInfosWidget.setFixedSize(500, 500)
        self.__layout.addWidget(self.__companyInfosWidget)

        self.__viewLayout : QVBoxLayout = QVBoxLayout()
        self.__viewLayoutH : QHBoxLayout =  QHBoxLayout()
        self.__viewLayoutH.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__co2_image_selected : QComboBox = QComboBox()
        self.__co2_image_selected.setCurrentIndex(0)
        self.__co2_image_selected.currentIndexChanged.connect(self.view_data_co2)
        self.__co2_image_selected.addItem("Les 5 plus petits émetteurs de CO2 en Europe")
        self.__co2_image_selected.addItem("Les 5 principaux émetteurs de CO2 en Europe.")
        self.__co2_image_selected.addItem("Les 5 plus petits émetteurs de co2 dans le monde")
        self.__co2_image_selected.addItem("Les 5 principaux emetteurs de co2 dans le monde")
        self.__viewLayoutH.addWidget(self.__co2_image_selected)
        self.__layout.addLayout(self.__viewLayout)

    def setCompanyList(self):
        isWorld : bool = True

        if self.__regionSelectedWidget.currentText() == "Europe":
            isWorld = False

        if self.__companyActiveButton.isChecked():
            print("Y" + str(isWorld))
            self.__companyList.setCompanyList("Y", isWorld)
        else:
            print("N" + str(isWorld))
            self.__companyList.setCompanyList("N", isWorld)

        

    def setInfosByCompany(self, company : str):
        self.__companyInfosWidget.setInfosByCompany(company)

    def view_data_co2(self):
        """Fonction de création du graphique pour le co2 
        """
        # Supprimer le widget existant s'il en existe un
        for i in reversed(range(self.__viewLayout.count())):
            widget = self.__viewLayout.itemAt(i).widget()
            if widget is not None:
                self.__viewLayout.removeWidget(widget)
                widget.deleteLater()

        data_co2 = []
        choix = 0

        if self.__co2_image_selected.currentText() == "Les 5 plus petits émetteurs de CO2 en Europe":
            data_co2 = self.__bdd.getco2ByAirlineCompany_europe_asc()
            choix = 1

        elif self.__co2_image_selected.currentText() == "Les 5 principaux émetteurs de CO2 en Europe.":
            data_co2 = self.__bdd.getco2ByAirlineCompany_europe_desc()
            choix = 2
        elif self.__co2_image_selected.currentText() == "Les 5 plus petits émetteurs de co2 dans le monde":
            data_co2 = self.__bdd.getco2ByAirlineCompany_monde_asc()
            choix = 3

        else:
            data_co2 = self.__bdd.getco2ByAirlineCompany_monde_desc()

        # Extraire les données de la liste
        names = [data[0] for data in data_co2]
        co2_values = [data[1] for data in data_co2]

        # Créer les positions des barres
        abscisse_pos = np.arange(len(names))

        # Paramétrage du graphique
        plt.bar(abscisse_pos, co2_values, align='edge', alpha=0.5, edgecolor='black')
        plt.xticks(abscisse_pos, names, rotation=45, ha='right', fontsize=12)
        plt.ylabel('Emission CO2')

        # Définir la plage de l'axe des ordonnées pour commencer à zéro
        plt.ylim(0, max(co2_values) * 1.1)
        

        # Définir le titre en fonction du choix
        if choix == 1:
            plt.title("Les 5 plus petits émetteurs de CO2 en Europe")
        elif choix == 2:
            plt.title("Les 5 principaux émetteurs de CO2 en Europe.")
        elif choix == 3:
            plt.title("Les 5 plus petits émetteurs de CO2 dans le monde")
        else:
            plt.title("Les 5 principaux émetteurs de CO2 dans le monde")

        # Ajuster le graphique au layout
        plt.tight_layout()

        # Nommage et sauvegarde de l'image
        temp_file = 'co2_impact_by_airline_company.png'
        plt.savefig(temp_file, format='png', dpi=75)
        plt.close()

        image_label = QLabel()
        image_label.setPixmap(QPixmap(temp_file))

        self.__viewLayoutH = QHBoxLayout()
        self.__viewLayoutH.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__viewLayoutH.addWidget(self.__co2_image_selected)

        self.__viewLayout.addLayout(self.__viewLayoutH)
        self.__viewLayout.addWidget(image_label, Qt.AlignmentFlag.AlignCenter)



        