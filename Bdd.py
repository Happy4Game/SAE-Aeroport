from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6 import QtSql, QtCore
from PyQt6.QtCore import QCoreApplication
import sys

class Bdd(QWidget):
    """Classe Bdd

    Args:
        QWidget : Hérite de la classe QWidget
    """

    def __init__(self):
        super().__init__()

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
            
        else:
            self.db.lastError().text()
    
    def getPlanes(self) -> list:
        """Récupère la liste des avions

        Returns:
            list: Une liste d'avions (TODO)
        """
        query : QSqlQuery = self.db.exec('SELECT * FROM "Planes";')
        list = []
        while query.next():
            list.append(query.value(0))
        return list

    def get_name_country(self) -> tuple:
        """Récupère la liste des avions

    Returns:
        (QSqlQuery, list): La requête exécutée et une liste d'avions
    """
        query = QSqlQuery(self.db)
        query.prepare('SELECT "Name" FROM "Countries" ORDER BY "Name" ASC;')

        if query.exec():
            plane_list = []
            while query.next():
                plane_list.append(query.value(0))
            return query, plane_list
        else:
            print("Erreur lors de l'exécution de la requête.")
            return query, []

    
    def getCountry(self) -> list:
        """Retourne la liste des pays

        Returns:
            list: Une liste de nom de pays
        """
        query : QSqlQuery = self.db.exec('SELECT "Name" FROM "Countries" ORDER BY "Name" ASC;')
        list = []
        while query.next():
            list.append(query.value(0))
        return list
    
    def getInfoByAirport(self, airport : str) -> list:
        if airport == "Charles de Gaulle":
            return["AER", "ETU", "knfv", "hurhu", "gt", "gtijid", "ieviuv", "huevu", "ufgihe"]
        else:
            return [""]
        

    def getAirportByCountry(self, country : str) -> list:
        """Retourne les aeroports

        Args:
            country (str): Nom d'un pays

        Returns:
            list: Une liste d'aeroport
        """
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