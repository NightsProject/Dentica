from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.dates as mdates

class TreatmentCostsLineChart(QWidget):
    def __init__(self, data_dates, data_costs, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(5, 2.5))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(data_dates, data_costs)

    def draw_chart(self, dates, costs):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(dates, costs, color='#5e93bf', marker='o')
        ax.set_title('Treatment Costs Over Time', fontsize=10, fontweight='bold', color='#37547A')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_facecolor('#C6D7EC')

        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
        ax.tick_params(axis='x', rotation=45, labelsize=7)
        ax.tick_params(axis='y', labelsize=8)
        ax.set_ylabel('Cost', fontsize=9, color='#37547A')
        self.figure.subplots_adjust(left=0.22, right=0.95, bottom=0.25)
        self.canvas.draw()