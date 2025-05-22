from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

class DonutChart(QWidget):
    def __init__(self, data_labels, data_values, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        self.figure = Figure(figsize=(4, 4))
        self.figure.patch.set_facecolor('#C6D7EC')
        self.graph_cont = QtWidgets.QFrame()
        self.graph_cont.setStyleSheet('border: 1px solid black')
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)
        self.draw_chart(data_labels, data_values)

    def draw_chart(self, labels, values):
        ax = self.figure.add_subplot(111)
        ax.clear()
        colors = ['#1d1f27', '#5e93bf', '#99c4e7']
        wedges, texts = ax.pie(values, labels=None, autopct=None,
                            startangle=90, wedgeprops=dict(width=0.4), colors=colors)
        total = sum(values)
        ax.axis('off')

        
        self.figure.subplots_adjust(right=0.7)  

        ax.legend(wedges, labels, title=None, loc="center left", bbox_to_anchor=(1.05, 0.25), frameon=False)
        self.canvas.draw()

    # def update_dashboard_chart(self, new_values):
    #     labels = ['Scheduled', 'Completed', 'Cancelled']

    #     # Find the layout set on self.dash_graph
    #     layout = self.dash_graph.layout()

    #     # Remove the old donut chart (assuming it's the last widget in the layout)
    #     if layout.count() > 1:
    #         old_chart = layout.itemAt(1).widget()
    #         if old_chart:
    #             layout.removeWidget(old_chart)
    #             old_chart.deleteLater()  # Free memory

    #     # Add new chart with updated values
    #     new_chart = DonutChart(labels, new_values)
    #     layout.addWidget(new_chart)