from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6 import QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class PaymentMethodPie(QWidget):
    def __init__(self, data_labels, data_values, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(4, 4))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(data_labels, data_values)

    def draw_chart(self, labels, values):
        ax = self.figure.add_subplot(111)
        ax.clear()
        colors = ['#1d1f27', '#5e93bf', '#99c4e7']  
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
            # Optional: move values slightly outward
            x, y = autotext.get_position()
            autotext.set_position((x * 1.2, y * 1.2))

        ax.axis('equal')  # keep pie circular
        self.canvas.draw()
