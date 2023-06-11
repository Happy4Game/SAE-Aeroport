from PyQt6.QtWidgets import QListWidget
from PyQt6.QtCore import pyqtSignal
from BddControler import BddControler

class CompanyListWidget(QListWidget):

    qSelectedCompany : pyqtSignal = pyqtSignal(str)

    def __init__(self, bdd : BddControler):
        super().__init__()
        self.__bdd : BddControler = bdd

        self.setCompanyList()

        self.itemClicked.connect(self.qSelectedCompanyFunc)

    def setCompanyList(self, active : str = "%"):
        """Défini la liste des compagnies aériennes dans le widget
        """
        self.clear()
        companys = self.__bdd.getCompanyList(active)
        for company in companys:
            self.addItem(company)

    def qSelectedCompanyFunc(self):
        self.qSelectedCompany.emit(self.currentItem().text())
