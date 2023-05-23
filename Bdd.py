from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QWidget

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

    def getAirportByCountry(self, country : str) -> list:
        """Retourne les aeroports

        Args:
            country (str): Nom d'un pays

        Returns:
            list: Une liste d'aeroport
        """
        # TODO
        if (country == "Test"):
            return ["Test de Gaulle", "Test de Roissy", "..."]
        else:
            return ["Aucun résultat"]
        
        
    def closeConnection(self):
        self.db.close()
        print("Connection closed")



# if __name__ == "__main__": 
#     print(f'main') 
#     app = QApplication(sys.argv) 
#     f = Bdd() 
#     sys.exit(app.exec())