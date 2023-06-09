from PyQt6.QtWidgets import QApplication, QTabWidget, QWidget
from InfosCountryAndAirport import InfosCountryAndAirport
from ViewDataCo2Widget import ViewDataCo2Widget
from RouteWidget import RouteWidget
from BddControler import BddControler
import sys

class win(QTabWidget): 
    """Créer la fenêtre principale

    """
    
    def __init__(self): 
        super().__init__()

        self.setMinimumSize(1250, 500)
        # TODO Changer le nom du logiciel
        self.setWindowTitle("UI Avions")        

        self.bdd : BddControler = BddControler()

        # Ajoute le widget principal au QTabBar
        self.addTab(InfosCountryAndAirport(self.bdd), "Informations sur les pays/aéroports")
        self.addTab(ViewDataCo2Widget(self.bdd), "CO2")
        self.addTab(RouteWidget(self.bdd), "Route")
        self.addTab(QWidget(), "Compagnie aérienne")
        self.addTab(QWidget(), "Avion")

        # Affiche la fenêtre
        self.show()
    
    def closeConnection(self):
        self.bdd.closeConnection()


if __name__ == "__main__": 
    print(f'main') 
    app = QApplication(sys.argv) 
    f = win() 
    sys.exit(app.exec())
    f.closeConnection()