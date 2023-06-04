
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import sys

class ViewDataMapWidget(QWidget):
    """Classe représentant un widget contenant une data visualisation map monde

    Args:
        QWidget (QWidget): hérite de QWidget
    """

    def __init__(self):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.resize(50,50)
        self.setLayout(self.__layout)
        
        

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
        image_label = QLabel()
        pixmap = QPixmap(temp_file).scaled(500, 500)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)
        
        
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
        image_label = QLabel()
        pixmap = QPixmap(temp_file).scaled(500, 500)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)
