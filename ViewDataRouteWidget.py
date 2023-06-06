from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import sys

class ViewDataRouteWidget(QWidget):
    """Classe représentant un widget contenant une data visualisation map monde

    Args:
        QWidget (QWidget): hérite de QWidget
    """

    def __init__(self):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.resize(50,50)
        self.setLayout(self.__layout)

    def view_data_route(self, depart :str, destination:str):
        """Méthode permettant d'afficher une data visualisation de la route entre deux aéroports

        Args:
            depart (str): aéroport de départ
            destination (str): aéroport d'arrivée
        """
        bdd = Bdd()
        #On stock dans une varibale le résultat de la méthode
        airport_data_depart = bdd.getInfoAirportRoute(depart)
        print(airport_data_depart)
        depart_name = airport_data_depart[0]
        depart_longitude = int(airport_data_depart[1])
        depart_latitude = int(airport_data_depart[2])
        airport_data_arrivee = bdd.getInfoByAirportRoute(destination)
        print(airport_data_arrivee)
        arrivee_name = airport_data_arrivee[0]
        arrivee_longitude = int(airport_data_arrivee[1])
        arrivee_latitude = int(airport_data_arrivee[2])

        # Création du DataFrame pour les aéroports de départ et d'arrivée
        df = pd.DataFrame({
            "name": [depart_name, arrivee_name],
            "longitude": [depart_longitude, depart_latitude],
            "latitude": [depart_latitude, arrivee_latitude]
        })

        # Création d'une géo-série GeoPandas à partir du DataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Chargement de la carte du monde
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Affichage de la carte du monde et des points des aéroports
        fig, ax = plt.subplots(figsize=(12, 8))
        gdf.plot(ax=ax, markersize=10, color="red", alpha=0.7, zorder=2)
        world.boundary.plot(ax=ax, facecolor="lightgray", edgecolor="black", zorder=1)

        # Tracé de la route entre les aéroports de départ et d'arrivée
        plt.plot(
            [depart_longitude, arrivee_longitude],
            [depart_latitude, arrivee_latitude],
            color="blue",
            linewidth=2,
            alpha=0.7,
            zorder=3,
        )

        # Paramètres de l'affichage
        ax.set_title("Route between Airports")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_aspect("equal")

        # Définir les limites de zoom sur l'Europe
        #ax.set_xlim(-30, 50)  # Ajuster ces valeurs en fonction de la zone d'intérêt
        #ax.set_ylim(30, 80)   # Ajuster ces valeurs en fonction de la zone d'intérêt

        # Définir les limites de zoom pour inclure les aéroports de départ et d'arrivée
        min_longitude = min(depart_longitude, arrivee_longitude) - 5
        max_longitude = max(depart_longitude, arrivee_longitude) + 5
        min_latitude = min(depart_latitude, arrivee_latitude) - 5
        max_latitude = max(depart_latitude, arrivee_latitude) + 5
        ax.set_xlim(min_longitude, max_longitude)
        ax.set_ylim(min_latitude, max_latitude)

        # Enregistrer la carte au format PNG
        temp_file = "route.png"
        plt.savefig(temp_file, format="png")
        plt.close()

        # Charger l'image dans QLabel
        image_label = QLabel()
        pixmap = QPixmap(temp_file).scaled(500, 500)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)