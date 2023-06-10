from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PyQt6.QtWidgets import QApplication, QWidget

import sys

class BddControler(QWidget):
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
        self.db.setDatabaseName("plane_test")
        self.db.setUserName("johan")
        self.db.setPassword("Johannahoj972.")
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
        query.exec("SELECT DISTINCT(country_ap) FROM airport WHERE country_ap ILIKE '" + text + "%' ORDER BY country_ap ASC;")
     
        
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


    def getPositionAeroportOfCountry(self, country: str) -> list:
        """Retourne la position des aeroports d'un pays

        Args:
            country (str): nom d'un pays

        Returns:
            list: Une liste de position d'aeroport
        """
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
        
    def getPositionAeroport(self, airport: str) -> list:
        """Retourne une liste de position d'un aeroport

        Args:
            airport (str): nom d'un aeroport

        Returns:
            list: Une liste de position d'un aeroport
        """
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
        
    def getAirFrancePlaneSeats(self) -> list:
        """Retourne la liste avec le nom des avions et le nombre de sieges

        Returns:
            list: Une liste avec le nom des avions et le nombre de sieges
        """
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
        
    def getAirports(self, airport : str = "") -> list:
        """Retourne les aeroports

        Args:
            airport (str) : Nom d'un aeroport 'pour la fonction de recherche'

        Returns:
            list: Une liste d'aeroport
        """
        query = QSqlQuery(self.db)
        query.prepare("SELECT name_ap FROM airport WHERE name_ap ILIKE '" + airport + "%' ORDER BY name_ap ASC;")

        if query.exec():
            data = []
            while query.next():
                if ("[Duplicate]" not in query.value(0) and "(Duplicate)" not in query.value(0)):
                    data.append(query.value(0))

            return data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return query, []
        
    def getNbPassengerByAirport(self, country: str) -> list:
        """Retourne le nombre de passager par aeroport

        Args:
            country (str): Nom d'un pays

        Returns:
            list: Une liste de nombre de passager par aeroport
        """
        # Quels sont les 10 aéroports dans un pays spécifique (défini par la variable ":country") 
        # qui ont transporté le plus grand nombre de passagers, triés par ordre croissant du nombre de passagers ?
        query = QSqlQuery(self.db)
        query.prepare("SELECT nb_passenger, name_ap, name_country FROM (SELECT SUM(seat_nb) AS nb_passenger, name_ap, name_country FROM planeseats AS ps INNER JOIN plane AS p ON p.icao_plane = ps.id_plane INNER JOIN routeavion AS ra ON ra.iata_code = p.iata_plane INNER JOIN routes AS r ON r.id_ra = ra.id_ra INNER JOIN airport ON source_ap = id_ap INNER JOIN country ON country.name_country = airport.country_ap WHERE name_country ILIKE :country GROUP BY name_ap, name_country ORDER BY nb_passenger DESC LIMIT 10 ) AS subquery ORDER BY nb_passenger ASC;")
        query.bindValue(":country", country)

        if query.exec():
            nb_passenger_data = [], []
            while query.next():
                nb_passenger = query.value("nb_passenger")
                airport_name = query.value("name_ap")
                nb_passenger_data[0].append(nb_passenger)
                nb_passenger_data[1].append(airport_name)
            return nb_passenger_data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return [], []

    def getMostUseAirport(self, country: str) -> list:
        """Retourne les aeroports les plus fréquentés dans un pays

        Args:
            country (str): Nom d'un pays

        Returns:
            list: Une liste d'aeroport
        """
        #Quels sont les aéroports les plus fréquentés dans un pays ?
        query = QSqlQuery(self.db)
        query.prepare("SELECT name_ap, frequency FROM(SELECT airport.name_ap, COUNT(*) AS frequency FROM routes JOIN airport ON routes.dest_ap = airport.id_ap JOIN country ON airport.country_ap = country.name_country WHERE country.name_country ILIKE :country GROUP BY airport.name_ap ORDER BY frequency DESC limit 5) as subquery ORDER BY frequency ASC;")
        query.bindValue(":country", country)
        if query.exec():
            nb_passenger_data = [], []
            while query.next():
                airport_name = query.value("name_ap")
                number = query.value("frequency")
                nb_passenger_data[0].append(airport_name)
                nb_passenger_data[1].append(number)
            return nb_passenger_data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return [], []
        
    def getTotalCo2ByCountry(self) -> list:
        """Retourne le total de co2 par pays

        Returns:
            list: Une liste de total de co2 par pays
        """
        query = QSqlQuery(self.db)
        query.prepare("select co2, country_ap as pays from tot_co2_pays;")
        if query.exec():
            data = []
            while query.next():
                co2 = query.value("co2")
                pays = query.value("pays")
                data.append((co2,pays))
                
            return data
        else:
            print("Erreur lors de l'exécution de la requête.")
            return []
    
    def getInfoAirportRoute(self, airport: str) -> list:
        """Retourne les informations d'un aeroport

        Args:
            airport (str): Nom d'un aeroport

        Returns:
            list: Une liste d'informations d'un aeroport
        """
        query = QSqlQuery(self.db)
        query.prepare('SELECT name_ap, longitude_ap, latitude_ap FROM "airport" WHERE name_ap = :airport;')
        query.bindValue(":airport", airport)
        
        if query.exec():
            info = []
            while query.next():
                name = query.value(0)
                longitude = query.value(1)
                latitude = query.value(2)
                info.append(name)
                info.append(longitude)
                info.append(latitude)
            return info
        else:
            print("Erreur lors de l'exécution de la requête.")
            return []
    
    def getInfoRouteByAirport(self, src_airport :str, dest_airport: str):
        """Retourne les informations des routes (distance en km et émission de co2)
        """
        query = QSqlQuery(self.db)
        query.prepare("select calculated_co2 as co2, source_airport, destination_airport, distance from co2_par_aeroport_total where source_airport ilike :source and destination_airport ilike :destination")
        query.bindValue(":source", src_airport)
        query.bindValue(":destination", dest_airport)

        if query.exec():
            info = []
            while query.next():
                co2 = query.value("co2")
                distance = query.value("distance")
                info.append(round(co2))
                info.append(round(distance))
            print(info)
            return info
        else:
            print("Erreur lors de l'exécution de la requête.")
            return []

    def getRouteFromAirportToCountry(self, airport : str):
        """Retourne la liste des pays disponible en prenant un aeroport

        Args:
            airport (str): aéroport de départ

        Returns:
            (list): une liste contenant les pays disponibles
        """
        query = QSqlQuery(self.db)
        query.prepare("SELECT DISTINCT(a2.country_ap) as country FROM routes r INNER JOIN airport a ON r.source_ap = a.id_ap INNER JOIN airport a2 on r.dest_ap = a2.id_ap WHERE a.name_ap ILIKE :airport;")
        query.bindValue(":airport", airport)
        
        if query.exec():
            info = []
            while query.next():
                countries = query.value("country")
                info.append(countries)
            print(info)
            return info
        else:
            print("Erreur lors de l'exécution de la requête.")
            return [] 
        
    def getTotalCo2ByEurope(self) -> list:
        """Retourne le total de co2 des pays d'europe

        Returns:
            list: Une liste de total de co2 en europe
        """
        query = QSqlQuery(self.db)
        query.prepare("select co2, country_ap as pays from tot_co2_pays_europe;")
        if query.exec():
            data = []
            while query.next():
                co2 = query.value("co2")
                pays = query.value("pays")
                data.append((co2,pays))
                
            return data
        else:
            print("Erreur lors de l'exécution de la requête.§§")
            return []
    
        
    def closeConnection(self) -> None:
        """Ferme la connection avec la base de données
        """
        self.db.close()
        print("Connection closed")



if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = BddControler() 
    sys.exit(app.exec())