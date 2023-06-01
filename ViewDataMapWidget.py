
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

    def __init__(self):
        super().__init__()

        self.__label = QLabel("salut")
        self.__layout = QVBoxLayout()
        self.resize(50,50)

        temp_file = self.view_data()

        # Charger l'image dans QLabel
        image_label = QLabel()
        pixmap = QPixmap(temp_file).scaled(500, 500)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)

        self.setLayout(self.__layout)
        
        

    def view_data(self) -> str:
        bdd = Bdd()
        airport_data = bdd.getPositionAeroport("France")

        # Création d'un DataFrame Pandas à partir des données des aéroports
        df = pd.DataFrame(airport_data, columns=["name", "latitude", "longitude"])

        df['latitude'] = df['latitude'].str.replace(',', '.')
        df['longitude'] = df['longitude'].str.replace(',', '.')
        # Création d'une géo-série GeoPandas à partir du DataFrame
        geometry = [Point(xy) for xy in zip(df['longitude'], df['latitude'])]
        gdf = gpd.GeoDataFrame(df, geometry=geometry)

        # Chargement de la carte du monde
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

        # Affichage de la carte du monde et des points des aéroports
        fig, ax = plt.subplots(figsize=(12, 8))
        world.plot(ax=ax, color='lightgray')
        gdf.plot(ax=ax, markersize=5, color='red', alpha=0.5)

        # Paramètres de l'affichage
        ax.set_title('Airport Locations')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        ax.set_aspect('equal')

        # Enregistrer la carte au format PNG
        temp_file = 'map.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        return temp_file
        











#     self.setWindowTitle("Airport Data")
    #     self.resize(800, 600)
    #     self.setLayout(QVBoxLayout())
        
    #     self.bdd = Bdd()
    #     self.view_data()

    # def view_data(self):

    #     query = QSqlQuery("SELECT country_ap, COUNT(*) as count FROM airport GROUP BY country_ap")

    #     series = QBarSeries()

    #     while query.next():
    #         country = query.value("country_ap")
    #         count = query.value("count")

    #         bar_set = QBarSet(country)
    #         bar_set.append(count)
    #         series.append(bar_set)

    #     chart = QChart()
    #     chart.addSeries(series)
    #     chart.setTitle("Number of Airports by Country")
    #     chart.setAnimationOptions(QChart.SeriesAnimations)

    #     axis_x = QBarCategoryAxis()
    #     chart.addAxis(axis_x, Qt.AlignBottom)
    #     series.attachAxis(axis_x)

    #     axis_y = QValueAxis()
    #     chart.addAxis(axis_y, Qt.AlignLeft)
    #     series.attachAxis(axis_y)

    #     chart_view = QChartView(chart)
    #     chart_view.setRenderHint(QPainter.Antialiasing)
    #     chart_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #     self.layout().addWidget(chart_view)






# if __name__ == "__main__":
#     app = QApplication(sys.argv)

#     view = ViewDataMapWidget()
#     view.show()

#     sys.exit(app.exec())