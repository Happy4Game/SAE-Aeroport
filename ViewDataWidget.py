from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import numpy as np
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


class ViewDataWidget(QWidget):
    """Classe représentant un widget contenant une data visualisation diagramme en barre

    Args:
        QWidget (QWidget): hérite de QWidget
    """

    qRadioBtnSignal : pyqtSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        # Layout comportant les radio box
        self.__viewLayoutH : QHBoxLayout = QHBoxLayout()
        self.__qRadioBbtn1 : QRadioButton = QRadioButton("Affichage des aeroports")
        self.__qRadioBbtn1.setChecked(True)
        self.__qRadioBbtn1.clicked.connect(self.qRadioBbtnSignalFunc)
        self.__qRadioBbtn2 : QRadioButton = QRadioButton("Aeroports les plus fréquentés")
        self.__qRadioBbtn2.clicked.connect(self.qRadioBbtnSignalFunc)

        self.__qRadioBbtn3 : QRadioButton = QRadioButton("Map monde des aeroports")
        self.__qRadioBbtn3.clicked.connect(self.qRadioBbtnSignalFunc)
        
        self.__viewLayoutH.addWidget(self.__qRadioBbtn1)
        self.__viewLayoutH.addWidget(self.__qRadioBbtn2)
        self.__viewLayoutH.addWidget(self.__qRadioBbtn3)

        self.__viewLayoutH.setAlignment(Qt.AlignmentFlag.AlignTop)


    def view_data_bar_nb_passenger_transport(self, country: str):
        """Méthode permettant de créer une data visualisation correspondant au nombre de personne transporté par aeroport

        Args:
            country (str): Le pays dont on veux connaitre le résultat de la requête
        """
        bdd = Bdd()
        #On stock dans une varibale le résultat de la methode
        nb_passenger_data = bdd.getNbPassengerByAirport(country)

        abscisse_pos = np.arange(len(nb_passenger_data[1]) + 1)

        # Coche le bouton radio 1
        self.__qRadioBbtn1.setChecked(True)

        #Transforme les données en str
        nb_passenger_str = np.array(nb_passenger_data[0]).astype(str)
        nb_passenger_str = np.insert(nb_passenger_str, 0, "0")

        # Ajouter le tuple pour la valeur "0"
        nb_passenger_data[1].insert(0, " ")

        #Paramétrage du graphique
        plt.bar(abscisse_pos, nb_passenger_str, align='edge', alpha=0.5, edgecolor='black')
        plt.xticks(abscisse_pos, nb_passenger_data[1], rotation=45, ha='right', fontsize=8)
        plt.ylabel('Number of Passengers')
        plt.title('Passenger Count by Airport in {}'.format(country))

        #Ajuster le graphique au layout
        plt.tight_layout()

        #Nommage et sauvegarde de l'image
        temp_file = 'graph_passenger.png'
        plt.savefig(temp_file, format='png', dpi=75)
        plt.close()

        self.image_label : QLabel = QLabel()
        self.image_label.setPixmap(QPixmap(temp_file))
        self.__layout.addLayout(self.__viewLayoutH)
        self.__layout.addWidget(self.image_label, Qt.AlignmentFlag.AlignCenter)

    def view_data_bar_airport_frequency(self, country: str):
        """Méthode permettant d'afficher une data visualisation de la fréquence d'utilisation des aeroport par pays

        Args:
            country (str): Le pays dont on veux connaitre le résultat de la requête
        """
        bdd = Bdd()
        data_frequency = bdd.getMostUseAirport(country)
        
        abscisse_pos = np.arange(len(data_frequency[0]) + 1)
        
        # Coche le bouton radio 2
        self.__qRadioBbtn2.setChecked(True)

        #Transforme les données en str
        frequency_str = np.array(data_frequency[1]).astype(str)
        frequency_str = np.insert(frequency_str, 0, "0")

        # Ajouter le tuple pour la valeur "0"
        data_frequency[0].insert(0, " ")
        
        #Paramétrage du graphique
        plt.bar(abscisse_pos, frequency_str, align='edge', alpha=0.5, edgecolor='black')
        plt.xticks(abscisse_pos, data_frequency[0], rotation=45, ha='right', fontsize=8)
        plt.ylabel('Frequency')
        plt.title('The most used airports in {}'.format(country))

        #Ajuster le graphique au layout
        plt.tight_layout()
        
        #Nommage et sauvegarde de l'image
        temp_file = 'graph_frequency.png'
        plt.savefig(temp_file, format='png', dpi=75)
        plt.close()

        image_label : QLabel = QLabel()
        image_label.setPixmap(QPixmap(temp_file))
        self.__layout.addLayout(self.__viewLayoutH)
        self.__layout.addWidget(image_label, Qt.AlignmentFlag.AlignCenter)
    
    def view_data_country(self, country : str):
        """Méthode permettant d'afficher une data visualisation de tout les aéroports d'un pays

        Args:
            country (str): le pays dont on veut connaitre les aéroports
        """
        bdd = Bdd()
        #On stock dans une varibale le résultat de la méthode
        airport_data = bdd.getPositionAeroportOfCountry(country)

        # Création d'un DataFrame Pandas à partir des données des aéroports
        df = pd.DataFrame(airport_data, columns=["name", "latitude", "longitude"])

        # Création d'une géo-série GeoPandas à partir du DataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Chargement de la carte du monde
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Affichage de la carte du monde et des points des aéroports
        fig, ax = plt.subplots(figsize=(12, 8))
        gdf.plot(ax=ax, markersize=10, color='red', alpha=0.7, zorder  = 2)
        world.boundary.plot(ax=ax, facecolor='lightgray', edgecolor='black', zorder = 1)

        # Paramètres de l'affichage
        ax.set_title('Airport Locations')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_aspect('equal')

        # Définir les limites de zoom sur l'Europe
        ax.set_xlim(-30, 50)  # Ajuster ces valeurs en fonction de la zone d'intérêt
        ax.set_ylim(30, 80)   # Ajuster ces valeurs en fonction de la zone d'intérêt


        # Enregistrer la carte au format PNG
        temp_file = 'map.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        # Charger l'image dans QLabel
        self.image_label : QLabel = QLabel()
        self.image_label.setPixmap(QPixmap(temp_file).scaled(500,500))
        self.__layout.addLayout(self.__viewLayoutH)
        self.__layout.addWidget(self.image_label, Qt.AlignmentFlag.AlignCenter)

    def view_data_airport(self, airport : str):
        """Méthode permettant d'afficher une data visualisation sous forme de map monde représentant un aéroport d'un pays

        Args:
            airport (str): l'aeroport dont on veut connaitre la position

        """
        bdd = Bdd()
        #On stock dans une variable le résultat de la méthode
        airport_data = bdd.getPositionAeroport(airport)
        print(airport_data)
        # Création d'un DataFrame Pandas à partir des données des aéroports
        df = pd.DataFrame(airport_data, columns=["name", "latitude", "longitude"])

        # Création d'une géo-série GeoPandas à partir du DataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Chargement de la carte du monde
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        
        # Affichage de la carte du monde et des points des aéroports
        fig, ax = plt.subplots(figsize=(12, 8))
        gdf.plot(ax=ax, markersize=10, color='red', alpha=0.7, zorder = 2)
        world.boundary.plot(ax=ax, facecolor='lightgray', edgecolor='black', zorder = 1)
        

        # Paramètres de l'affichage
        ax.set_title('Airport Locations')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_aspect('equal')

        # Définir les limites de zoom sur l'Europe
        ax.set_xlim(-30, 50)  # Ajuster ces valeurs en fonction de la zone d'intérêt
        ax.set_ylim(30, 80)   # Ajuster ces valeurs en fonction de la zone d'intérêt
        
        # Enregistrer la carte au format PNG
        temp_file = 'map.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        # Charger l'image dans QLabel
        self.image_label : QLabel = QLabel()
        self.image_label.setPixmap(QPixmap(temp_file).scaled(500,500))
        self.__layout.addLayout(self.__viewLayoutH)
        self.__layout.addWidget(self.image_label, Qt.AlignmentFlag.AlignCenter)
    
    def refresh(self, country : str = ""):
        """Rafraichi la vue en fonction du pays

        Args:
            country (str): country. Defaults to "".
        """
        if self.__qRadioBbtn1.isChecked() == True:
            self.clear()
            self.view_data_bar_nb_passenger_transport(country)
        elif self.__qRadioBbtn2.isChecked() == True:
            self.clear()
            self.view_data_bar_airport_frequency(country)
        elif self.__qRadioBbtn3.isChecked() == True:
            self.clear()
            self.view_data_country(country)
            #TODO: Ajouter un fonctionnalité pour lancer la méthode view_data_airport

    def qRadioBbtnSignalFunc(self):
        self.qRadioBtnSignal.emit()

    def clear(self):
        """Supprime le widget du layout
        """
        if self.__layout.count() > 1:
            self.__layout.removeWidget(self.__layout.itemAt(1).widget())