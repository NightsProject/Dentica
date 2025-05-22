from PyQt6 import QtCore, QtGui, QtWidgets


class PatientPage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.patient = QtWidgets.QLabel("Patient Profile", self)
        self.patient.setGeometry(QtCore.QRect(20, 25, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(18)
        font.setBold(True)
        self.patient.setFont(font)
        self.patient.setStyleSheet("background-color: #B2CDE9; color: #0E283F;")
        
        #profile card
        self.profile_card = QtWidgets.QFrame(self)
        self.profile_card.setGeometry(QtCore.QRect(30, 60, 250, 350))
        self.profile_card.setStyleSheet("""
        #profile_card {
                background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.profile_card.setObjectName("profile_card")
        
        #details card
        self.profile_card2 = QtWidgets.QFrame(self)
        self.profile_card2.setGeometry(QtCore.QRect(310, 60, 600, 350))
        self.profile_card2.setStyleSheet("""
        #profile_card2 {
                background: #C6D7EC; 
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.profile_card2.setObjectName("profile_card2")
        
        self.mainlayout = QtWidgets.QHBoxLayout()
        
        self.left_layout = QtWidgets.QVBoxLayout()
        self.fn = QtWidgets.QLabel()
        self.fn.setText("First Name:")
        self.fn.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B; ")
        self.left_layout.addWidget(self.fn)
        self.fnval = QtWidgets.QLabel()
        self.fnval.setText("TestF")
        self.fnval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.left_layout.addWidget(self.fnval)
        self.address = QtWidgets.QLabel()
        self.address.setText("Address:")
        self.address.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.left_layout.addWidget(self.address)
        self.adval = QtWidgets.QLabel()
        self.adval.setText("Saray")
        self.adval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.left_layout.addWidget(self.adval)
        self.email = QtWidgets.QLabel()
        self.email.setText("Email Address:")
        self.email.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.left_layout.addWidget(self.email)
        self.emailval = QtWidgets.QLabel()
        self.emailval.setText("testemail@gmail.com")
        self.emailval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.left_layout.addWidget(self.emailval)
        
        self.mid_layout = QtWidgets.QVBoxLayout()
        self.mn = QtWidgets.QLabel()
        self.mn.setText("Middle Name:")
        self.mn.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.mid_layout.addWidget(self.mn)
        self.mnval = QtWidgets.QLabel()
        self.mnval.setText("TestM")
        self.mnval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.mid_layout.addWidget(self.mnval)
        self.gender = QtWidgets.QLabel()
        self.gender.setText("Gender:")
        self.gender.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.mid_layout.addWidget(self.gender)
        self.genval = QtWidgets.QLabel()
        self.genval.setText("Male")
        self.genval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.mid_layout.addWidget(self.genval)
        self.birth_date = QtWidgets.QLabel()
        self.birth_date.setText("Birth Date:")
        self.birth_date.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.mid_layout.addWidget(self.birth_date)
        self.bdval = QtWidgets.QLabel()
        self.bdval.setText("12-02-1997")
        self.bdval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.mid_layout.addWidget(self.bdval)
        
        self.right_layout = QtWidgets.QVBoxLayout()
        self.ln = QtWidgets.QLabel()
        self.ln.setText("Last Name:")
        self.ln.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.right_layout.addWidget(self.ln)
        self.lndval = QtWidgets.QLabel()
        self.lndval.setText("TestL")
        self.lndval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.right_layout.addWidget(self.lndval)
        self.contact = QtWidgets.QLabel()
        self.contact.setText("Contact:")
        self.contact.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.right_layout.addWidget(self.contact)
        self.condval = QtWidgets.QLabel()
        self.condval.setText("0999231235")
        self.condval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 18px; ")
        self.right_layout.addWidget(self.condval)
        self.blank = QtWidgets.QLabel()
        self.blank.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.right_layout.addWidget(self.blank)
        self.blankdval = QtWidgets.QLabel()
        self.blankdval.setStyleSheet("background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;")
        self.right_layout.addWidget(self.blankdval)
        
        self.mainlayout.addLayout(self.left_layout)
        self.mainlayout.addLayout(self.mid_layout)
        self.mainlayout.addLayout(self.right_layout)
        self.profile_card2.setLayout(self.mainlayout)
        
        # Reduce spacing and margins for tighter layout
        for layout in [self.left_layout, self.mid_layout, self.right_layout]:
                layout.setSpacing(0)
                layout.setContentsMargins(0, 0, 0, 0)

        # Set tighter spacing for the main layout too
        self.mainlayout.setSpacing(10)
        self.mainlayout.setContentsMargins(10, 10, 10, 10)  # Adjust outer padding
        
        
        #history card
        self.profile_card3 = QtWidgets.QFrame(self)
        self.profile_card3.setGeometry(QtCore.QRect(30, 420, 880, 370))
        self.profile_card3.setStyleSheet("""
        #profile_card3 {
                background: #C6D7EC; font-family: Inter; font-size: 14px; color: #64748B;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.profile_card3.setObjectName("profile_card3")
        self.AppHis = QtWidgets.QLabel("Appointment History", parent=self.profile_card3)
        self.AppHis.setGeometry(QtCore.QRect(20, 20, 200, 20))
        self.AppHis.setStyleSheet("background: #C6D7EC; color: #37547A; font-family: Inter; font-size: 16px; font-weight: bold;")
       
       