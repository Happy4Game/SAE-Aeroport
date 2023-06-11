from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QRadioButton, QComboBox
from PyQt6.QtCore import Qt
from BddControler import BddControler
from AirPlainCompanyInfoWidget import AirPlainCompanyInfoWidget
from CompanyListWidget import CompanyListWidget

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