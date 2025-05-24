from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class AppointmentLineChart(QWidget):
    def __init__(self, x_labels, y_values, title="Appointments Over Time", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(5, 3))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(x_labels, y_values, title)

    def draw_chart(self, x_labels, y_values, title):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(x_labels, y_values, marker='o', color='#5e93bf', linewidth=2)
        ax.set_facecolor('#C6D7EC')
        ax.set_title(title, fontsize=12)
        ax.set_xlabel("Week")
        ax.set_ylabel("No. of Appointments", fontsize=7, color='#37547A')
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.tick_params(axis='x', rotation=45)
        self.figure.tight_layout()
        self.canvas.draw()
