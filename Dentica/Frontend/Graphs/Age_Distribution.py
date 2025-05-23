from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class PatientAgeDistributionPie(QWidget):
    def __init__(self, data_labels, data_values, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(2, 2))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.figure.subplots_adjust(right=0.8)
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0,0,0,0)
        self.draw_chart(data_labels, data_values)

    def draw_chart(self, labels, values):
        ax = self.figure.add_subplot(111)
        ax.clear()
        colors = ['#5e93bf', '#99c4e7', '#1d1f27', '#37547A']  
        wedges, texts, autotexts = ax.pie(
            values,
            labels=labels,
            autopct='%1.1f%%',
            startangle=90,
            colors=colors
        )
        for text in texts:
            text.set_fontsize(8)

        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontweight('bold')
            autotext.set_fontsize(10)
            x, y = autotext.get_position()
            autotext.set_position((x * 1.2, y * 1.2))

        ax.axis('equal')
        self.canvas.draw()
