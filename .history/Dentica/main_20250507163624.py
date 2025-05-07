import sys
from PyQt6 import QtWidgets

from controller.main_controller import MainController

#===== Initialize MainWindow ==========
def main():
    app = QtWidgets.QApplication(sys.argv)
    
    # Show the main window
    ui = MainController()
    ui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()






