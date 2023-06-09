from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt
from BddControler import BddControler
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd

class ViewDataCo2Widget(QWidget):
    def __init__(self, bdd : BddControler):
        super().__init__()

        self.bdd = bdd

        self.__layout = QVBoxLayout()
        self.view_data_co2()
        self.setLayout(self.__layout)
        
    
    def view_data_co2(self):
        co2_data = self.bdd.getTotalCo2ByCountry()
        print(co2_data)
        # Créer un DataFrame à partir des données de CO2
        df = pd.DataFrame(co2_data, columns=["co2", "pays"])

        # Fusionner les données de CO2 avec les données de la carte du monde
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
        merged = world.merge(df, left_on='name', right_on='pays', how='left')

        # Tracer les données fusionnées
        fig, ax = plt.subplots(figsize=(12, 8))
        merged.plot(column='co2', cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8', legend=True)

        # Définir le titre et les étiquettes du graphique
        ax.set_title('Émissions de CO2 par pays')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')

        # Définir le rapport d'aspect et les limites de zoom
        ax.set_aspect('equal')
        ax.set_xlim(-30, 50)  # Ajustez ces valeurs en fonction de la zone d'intérêt
        ax.set_ylim(30, 80)   # Ajustez ces valeurs en fonction de la zone d'intérêt

        # Enregistrer la carte sous forme de fichier PNG
        temp_file = 'co2.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        # Charger l'image dans un QLabel
        self.image_label = QLabel()
        self.image_label.setPixmap(QPixmap(temp_file))
        self.__layout.addWidget(self.image_label, Qt.AlignmentFlag.AlignCenter)