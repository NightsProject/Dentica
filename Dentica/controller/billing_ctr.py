from PyQt6 import QtCore
from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import QRegularExpression, pyqtSignal
from ui.Dialogues.ui_billing_dialog import Add_Payment


class Billing_Dialog_Ctr(Add_Payment):
    payment_added = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)