from PyQt6 import QtCore, QtGui, QtWidgets

filepath = "Dentica/ui/icons/"

class Ui_MainWindow(object):
   
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(1200, 800)
        MainWindow.setWindowTitle("Dentica")
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #Sidebar Frame
        self.SidebarFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.SidebarFrame.setGeometry(QtCore.QRect(0, 0, 260, 780))
        self.SidebarFrame.setAutoFillBackground(False)
        self.SidebarFrame.setStyleSheet("background-color: #fff; border-right: 1px solid #E5E7EB;")
        self.SidebarFrame.setObjectName("SidebarFrame")

        #Dentica Label
        self.Dentica = QtWidgets.QLabel(parent=self.SidebarFrame)
        self.Dentica.setGeometry(QtCore.QRect(70, 25, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(20)
        font.setBold(True)
        self.Dentica.setFont(font)
        self.Dentica.setStyleSheet("""border: none;
                                      color: black;
                                      """)
        self.Dentica.setObjectName("Dentica")

        #Sidebar Layout
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.SidebarFrame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 80, 260, 620))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setSpacing(20)
        self.verticalLayout.setContentsMargins(24, 24, 24, 24)
        
        #Dashboard Button
        self.Dash_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        dash_icon = QtGui.QIcon(f"{filepath}Dashboard.svg")
        self.Dash_btn.setIcon(dash_icon)
        self.Dash_btn.setIconSize(QtCore.QSize(25, 25))
        self.Dash_btn.setObjectName("Dash_btn")
        self.Dash_btn.clicked.connect(lambda : self.Pages.setCurrentIndex(0))
        self.Dash_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.verticalLayout.addWidget(self.Dash_btn)
        

        #Patient button
        self.Patient_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        pat_icon = QtGui.QIcon(f"{filepath}Patients.svg")
        self.Patient_btn.setIcon(pat_icon)
        self.Patient_btn.setIconSize(QtCore.QSize(25, 25))
        self.Patient_btn.setObjectName("Patient_btn")
        self.Patient_btn.clicked.connect(lambda : self.Pages.setCurrentIndex(1))
        self.Patient_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.verticalLayout.addWidget(self.Patient_btn)
        
        

        #Appointment button
        self.Apntmnt_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        apt_icon = QtGui.QIcon(f"{filepath}Appointments.svg")
        self.Apntmnt_btn.setIcon(apt_icon)
        self.Apntmnt_btn.setIconSize(QtCore.QSize(25, 25))
        self.Apntmnt_btn.setObjectName("Apntmnt_btn")
        self.Apntmnt_btn.clicked.connect(lambda : self.Pages.setCurrentIndex(2))
        self.Apntmnt_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.verticalLayout.addWidget(self.Apntmnt_btn)
        

        #Billing button
        self.Bill_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        bil_icon = QtGui.QIcon(f"{filepath}Billing.svg")
        self.Bill_btn.setIcon(bil_icon)
        self.Bill_btn.setIconSize(QtCore.QSize(25, 25))
        self.Bill_btn.setObjectName("Bill_btn")
        self.Bill_btn.clicked.connect(lambda : self.Pages.setCurrentIndex(3))
        self.Bill_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.verticalLayout.addWidget(self.Bill_btn)
        

        #Reports button
        self.Rep_btn = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        rep_icon= QtGui.QIcon(f"{filepath}Reports.svg")
        self.Rep_btn.setIcon(rep_icon)
        self.Rep_btn.setIconSize(QtCore.QSize(25, 25))
        self.Rep_btn.setObjectName("Rep_btn")
        self.Rep_btn.clicked.connect(lambda : self.Pages.setCurrentIndex(4))
        self.Rep_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.verticalLayout.addWidget(self.Rep_btn)
        self.verticalLayout.addStretch()
        

        #Pages
        self.Pages = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.Pages.setGeometry(QtCore.QRect(260, 0, 1200, 800))
        self.Pages.setStyleSheet("""background: #F8FAFC;
                                    color: black;
                                    """)
        self.Pages.setObjectName("Pages")
        self.Dashboard_page = QtWidgets.QWidget()
        self.Dashboard_page.setObjectName("Dashboard_page")
        

        #Dashboard top bar
        self.frame = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.frame.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.frame.setStyleSheet("""
                #frame { background-color: #fff; border-bottom: 1px solid #E5E7EB;
                        }
                                 """)
        self.frame.setObjectName("frame")


        self.label = QtWidgets.QLabel(parent=self.frame)
        self.label.setGeometry(QtCore.QRect(20, 25, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(18)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("background-color: #fff;")
        self.label.setObjectName("label")

        #Notification button
        self.not_btn = QtWidgets.QPushButton(parent=self.frame)
        self.not_btn.setGeometry(QtCore.QRect(830, 23, 40, 40))
        self.not_btn.setText("")
        not_icon = QtGui.QIcon(f"{filepath}Notification.svg")
        self.not_btn.setIcon(not_icon)
        self.not_btn.setIconSize(QtCore.QSize(25, 25))
        self.not_btn.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;                   
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }                           
        """)
        self.not_btn.setObjectName("not_btn")

        #User button
        self.userbtn = QtWidgets.QPushButton(parent=self.frame)
        self.userbtn.setGeometry(QtCore.QRect(880, 23, 40, 40)) 
        user_icon = QtGui.QIcon(f"{filepath}User.svg")
        self.userbtn.setIcon(user_icon)
        self.userbtn.setIconSize(QtCore.QSize(25, 25))
        self.userbtn.setIconSize(QtCore.QSize(25, 25))
        self.userbtn.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        
        self.userbtn.clicked.connect(lambda: self.toggle_dropdown(self.userbtn, self.centralwidget, self.user_menu))
        self.userbtn.setObjectName("userbtn")

        #User menu drop-down
        self.user_menu = QtWidgets.QFrame(parent = self.centralwidget)
        self.user_menu.setObjectName("user_menu")
        self.user_menu.setGeometry(QtCore.QRect(1050, 70, 150, 100))
        self.user_menu.setStyleSheet("""
        #user_menu{
                background: #fff; 
                border: 1px solid #e5e7eb;
                border-radius: 5px;
                }
        QPushButton {
                        text-align: left;
                        background-color: transparent;
                        border: none;
                        color: #475569;
                        font-size: 12px;
                }
        QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
        """)
        self.user_menu.setVisible(False)

        #User login
        self.settings_btn = QtWidgets.QPushButton("User login", parent=self.user_menu)
        self.settings_btn.setGeometry(10, 10, 130, 30)
        self.settings_btn.setObjectName("settings_btn")

        #database login
        self.logout_btn = QtWidgets.QPushButton("Database login", parent=self.user_menu)
        self.logout_btn.setGeometry(10, 50, 130, 30)
        self.logout_btn.setObjectName("logout_btn")
        
        #Total Patient Card
        self.TotPat_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.TotPat_card.setGeometry(QtCore.QRect(20, 90, 190, 120))
        self.TotPat_card.setStyleSheet("""
        #TotPat_card {
                background: #fff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.TotPat_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.TotPat_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.TotPat_card.setObjectName("TotPat_card")

        # Total Patient
        self.label_2 = QtWidgets.QLabel(parent=self.TotPat_card)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: #fff; color: #64748B;")
        self.label_2.setObjectName("label_2")

        # Count Patient
        self.label_5 = QtWidgets.QLabel(parent=self.TotPat_card)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setWeight(75)
        self.label_5.setFont(font) 
        self.label_5.setStyleSheet("background: #fff;")
        self.label_5.setObjectName("label_5")

        #Total Appointments Card
        self.TodApp_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.TodApp_card.setGeometry(QtCore.QRect(255, 90, 190, 120))
        self.TodApp_card.setStyleSheet("""
        #TodApp_card {
                background: #fff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.TodApp_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.TodApp_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.TodApp_card.setObjectName("TodApp_card")

        #Today's Appointment
        self.label_3 = QtWidgets.QLabel(parent=self.TodApp_card)
        self.label_3.setGeometry(QtCore.QRect(10, 20, 165, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background: #fff; color: #64748B;")
        self.label_3.setObjectName("label_3")

        #Count Appointment where date now
        self.label_6 = QtWidgets.QLabel(parent=self.TodApp_card)
        self.label_6.setGeometry(QtCore.QRect(20, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background: #fff;")
        self.label_6.setObjectName("label_6")

        #Pending Payment Card
        self.PendPay_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.PendPay_card.setGeometry(QtCore.QRect(490, 90, 190, 120))
        self.PendPay_card.setStyleSheet("""
        #PendPay_card {
                background: #fff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.PendPay_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.PendPay_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.PendPay_card.setObjectName("PendPay_card")

        #Pending Payment
        self.label_4 = QtWidgets.QLabel(parent=self.PendPay_card)
        self.label_4.setGeometry(QtCore.QRect(10, 20, 175, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background: #fff; color: #64748B;")
        self.label_4.setObjectName("label_4")

        #Count Payment
        self.label_7 = QtWidgets.QLabel(parent=self.PendPay_card)
        self.label_7.setGeometry(QtCore.QRect(20, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background: #fff;")
        self.label_7.setObjectName("label_7")

        #Completed Treatment Card
        self.ComTreat_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.ComTreat_card.setGeometry(QtCore.QRect(725, 90, 190, 120))
        self.ComTreat_card.setStyleSheet("""
        #ComTreat_card {
                background: #fff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.ComTreat_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ComTreat_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ComTreat_card.setObjectName("ComTreat_card")
        
        #Completed Treatment
        self.label_8 = QtWidgets.QLabel(parent=self.ComTreat_card)
        self.label_8.setGeometry(QtCore.QRect(10, 20, 175, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(11)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background: #fff; color: #64748B;")
        self.label_8.setObjectName("label_8")

        #Count Treatment
        self.label_9 = QtWidgets.QLabel(parent=self.ComTreat_card)
        self.label_9.setGeometry(QtCore.QRect(20, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background: #fff;")
        self.label_9.setObjectName("label_9")

        #Todays Appintment Frame
        self.frame_2 = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.frame_2.setGeometry(QtCore.QRect(30, 230, 650, 461))
        self.frame_2.setStyleSheet("""
        #frame_2 {
                background: red;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.frame_2.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        
        self.frame_2.setObjectName("frame_2")
        self.label_10 = QtWidgets.QLabel(parent=self.frame_2)
        self.label_10.setGeometry(QtCore.QRect(20, 20, 231, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(14)
        font.setBold(True)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("background: #fff;")
        self.label_10.setObjectName("label_10")

        #Todays Appointment Table
        self.UpAp_table = QtWidgets.QTableWidget(parent=self.frame_2)
        self.UpAp_table.setGeometry(QtCore.QRect(40, 80, 500, 361))
        self.UpAp_table.setShowGrid(False)
        self.UpAp_table.setStyleSheet("""
        QTableWidget {
        background-color: #fff;
        border: none;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
        }
        QHeaderView::section {
                border: none;
                background-color: #fff;
        }
        """)
        self.UpAp_table.setObjectName("UpAp_table")
        self.UpAp_table.setColumnCount(5)
        self.UpAp_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.UpAp_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.UpAp_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.UpAp_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.UpAp_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.UpAp_table.setHorizontalHeaderItem(4, item)
        self.UpAp_table.verticalHeader().setVisible(False)

        self.UpAp_table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
                font-family: "Inter"; 
                font-size: 14px;        
                color: #64748B;       
                padding: 5px;         
        }
        """)

  
        # Recent Notifications Frame
        self.frame_3 = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.frame_3.setGeometry(QtCore.QRect(700, 230, 220, 461))
        self.frame_3.setStyleSheet("""
        #frame_3 {
                background: #ffffff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")
        self.label_11 = QtWidgets.QLabel(parent=self.frame_3)
        self.label_11.setGeometry(QtCore.QRect(20, 10, 190, 51))
        self.label_11.setStyleSheet("background-color: #fff;")
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(12)
        font.setBold(True)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.Pages.addWidget(self.Dashboard_page)

        #Patients Page
        self.Patients_page = QtWidgets.QWidget()
        self.Patients_page.setObjectName("Patients_page")
        
        #Patients top bar
        self.frame_4 = QtWidgets.QFrame(parent=self.Patients_page)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.frame_4.setStyleSheet("""
                #frame_4 { background-color: #fff; border-bottom: 1px solid #E5E7EB;
                        }
                         """)
        self.label_12 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_12.setGeometry(QtCore.QRect(20, 25, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: #fff;")
        self.label_12.setObjectName("label_12")

        #Notification button 2
        self.not_btn_2 = QtWidgets.QPushButton(parent=self.frame_4)
        self.not_btn_2.setGeometry(QtCore.QRect(725, 20, 40, 42))
        self.not_btn_2.setIcon(not_icon)
        self.not_btn_2.setIconSize(QtCore.QSize(25, 25))
        self.not_btn_2.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;                      
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.not_btn_2.setObjectName("not_btn_2")

        #User Button 2
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.frame_4)
        self.pushButton_3.setGeometry(QtCore.QRect(765, 20, 40, 42))
        self.pushButton_3.setText("")
        self.pushButton_3.setIcon(user_icon)
        self.pushButton_3.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_3.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;                         
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.pushButton_3.setObjectName("pushButton_3")

        #Search patient
        self.search_patient = QtWidgets.QLineEdit(parent=self.frame_4)
        self.search_patient.setGeometry(QtCore.QRect(490, 25, 211, 31))
        self.search_patient.setStyleSheet("background-color: #F1F5F9; border-radius: 8px;")
        self.search_patient.setReadOnly(False)
        self.search_patient.setObjectName("search_patient")

        #Add Patient Button
        self.add_icon = QtWidgets.QPushButton(parent=self.frame_4)
        self.add_icon.setGeometry(QtCore.QRect(810, 25, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.add_icon.setFont(font)
        self.add_icon.setStyleSheet("background-color: #3b82f6; border-radius: 8px; color: white;")
        add_icon = QtGui.QIcon(f"{filepath}Add.svg")
        self.add_icon.setIcon(add_icon)
        self.add_icon.setIconSize(QtCore.QSize(23, 23))
        self.add_icon.setObjectName("add_icon")

        #Patient Table Frame
        self.Pat_table_Frame = QtWidgets.QFrame(parent=self.Patients_page)
        self.Pat_table_Frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.Pat_table_Frame.setStyleSheet("""
        #Pat_table_Frame {
                background: #ffffff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.Pat_table_Frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Pat_table_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Pat_table_Frame.setObjectName("Pat_table_Frame")

        #Patients table
        self.Patients_table = QtWidgets.QTableWidget(parent=self.Pat_table_Frame)
        self.Patients_table.setGeometry(QtCore.QRect(10, 20, 700, 680))
        self.Patients_table.setObjectName("Patients_table")
        self.Patients_table.setColumnCount(7)
        self.Patients_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.Patients_table.setHorizontalHeaderItem(6, item)
        self.Pages.addWidget(self.Patients_page)
        self.Patients_table.setStyleSheet("""
        QTableWidget {
        background-color: #fff;
        border: none;
        border-radius: 12px;                                  
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
        }
        QHeaderView::section {
                border: none;
                background-color: #fff;
        }
        """)
        self.Patients_table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
                font-family: "Inter"; 
                font-size: 14px;        
                color: #64748B;                
        }
        """)
        
        #Appointments Page
        
        #Appointments top bar
        self.Appointments_page = QtWidgets.QWidget()
        self.Appointments_page.setObjectName("Appointments_page")
        self.app_frame = QtWidgets.QFrame(parent=self.Appointments_page)
        self.app_frame.setObjectName("app_frame")
        self.app_frame.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.app_frame.setStyleSheet("""
                #app_frame { background-color: #fff; border-bottom: 1px solid #E5E7EB;
                        }
                         """)
        self.label_13 = QtWidgets.QLabel(parent=self.app_frame)
        self.label_13.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: #fff;")
        self.label_13.setObjectName("label_13")

        #Notification button 3
        self.not_btn_3 = QtWidgets.QPushButton(parent=self.app_frame)
        self.not_btn_3.setGeometry(QtCore.QRect(685, 20, 40, 42))
        self.not_btn_3.setIcon(not_icon)
        self.not_btn_3.setIconSize(QtCore.QSize(25, 25))
        self.not_btn_3.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px; 
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.not_btn_3.setObjectName("not_btn_3")

        #User button 5
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.app_frame)
        self.pushButton_4.setGeometry(QtCore.QRect(725, 20, 40, 42))
        self.pushButton_4.setIcon(user_icon)
        self.pushButton_4.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_4.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px; 
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.pushButton_4.setObjectName("pushButton_4")

        #Search Appointment
        self.Search_app = QtWidgets.QLineEdit(parent=self.app_frame)
        self.Search_app.setGeometry(QtCore.QRect(450, 25, 211, 31))
        self.Search_app.setStyleSheet("background-color: #F1F5F9; border-radius: 8px;")
        self.Search_app.setReadOnly(False)
        self.Search_app.setObjectName("Search_app")
    

        #Add Appointment button
        self.AddApp_btn = QtWidgets.QPushButton(parent=self.app_frame)
        self.AddApp_btn.setGeometry(QtCore.QRect(770, 25, 151, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.AddApp_btn.setFont(font)
        self.AddApp_btn.setStyleSheet("background-color: #3b82f6; border-radius: 8px; color: white;")
        self.AddApp_btn.setIcon(add_icon)
        self.AddApp_btn.setIconSize(QtCore.QSize(23, 23))
        self.AddApp_btn.setObjectName("AddApp_btn")

        #Appointment Table Frame
        self.app_table_frame = QtWidgets.QFrame(parent=self.Appointments_page)
        self.app_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.app_table_frame.setStyleSheet("""
        #app_table_frame {
                background: #ffffff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.app_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.app_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.app_table_frame.setObjectName("app_table_frame")

        #Appointment table
        self.Appointments_table = QtWidgets.QTableWidget(parent=self.app_table_frame)
        self.Appointments_table.setGeometry(QtCore.QRect(150, 60, 500, 501))
        self.Appointments_table.setObjectName("Appointments_table")
        self.Appointments_table.setColumnCount(5)
        self.Appointments_table.setRowCount(0)
        self.Appointments_table.setStyleSheet("""
        QTableWidget {
        background-color: #fff;
        border: none;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
        }
        QHeaderView::section {
                border: none;
                background-color: #fff;
        }
        """)
        item = QtWidgets.QTableWidgetItem()
        self.Appointments_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Appointments_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Appointments_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Appointments_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Appointments_table.setHorizontalHeaderItem(4, item)
        self.Appointments_table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
                font-family: "Inter"; 
                font-size: 14px;        
                color: #64748B;               
        }
        """)

        #Appointments buttons layout
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.app_table_frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 461, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setStyleSheet("background-color: #fff;")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #Appointments All button
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout.addWidget(self.pushButton_8)

        #Appointments Scheduled button
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_9.setObjectName("pushButton_9")
        self.pushButton_9.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout.addWidget(self.pushButton_9)

        #Appointments Confirmed button
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout.addWidget(self.pushButton_7)
        
        #Appointments Waiting button
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget)
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout.addWidget(self.pushButton_6)
        self.Pages.addWidget(self.Appointments_page)


        #Billing Page

        #Billings top bar
        self.Billing_page = QtWidgets.QWidget()
        self.Billing_page.setObjectName("Billing_page")
        self.Bill_frame = QtWidgets.QFrame(parent=self.Billing_page)
        self.Bill_frame.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.Bill_frame.setStyleSheet("""
                #Bill_frame {background-color: #fff; border-bottom: 1px solid #E5E7EB;
                }
                """)
        self.Bill_frame.setObjectName("Bill_frame")

        #Billing
        self.label_14 = QtWidgets.QLabel(parent=self.Bill_frame)
        self.label_14.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: #fff;")
        self.label_14.setObjectName("label_14")

        #Notification button 4
        self.not_btn_4 = QtWidgets.QPushButton(parent=self.Bill_frame)
        self.not_btn_4.setGeometry(QtCore.QRect(725, 20, 40, 42))
        self.not_btn_4.setText("")
        self.not_btn_4.setIcon(not_icon)
        self.not_btn_4.setIconSize(QtCore.QSize(25, 25))
        self.not_btn_4.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px; 
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.not_btn_4.setObjectName("not_btn_4")

        #User button 4
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.Bill_frame)
        self.pushButton_10.setGeometry(QtCore.QRect(765, 20, 40, 42))
        self.pushButton_10.setText("")
        self.pushButton_10.setIcon(user_icon)
        self.pushButton_10.setIconSize(QtCore.QSize(25, 25))
        self.pushButton_10.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;                          
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.pushButton_10.setObjectName("pushButton_10")

        #Search bill
        self.Search_bill = QtWidgets.QLineEdit(parent=self.Bill_frame)
        self.Search_bill.setGeometry(QtCore.QRect(490, 25, 211, 31))
        self.Search_bill.setStyleSheet("background-color: #F1F5F9; border-radius: 8px;")
        self.Search_bill.setReadOnly(False)
        self.Search_bill.setObjectName("Search_bill")

        #Add bill button
        self.AddBill_btn = QtWidgets.QPushButton(parent=self.Bill_frame)
        self.AddBill_btn.setGeometry(QtCore.QRect(810, 25, 111, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(10)
        self.AddBill_btn.setFont(font)
        self.AddBill_btn.setStyleSheet("background-color: #3b82f6; border-radius: 8px; color: white;")
        self.AddBill_btn.setIcon(add_icon)
        self.AddBill_btn.setIconSize(QtCore.QSize(23, 23))
        self.AddBill_btn.setObjectName("AddBill_btn")

        #Billing Table frame
        self.bill_table_frame = QtWidgets.QFrame(parent=self.Billing_page)
        self.bill_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.bill_table_frame.setStyleSheet("""
        #bill_table_frame {
                background: #ffffff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.bill_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.bill_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bill_table_frame.setObjectName("bill_table_frame")

        #Billing Table
        self.Billing_table = QtWidgets.QTableWidget(parent=self.bill_table_frame)
        self.Billing_table.setGeometry(QtCore.QRect(150, 60, 500, 501))
        self.Billing_table.setObjectName("Billing_table")
        self.Billing_table.setColumnCount(6)
        self.Billing_table.setRowCount(0)
        self.Billing_table.setStyleSheet("""
        QTableWidget {
        background-color: #fff;
        border: none;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
        }
        QHeaderView::section {
                border: none;
                background-color: #fff;
        }
        """)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.Billing_table.setHorizontalHeaderItem(5, item)
        self.Billing_table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
                font-family: "Inter"; 
                font-size: 14px;        
                color: #64748B;       
                padding: 5px;         
        }
        """)

        #Billing buttons layout
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.bill_table_frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 461, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setStyleSheet("background-color: #fff;")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        #All Billing button
        self.pushButton_12 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_12.setObjectName("pushButton_12")
        self.pushButton_12.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout_2.addWidget(self.pushButton_12)

        #Pending Billing button
        self.pushButton_13 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_13.setObjectName("pushButton_13")
        self.pushButton_13.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout_2.addWidget(self.pushButton_13)
        

        #Paid Billing button
        self.pushButton_14 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_14.setObjectName("pushButton_14")
        self.pushButton_14.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.horizontalLayout_2.addWidget(self.pushButton_14)

        #Overdue Billing button
        self.pushButton_15 = QtWidgets.QPushButton(parent=self.horizontalLayoutWidget_2)
        self.pushButton_15.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: #fff;
                        border: none;
                        color: #475569;
                        font-size: 16px;
                        text-align: center;                
                }
                QPushButton:hover {
                        background-color: #f1f5f9;
                        color: #000000;
                        border-radius: 8px;
                }
                """)
        self.pushButton_15.setObjectName("pushButton_15")

        self.horizontalLayout_2.addWidget(self.pushButton_15)
        self.Pages.addWidget(self.Billing_page)

        #Reports Page

        #Reports Top bar frame
        self.Reports_page = QtWidgets.QWidget()
        self.Reports_page.setObjectName("Reports_page")
        self.Reports_topbar_frame = QtWidgets.QFrame(parent=self.Reports_page)
        self.Reports_topbar_frame.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.Reports_topbar_frame.setStyleSheet("""
                #Reports_topbar_frame {background-color: #fff; border-bottom: 1px solid #E5E7EB;
                }
                """)
        self.Reports_topbar_frame.setObjectName("Reports_topbar_frame")

        #Reports
        self.label_15 = QtWidgets.QLabel(parent=self.Reports_topbar_frame)
        self.label_15.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: #fff;")
        self.label_15.setObjectName("label_15")
        

        
        #Notification button 5
        self.not_btn_5 = QtWidgets.QPushButton(parent=self.Reports_topbar_frame)
        self.not_btn_5.setGeometry(QtCore.QRect(840, 23, 40, 40))
        not_icon = QtGui.QIcon(f"{filepath}Notification.svg")
        self.not_btn_5.setIcon(not_icon)
        self.not_btn_5.setIconSize(QtCore.QSize(25, 25))
        self.not_btn_5.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;                   
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }                           
        """)
        self.not_btn_5.setObjectName("not_btn_5")

        #User button 5
        self.userbtn_5 = QtWidgets.QPushButton(parent=self.Reports_topbar_frame)
        self.userbtn_5.setGeometry(QtCore.QRect(890, 23, 40, 40))
        user_icon = QtGui.QIcon(f"{filepath}User.svg")
        self.userbtn_5.setIcon(user_icon)
        self.userbtn_5.setIconSize(QtCore.QSize(25, 25))
        self.userbtn_5.setIconSize(QtCore.QSize(25, 25))
        self.userbtn_5.setStyleSheet("""
        QPushButton {
                border: none;
                background: transparent;
                border-radius: 20px;
        }
        QPushButton:hover {
                background-color: #72A8FF;
        }
        """)
        self.userbtn.setObjectName("userbtn_5")
        
        #Reports table frame
        self.Reports_table_frame = QtWidgets.QFrame(parent=self.Reports_page)
        self.Reports_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.Reports_table_frame.setStyleSheet("""
        #Reports_table_frame {
                background: #ffffff;
                border: 1px solid #e5e7eb;  
                border-radius: 12px;
        }
        """)
        self.Reports_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Reports_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Reports_table_frame.setObjectName("Reports_table_frame")
        self.Pages.addWidget(self.Reports_page)

        #User popup dialog
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1067, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.retranslateUi(MainWindow)
        self.Pages.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Dentica.setText(_translate("MainWindow", "Dentica"))
        
        #Dashboard Tab
        self.Dash_btn.setText(_translate("MainWindow", "Dashboard"))
        self.Patient_btn.setText(_translate("MainWindow", "Patients"))
        self.Apntmnt_btn.setText(_translate("MainWindow", "Appointments"))
        self.Bill_btn.setText(_translate("MainWindow", "Billing"))
        self.Rep_btn.setText(_translate("MainWindow", "Reports"))
        self.label.setText(_translate("MainWindow", "Dashboard"))
        self.label_2.setText(_translate("MainWindow", "Total Patient"))
        self.label_5.setText(_translate("MainWindow", "0"))
        self.label_3.setText(_translate("MainWindow", "Today's Appointments"))
        self.label_6.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Pending Payments"))
        self.label_7.setText(_translate("MainWindow", "0"))
        self.label_8.setText(_translate("MainWindow", "Completed Treatments"))
        self.label_9.setText(_translate("MainWindow", "0"))
        
        self.label_10.setText(_translate("MainWindow", "Todays Appointments"))
        item = self.UpAp_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Apppointment ID"))
        item = self.UpAp_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Patient Name"))
        item = self.UpAp_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Time"))
        item = self.UpAp_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Treatment"))
        item = self.UpAp_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Treatment Status"))
        
        self.label_11.setText(_translate("MainWindow", "Recent Notifications"))
        
        #Patients Tab
        self.label_12.setText(_translate("MainWindow", "Patients"))
        self.search_patient.setPlaceholderText(_translate("MainWindow", "Search patients..."))
        self.add_icon.setText(_translate("MainWindow", "Add Patient"))
        item = self.Patients_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Patient ID"))
        item = self.Patients_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Name"))
        item = self.Patients_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Gender"))
        item = self.Patients_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Birthdate"))
        item = self.Patients_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Contact"))
        item = self.Patients_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Email"))
        item = self.Patients_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Address"))

        #Appointments Tab
        self.label_13.setText(_translate("MainWindow", "Appointments"))
        self.Search_app.setPlaceholderText(_translate("MainWindow", "Search appointments..."))
        self.AddApp_btn.setText(_translate("MainWindow", "Add Appointments"))
        item = self.Appointments_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Patient"))
        item = self.Appointments_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date & Time"))
        item = self.Appointments_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Treatment"))
        item = self.Appointments_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        item = self.Appointments_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Action"))
        self.pushButton_8.setText(_translate("MainWindow", "All"))
        self.pushButton_9.setText(_translate("MainWindow", "Scheduled"))
        self.pushButton_7.setText(_translate("MainWindow", "Confirmed"))
        self.pushButton_6.setText(_translate("MainWindow", "Waiting"))
        self.label_14.setText(_translate("MainWindow", "Billing"))
        
        #Billings Tab
        self.Search_bill.setPlaceholderText(_translate("MainWindow", "Search invoices..."))
        self.AddBill_btn.setText(_translate("MainWindow", "New Invoice"))
        item = self.Billing_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Patient"))
        item = self.Billing_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date & Time"))
        item = self.Billing_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Treatment"))
        item = self.Billing_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Amount"))
        item = self.Billing_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Status"))
        item = self.Billing_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Action"))
        self.pushButton_12.setText(_translate("MainWindow", "All"))
        self.pushButton_13.setText(_translate("MainWindow", "Paid"))
        self.pushButton_14.setText(_translate("MainWindow", "Pending"))
        self.pushButton_15.setText(_translate("MainWindow", "Overdue"))
        
        #Reports Tab
        self.label_15.setText(_translate("MainWindow", "Reports"))
            
    def toggle_dropdown(self, userbtn, centralwidget, user_menu):
        if not userbtn.isVisible():
                btn_pos = userbtn.mapTo(centralwidget, QtCore.QPoint(0, userbtn.height()))
                userbtn.move(btn_pos)
        user_menu.setVisible(not user_menu.isVisible())
