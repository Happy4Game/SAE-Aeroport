from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtSql import QSqlDatabase, QSqlQuery
from PySide6.QtCharts import QChartView, QLineSeries, QChart, QBarSeries, QBarSet, QBarCategoryAxis
from PySide6.QtGui import QPainter
from Bdd import Bdd

class ViewDataLayout(QVBoxLayout):
    def __init__(self):
        super().__init__()

        self.__label = QLabel("Visualisation")
        
        self.addWidget(self.__label)
        
        
    def load_data(self, bdd):
        query, data = bdd.getAirFrancePlaneSeats()

        series = QBarSeries()

        bar_set = QBarSet("Number of Seats")

        for row in data:
            plane_name = row[0]
            seat_count = row[1]
            bar_set.append(seat_count)

            # Ajoutez l'étiquette de nom d'avion à l'axe des catégories
            category_axis = self.__view.chart().axisX()
            category_axis.append(plane_name)

        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        chart.setAxisX(axis_x, series)
        self.chartview = QChartView(chart)
        self.addWidget(self.chartview)

    def paintEvent(self, event):
        # S'assure que la vue est correctement rendue lorsque la fenêtre est redimensionnée
        self.__view.setGeometry(self.rect())
        super().paintEvent(event)


