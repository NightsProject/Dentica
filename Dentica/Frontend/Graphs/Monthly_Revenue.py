from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class QuarterlyRevenueLineChart(QWidget):
    def __init__(self, months, revenues, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(4, 2.5))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(months, revenues)

    def draw_chart(self, months, revenues):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(months, revenues, marker='o', color='#37547A', linewidth=2)
        ax.set_facecolor('#C6D7EC')
        ax.tick_params(axis='x', rotation=45, labelsize=8)  
        ax.set_ylabel('Amount Paid')
        ax.grid(True, linestyle='--', alpha=0.6)
        self.figure.subplots_adjust(left=0.15, bottom=0.25)
        self.canvas.draw()
