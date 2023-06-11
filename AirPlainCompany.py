from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QCheckBox, QRadioButton
from PyQt6.QtCore import Qt
from BddControler import BddControler
from CompanyListWidget import CompanyListWidget

class AirPlainCompany(QWidget):

    def __init__(self, bdd : BddControler):
        super().__init__()

        self.__bdd : BddControler = bdd

        self.__layout : QHBoxLayout = QHBoxLayout()
        self.setLayout(self.__layout)

        self.__companyLayout : QVBoxLayout = QVBoxLayout()
        self.__companyLayout.addWidget(QLabel("Souhaitez vous voir les aéroports:"))


        # TODO Ajouter le checkbox
        self.__companyCheckBoxLayout : QHBoxLayout = QHBoxLayout()
        self.__companyCheckBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.__companyActiveButton : QRadioButton = QRadioButton("Actif")
        self.__companyActiveButton.clicked.connect(self.setCompanyList)
        self.__commpanyInactiveButton : QRadioButton = QRadioButton("Inactif")
        self.__commpanyInactiveButton.clicked.connect(self.setCompanyList)
        self.__companyCheckBoxLayout.addWidget(self.__companyActiveButton)
        self.__companyCheckBoxLayout.addWidget(self.__commpanyInactiveButton)

        self.__companyLayout.addLayout(self.__companyCheckBoxLayout)


        self.__companyList : CompanyListWidget = CompanyListWidget(self.__bdd)

        self.__companyLayout.addWidget(self.__companyList)
        self.__layout.addLayout(self.__companyLayout)

    def setCompanyList(self):
        if self.__companyActiveButton.isChecked():
            self.__commpanyInactiveButton.setChecked(False)
            self.__companyList.setCompanyList("Y")
        else:
            self.__companyActiveButton.setChecked(False)
            self.__companyList.setCompanyList("N")