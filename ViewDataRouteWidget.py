from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point


class ViewDataRouteWidget(QWidget):
    """Classe représentant un widget contenant une data visualisation diagramme en barre

    Args:
        QWidget (QWidget): hérite de QWidget
    """

    def __init__(self, depart : str, destination : str):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.setLayout(self.__layout)

        if depart != "" and destination != "":
            self.clear()
            self.view_data_route(depart, destination)

    def view_data_route(self, depart : str, destination : str):
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
        print(depart_name)
        depart_longitude = float(airport_data_depart[1])
        print(depart_longitude)
        depart_latitude = float(airport_data_depart[2])
        print(depart_latitude)
        airport_data_arrivee = bdd.getInfoAirportRoute(destination)
        print(airport_data_arrivee)
        arrivee_name = airport_data_arrivee[0]
        arrivee_longitude = float(airport_data_arrivee[1])
        arrivee_latitude = float(airport_data_arrivee[2])

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
            color="red",
            linewidth=3, #Epaisseur de ligne
            linestyle = "--", #Style de ligne
            alpha=0.7,
            zorder=3,
        )

        # Paramètres de l'affichage
        ax.set_title("Route between Airports")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.set_aspect("equal")

        # Définir les limites de zoom sur l'Europe
        ax.set_xlim(-30, 50)  # Ajuster ces valeurs en fonction de la zone d'intérêt
        ax.set_ylim(30, 80)   # Ajuster ces valeurs en fonction de la zone d'intérêt

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

        # Charger l'image dans un QLabel
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(temp_file).scaled(500, 500))
        self.__layout.addWidget(self.image_label)

    def clear(self):
        """Supprime le widget du layout
        """
        if self.__layout.count() > 1:
            self.__layout.removeWidget(self.__layout.itemAt(1).widget())
        elif self.__layout.count() == 1:
            self.__layout.removeWidget(self.__layout.itemAt(0).widget())
            
        