from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
import numpy as np
import sys
from PyQt6.QtSql import QSqlQuery

class ViewDataBarWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.__layout = QVBoxLayout()
        self.resize(50,50)
        self.setLayout(self.__layout)
        

    def view_data_bar_nb_passenger_transport(self, country: str):
        bdd = Bdd()
        nb_passenger_data = bdd.getNbPassengerByAirport(country)

        y_pos = np.arange(len(nb_passenger_data[1]) + 1)

        nb_passenger_str = np.array(nb_passenger_data[0]).astype(str)
        nb_passenger_str = np.insert(nb_passenger_str, 0, "0")

        # Ajouter le tuple pour la valeur "0"
        nb_passenger_data[1].insert(0, " ")

        fig, ax = plt.subplots()
        plt.bar(y_pos, nb_passenger_str, align='edge', alpha=0.5, edgecolor='black')
        plt.xticks(y_pos, nb_passenger_data[1], rotation=45, ha='right', fontsize=8)
        plt.ylabel('Number of Passengers')
        plt.title('Passenger Count by Airport in {}'.format(country))

        plt.tight_layout()

        ax.set_ylim(bottom=0)

        temp_file = 'graph_passenger.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        image_label = QLabel()
        pixmap = QPixmap(temp_file)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)

    def view_data_bar_airport_frequency(self, country: str):
        bdd = Bdd()
        data_frequency = bdd.getMostUseAirport(country)
        
        y_pos = np.arange(len(data_frequency[0]) + 1)
        
        frequency_str = np.array(data_frequency[1]).astype(str)
        frequency_str = np.insert(frequency_str, 0, "0")

        # Ajouter le tuple pour la valeur "0"
        data_frequency[0].insert(0, " ")
        
        fig, ax = plt.subplots()
        plt.bar(y_pos, frequency_str, align='edge', alpha=0.5, edgecolor='black')
        plt.xticks(y_pos, data_frequency[0], rotation=45, ha='right', fontsize=8)
        plt.ylabel('Frequency')
        plt.title('The most used airports in {}'.format(country))

        plt.tight_layout()

        ax.set_ylim(bottom=0)

        temp_file = 'graph_frequency.png'
        plt.savefig(temp_file, format='png')
        plt.close()

        image_label = QLabel()
        pixmap = QPixmap(temp_file)
        image_label.setPixmap(pixmap)
        self.__layout.addWidget(image_label)
