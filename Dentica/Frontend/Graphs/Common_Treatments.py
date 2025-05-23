from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class CommonTreatmentsBarChart(QWidget):
    def __init__(self, procedures, counts, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(4, 2.5))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(procedures, counts)

    def draw_chart(self, procedures, counts):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.set_facecolor('#C6D7EC')
        colors = ['#5e93bf', '#99c4e7', '#1d1f27', '#7fa9d9']
        bars = ax.bar(procedures, counts, color=colors[:len(procedures)])
        ax.set_xticks([])
        ax.set_xticklabels([])
        for bar, label in zip(bars, procedures):
            bar.set_label(label)
        ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.6), fontsize=8, frameon=False)
        ax.bar_label(bars, padding=3, fontsize=10, color='white', fontweight='bold')
        self.figure.subplots_adjust(left=0.08, right=0.78, bottom=0.2)

        self.canvas.draw()