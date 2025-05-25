from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class QuarterlyRevenueLineChart(QWidget):
    def __init__(self, quarters, revenues, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(4, 2.5))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(quarters, revenues)

    def draw_chart(self, quarters, revenues):
        ax = self.figure.add_subplot(111)
        ax.clear()
        ax.plot(quarters, revenues, marker='o', color='#37547A', linewidth=2)
        ax.set_facecolor('#C6D7EC')
        ax.set_title("Quarterly Revenue", fontsize=10, fontweight='bold', color='#37547A')
        ax.set_ylabel('Amount Paid', fontsize=9, color='#37547A')
        ax.set_xticks(range(len(quarters)))
        ax.set_xticklabels(quarters, rotation=45, fontsize=8, color='#37547A')
        ax.tick_params(axis='y', labelsize=10, color='#000')

        # Bold and white y-tick labels (like pie chart values)
        for label in ax.get_yticklabels():
            label.set_color('black')
            label.set_fontsize(10)

        ax.grid(True, linestyle='--', alpha=0.6)
        self.figure.subplots_adjust(left=0.18, bottom=0.25)
        self.canvas.draw()
