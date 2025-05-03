import sys
from PyQt6 import QtWidgets

from Frontend.denticagui_main import Ui_MainWindow


#===== Initialize MainWindow ==========
def initialize_mainWindow():
    app = QtWidgets.QApplication(sys.argv)

    # Show the main window
    main_window = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(main_window)
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    initialize_mainWindow()






