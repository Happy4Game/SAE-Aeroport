from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QWidget

import sys

class Bdd(QWidget):
    """Classe Bdd

    Args:
        QWidget : Hérite de la classe QWidget
    """

    def __init__(self):
        super().__init__()

        if QSqlDatabase.contains():
            default_connection = QSqlDatabase.database()
            default_connection.close()
            QSqlDatabase.removeDatabase(default_connection.connectionName())

        # QSqlDatabase
        self.db : QSqlDatabase = QSqlDatabase.addDatabase("QPSQL")
        self.db.setHostName("localhost")
        self.db.setPort(5432)
        self.db.setDatabaseName("planes_test")
        self.db.setUserName("happy")
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


    
    def getCountry(self, text : str = "") -> list:
        """Retourne la liste des pays

        Args:
            text (str): Nom d'un pays 'pour de la recherche' 

        Returns:
            list: Une liste de noms de pays
        """
        query = QSqlQuery(self.db)
        query.exec("SELECT name_country FROM country WHERE name_country ILIKE '" + text + "%' ORDER BY name_country ASC;")
     
        
        country_list = []
        while query.next():
            country_list.append(query.value(0))
        
        print(country_list)
        return country_list
    
    def getInfoByAirport(self, airport: str) -> list:
        """Retourne la liste des infos d'un aeroport

        Args:
            airport (str): nom de l'aeroport

        Returns:
            list: Une liste d'informations sur un aeroport
        """
        query = QSqlQuery(self.db)
        info = []
        if query.exec('SELECT * FROM "airport";'):
            while query.next():
                name = query.value(1)
                city = query.value(2)
                country = query.value(3)
                iata_code = query.value(4)
                icao_code = query.value(5)
                latitude = query.value(6)
                longitude = query.value(7)
                altitude = query.value(8)
                timezone = query.value(9)

                if airport == name:
                    info.append(name)
                    info.append(city)
                    info.append(country)
                    info.append(iata_code)
                    info.append(icao_code)
                    info.append(latitude)
                    info.append(longitude)
                    info.append(altitude)
                    info.append(timezone)

        else:
            print("Erreur lors de l'exécution de la requête.")

        return info


    def getPositionAeroportOfCountry(self, country: str):
        query = QSqlQuery(self.db)
        query.prepare("SELECT name_ap, latitude_ap, longitude_ap FROM airport WHERE country_ap = :country")
        query.bindValue(":country", country)

        if query.exec():
            data = []
            while query.next():
                name = query.value(0)
                latitude = query.value(1)
                longitude = query.value(2)
                data.append((name, latitude, longitude))

            return data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return query, []
        
    def getPositionAeroport(self, airport: str):
        query = QSqlQuery(self.db)
        query.prepare("SELECT name_ap, latitude_ap, longitude_ap FROM airport WHERE name_ap = :airport")
        query.bindValue(":airport", airport)
    
        if query.exec():
            data = []
            while query.next():
                name = query.value(0)
                latitude = query.value(1)
                longitude = query.value(2)
                data.append((name, latitude, longitude))

            return data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return query, []
        
    def getAirFrancePlaneSeats(self):
        query = QSqlQuery(self.db)
        query.exec('select distinct p.name_plane, ps.seat_nb from plane p inner join planeseats ps on p.icao_plane = ps.icao_plane inner join routes r on p.icao_plane = r.icao_code inner join airlinecompany ac on r.id_ac = ac.id_ac where ac.name_ac ilike "Air France";')
        seat_list = []
        while query.next():
            plane_name = query.value(0)
            seat_number = query.value(1)
            seat_list.append((plane_name, seat_number))
        return seat_list

        

    def getAirportByCountry(self, country : str, airport : str = "") -> list:
        """Retourne les aeroports

        Args:
            country (str): Nom d'un pays
            airport (str) : Nom d'un aeroport 'pour la fonction de recherche'

        Returns:
            list: Une liste d'aeroport
        """
        query = QSqlQuery(self.db)
        query.prepare("SELECT name_ap FROM airport WHERE country_ap = :country AND name_ap ILIKE '" + airport + "%' ORDER BY name_ap ASC;")
        query.bindValue(":country", country)

        if query.exec():
            data = []
            while query.next():
                data.append(query.value(0))

            return data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return query, []
        
    def closeConnection(self):
        self.db.close()
        print("Connection closed")



if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = Bdd() 
    sys.exit(app.exec())