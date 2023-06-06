from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QRadioButton
from PyQt6.QtCore import Qt, pyqtSignal
from Bdd import Bdd
from PyQt6.QtGui import QPixmap
import matplotlib.pyplot as plt
import numpy as np


class ViewDataBarWidget(QWidget):
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
        self.__qRadioBbtn1 : QRadioButton = QRadioButton("Affichage des aeoroports")
        self.__qRadioBbtn1.setChecked(True)
        self.__qRadioBbtn1.clicked.connect(self.qRadioBbtnSignalFunc)
        self.__qRadioBbtn2 : QRadioButton = QRadioButton("Aeroports les plus fréquentés")
        self.__qRadioBbtn2.clicked.connect(self.qRadioBbtnSignalFunc)
        
        self.__viewLayoutH.addWidget(self.__qRadioBbtn1)
        self.__viewLayoutH.addWidget(self.__qRadioBbtn2)

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

    def qRadioBbtnSignalFunc(self):
        self.qRadioBtnSignal.emit()

    def clear(self):
        """Supprime le widget du layout
        """
        if self.__layout.count() > 1:
            self.__layout.removeWidget(self.__layout.itemAt(1).widget())