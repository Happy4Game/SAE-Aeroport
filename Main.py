from PyQt6.QtWidgets import QApplication, QWidget, QTabWidget
from InfosCountryAndAirport import InfosCountryAndAirport
import sys

class win(QTabWidget): 
    """Créer la fenêtre principale

    """
    
    def __init__(self): 
        super().__init__()

        self.setMinimumSize(1250, 500)
        # TODO Changer le nom du logiciel
        self.setWindowTitle("UI Avions")        

        # Ajoute le widget principal au QTabBar
        self.addTab(InfosCountryAndAirport(), "Informations sur les pays/aéroports")
        self.addTab(ViewDataCo2Widget(), "CO2")

        # Affiche la fenêtre
        self.show()


if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())