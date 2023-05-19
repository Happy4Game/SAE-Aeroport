from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtSql, QtCore
from PyQt6.QtCore import QCoreApplication
import sys

class Bdd(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI Avions")

        # QSqlDatabase
        self.db : QSqlDatabase = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setPort(5432)
        self.db.setDatabaseName("planes_test")
        self.db.setUserName("postgres")
        self.db.setPassword("toor")
        ok : bool = self.db.open()
        if ok:
            print("Successfull connection to database")
            self.getPlanes()
            self.getCountry()
            
        else:
            self.db.lastError().text()
    
    def getPlanes(self) -> list:
        query : QSqlQuery = self.db.exec('SELECT * FROM "Planes";')
        list = []
        while query.next():
            list.append(query.value(0))
        return list

    def getCountry(self) -> list:
        query : QSqlQuery = self.db.exec('SELECT "Name" FROM "Countries" ORDER BY "Name" ASC;')
        list = []
        while query.next():
            list.append(query.value(0))
        return list

    def getAirportByCountry(self, country : str) -> list:
        #TODO
        pass
        
    def closeConnection(self):
        self.db.close()
        print("Connection closed")



if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = Bdd() 
    sys.exit(app.exec())