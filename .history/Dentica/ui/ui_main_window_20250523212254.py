from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QCalendarWidget
from ui.Dialogues.ui_exit_dialog import Exit_App
from Frontend.Graphs.Appointment_status import DonutChart
from ui.Patients_Page import PatientPage
from ui.TablePagination import TablePagination
from PyQt6.QtGui import QTextCharFormat, QColor


filepath = "Dentica/ui/icons/"

class Ui_MainWindow(object):
   
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.setFixedSize(1200, 800)
        MainWindow.setWindowTitle("Dentica")
        MainWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self._drag_pos = None
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.dark_mode = False 
        
        #Sidebar Frame
        self.SidebarFrame = QtWidgets.QFrame(parent=self.centralwidget)
        self.SidebarFrame.setGeometry(QtCore.QRect(0, 0, 260, 800))
        self.SidebarFrame.setAutoFillBackground(False)
        self.SidebarFrame.setStyleSheet("background-color: #1F1F21 ; border-right: 1px solid #1F1F21 ;")
        self.SidebarFrame.setObjectName("SidebarFrame")
        
        #User card
        self.UserCard = QtWidgets.QFrame(parent=self.SidebarFrame)
        self.UserCard.setGeometry(QtCore.QRect(20, 600, 220, 150))
        self.UserCard.setStyleSheet("background-color: #B2CDE9 ; border-radius: 10px;")
        self.UserCard.setObjectName("UserCard")
        
        
        #Dentist Profile
        self.Dentica_profile = QtWidgets.QLabel(parent=self.SidebarFrame)
        self.Dentica_profile.setGeometry(QtCore.QRect(100, 580, 50, 50))
        self.Dentica_profile.setStyleSheet("border: none; background: transparent;")

        # Load and scale the image
        orig = QtGui.QPixmap(f"{filepath}Dentist_Profile.png").scaled(
        50, 50,
        QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
        QtCore.Qt.TransformationMode.SmoothTransformation
        )

        # Create circular mask
        mask = QtGui.QBitmap(50, 50)
        mask.fill(QtCore.Qt.GlobalColor.color0)
        p = QtGui.QPainter(mask)
        p.setBrush(QtCore.Qt.GlobalColor.color1)
        p.setPen(QtCore.Qt.PenStyle.NoPen)
        p.drawEllipse(0, 0, 50, 50)
        p.end()

        # Apply mask
        orig.setMask(mask)

        # Set pixmap
        self.Dentica_profile.setPixmap(orig)



        #Dentist Label
        self.Dentist = QtWidgets.QLabel(parent=self.UserCard)
        self.Dentist.setGeometry(QtCore.QRect(15, 50, 200, 20))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(13)
        font.setBold(True)
        self.Dentist.setFont(font)
        self.Dentist.setStyleSheet("""
                                      color: #37547A;
                                      border: none;
                                      """)
        self.Dentist.setText("Dr. Bobeth Maghuyop")
        self.Dentist.setObjectName("Dentica")
        
        #Dentist Title Label
        self.Dentist_title = QtWidgets.QLabel(parent=self.UserCard)
        self.Dentist_title.setGeometry(QtCore.QRect(20, 70, 180, 20))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(8)
        font.setBold(True)
        self.Dentist_title.setFont(font)
        self.Dentist_title.setStyleSheet("""
                                      color: #FFF;
                                      border: none;
                                      """)
        self.Dentist_title.setText("Doctor of Dental Surgery (DDS)")
        self.Dentist_title.setObjectName("Dentica")
        
        #Theme button
        self.theme_btn = QtWidgets.QPushButton(parent=self.UserCard)
        self.theme_btn.setGeometry(QtCore.QRect(35, 100, 40, 40))
        self.theme_btn.setIconSize(QtCore.QSize(25, 25))
        self.theme_btn.setObjectName("theme_btn")
        dark_icon = QtGui.QIcon(f"{filepath}Dark.svg")
        self.theme_btn.setIcon(dark_icon)
        self.theme_btn.setStyleSheet("""
        QPushButton {
                border: none;
                background-color: #37547A;
                border-radius: 20px;
        }
        QPushButton:hover {
                background-color: #C6D7EC;
        }
        """)
        self.theme_btn.clicked.connect(self.toggle_theme) 
         
        #User button
        self.userbtn = QtWidgets.QPushButton(parent=self.UserCard)
        self.userbtn.setGeometry(QtCore.QRect(85, 100, 40, 40)) 
        user_icon = QtGui.QIcon(f"{filepath}User.svg")
        self.userbtn.setIcon(user_icon)
        self.userbtn.setIconSize(QtCore.QSize(25, 25))
        self.userbtn.setStyleSheet("""
        QPushButton {
                border: none;
                background-color: #37547A;
                border-radius: 20px;
        }
        QPushButton:hover {
                background-color: #C6D7EC;
        }
        """)
        
        #Exit button
        self.exitbtn = QtWidgets.QPushButton(parent=self.UserCard)
        self.exitbtn.setGeometry(QtCore.QRect(135, 100, 40, 40)) 
        exit_icon = QtGui.QIcon(f"{filepath}Exit.svg")
        self.exitbtn.setIcon(exit_icon)
        self.exitbtn.setIconSize(QtCore.QSize(25, 25))
        self.exitbtn.setIconSize(QtCore.QSize(25, 25))
        self.exitbtn.setStyleSheet("""
        QPushButton {
                border: none;
                background-color: #37547A;
                border-radius: 20px;
        }
        QPushButton:hover {
                background-color: #C6D7EC;
        }
        """)
        
        #Dentica Label
        self.Dentica = QtWidgets.QLabel(parent=self.SidebarFrame)
        self.Dentica.setGeometry(QtCore.QRect(65, 25, 121, 51))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(20)
        font.setBold(True)
        self.Dentica.setFont(font)
        self.Dentica.setStyleSheet("""border: none;
                                      color: #fff;
                                      """)
        self.Dentica.setObjectName("Dentica")

        #Dentica Icon
        self.DenticaIcon = QtWidgets.QLabel(parent = self.SidebarFrame)
        self.DenticaIcon.setGeometry(QtCore.QRect(30, 33, 35, 35))
        dent_icon = QtGui.QIcon(f"{filepath}Dentica.svg")
        pixmap = dent_icon.pixmap(35,35)
        self.DenticaIcon.setPixmap(pixmap)

        #Sidebar Layout
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.SidebarFrame)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 80, 260, 490))
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
        self.Dash_btn.clicked.connect(lambda: (self.Pages.setCurrentIndex(0), self.set_active_button(self.Dash_btn)))
        self.Dash_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #fff;
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }
                QPushButton:checked {
                        background-color: #8DB8E0;
                        color: #fff;
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
        self.Patient_btn.clicked.connect(lambda: (self.Pages.setCurrentIndex(1), self.set_active_button(self.Patient_btn)))
        self.Patient_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #fff;
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }
                QPushButton:checked {
                        background-color: #8DB8E0;
                        color: #fff;
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
        self.Apntmnt_btn.clicked.connect(lambda: (self.Pages.setCurrentIndex(2), self.set_active_button(self.Apntmnt_btn)))
        self.Apntmnt_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #fff;
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }
                QPushButton:checked {
                        background-color: #8DB8E0;
                        color: #fff;
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
        self.Bill_btn.clicked.connect(lambda: (self.Pages.setCurrentIndex(3), self.set_active_button(self.Bill_btn)))
        self.Bill_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #fff;
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }
                QPushButton:checked {
                        background-color: #8DB8E0;
                        color: #fff;
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
        self.Rep_btn.clicked.connect(lambda: (self.Pages.setCurrentIndex(4), self.set_active_button(self.Rep_btn)))
        self.Rep_btn.setStyleSheet("""
                QPushButton {
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: #fff;
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }
                QPushButton:checked {
                        background-color: #8DB8E0;
                        color: #fff;
                        border-radius: 8px;
                }                    
                """)
        self.verticalLayout.addWidget(self.Rep_btn)
        
        #Test patient page button
        # self.testbutton = QtWidgets.QPushButton("View Patient Test Btn")
        # self.testbutton.setStyleSheet("color: #fff; border: 1px solid #fff;")
        # self.verticalLayout.addWidget(self.testbutton)
        # self.testbutton.clicked.connect(lambda: self.Pages.setCurrentIndex(5))
        self.verticalLayout.addStretch()
        #self.testbutton.setObjectName("testbutton")
        
        #Test appointment dialogue button
        self.testbutton2 = QtWidgets.QPushButton("View Appointment Test Btn")
        self.testbutton2.setStyleSheet("color: #fff; border: 1px solid #fff;")
        self.verticalLayout.addWidget(self.testbutton2)
        self.verticalLayout.addStretch()
        self.testbutton2.setObjectName("testbutton2")
        
        
        for btn in [self.Dash_btn, self.Patient_btn, self.Apntmnt_btn, self.Bill_btn, self.Rep_btn]:
                btn.setCheckable(True)

        self.button_group = QtWidgets.QButtonGroup()
        self.button_group.setExclusive(True)
        self.button_group.addButton(self.Dash_btn)
        self.button_group.addButton(self.Patient_btn)
        self.button_group.addButton(self.Apntmnt_btn)
        self.button_group.addButton(self.Bill_btn)
        self.button_group.addButton(self.Rep_btn)

        #Pages
        self.Pages = QtWidgets.QStackedWidget(parent=self.centralwidget)
        self.Pages.setGeometry(QtCore.QRect(260, 0, 1200, 800))
        self.Pages.setStyleSheet("""background: #B2CDE9;
                                    color: black;
                                    """)
        self.Pages.setObjectName("Pages")
        self.Dashboard_page = QtWidgets.QWidget()
        self.Dashboard_page.setObjectName("Dashboard_page")
        
       
        #Dashboard graph
        self.dash_graph = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.dash_graph.setGeometry(QtCore.QRect(30, 30, 420, 290))
        self.dash_graph.setStyleSheet("""
        #dash_graph {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.dash_graph.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.dash_graph.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.dash_graph.setObjectName("dash_graph")
        
        self.graph_label = QtWidgets.QLabel(parent=self.dash_graph)
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(12)
        font.setBold(True)
        self.graph_label.setFont(font)
        self.graph_label.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.graph_label.setText("Appointments Status")
        
        layout = QVBoxLayout()
        self.dash_graph.setLayout(layout)
        labels = ['Scheduled', 'Completed', 'Cancelled']
        chart_values = [15, 50, 10]
        donut_chart = DonutChart(labels, chart_values)
        layout.addWidget(self.graph_label)
        layout.addWidget(donut_chart)
        
        
        #Total Patient Card
        self.TotPat_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.TotPat_card.setGeometry(QtCore.QRect(490, 30, 200, 130))
        self.TotPat_card.setStyleSheet("""
        #TotPat_card {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.TotPat_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.TotPat_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.TotPat_card.setObjectName("TotPat_card")

        #Patient icon
        self.totpat_icon = QtWidgets.QLabel(parent=self.TotPat_card)
        self.totpat_icon.setGeometry(QtCore.QRect(20, 15, 30, 30))
        self.totpat_icon.setStyleSheet("background: transparent;")
        pat_icon2 = QtGui.QIcon(f"{filepath}Patients2.svg")
        pixmap = pat_icon2.pixmap(25,25)
        self.totpat_icon.setPixmap(pixmap)

        #Total Patient
        self.label_2 = QtWidgets.QLabel(parent=self.TotPat_card)
        self.label_2.setGeometry(QtCore.QRect(50, 20, 121, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(9)
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_2.setObjectName("label_2")

        #Count Patient
        self.label_5 = QtWidgets.QLabel(parent=self.TotPat_card)
        self.label_5.setGeometry(QtCore.QRect(20, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        self.label_5.setFont(font) 
        self.label_5.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_5.setObjectName("label_5")

        #Total Appointments Card
        self.TodApp_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.TodApp_card.setGeometry(QtCore.QRect(725, 30, 200, 130))
        self.TodApp_card.setStyleSheet("""
        #TodApp_card {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.TodApp_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.TodApp_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.TodApp_card.setObjectName("TodApp_card")

        #appointment icon
        self.totapp_icon = QtWidgets.QLabel(parent=self.TodApp_card)
        self.totapp_icon.setGeometry(QtCore.QRect(10, 15, 30, 30))
        self.totapp_icon.setStyleSheet("background: transparent;")
        app_icon2 = QtGui.QIcon(f"{filepath}Appointments2.svg")
        pixmap2 = app_icon2.pixmap(23,23)
        self.totapp_icon.setPixmap(pixmap2)

        #Today's Appointment
        self.label_3 = QtWidgets.QLabel(parent=self.TodApp_card)
        self.label_3.setGeometry(QtCore.QRect(35, 20, 155, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(9)
        font.setBold(True)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_3.setObjectName("label_3")

        #Count Appointment where date now
        self.label_6 = QtWidgets.QLabel(parent=self.TodApp_card)
        self.label_6.setGeometry(QtCore.QRect(10, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_6.setObjectName("label_6")

        #Pending Payment Card
        self.PendPay_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.PendPay_card.setGeometry(QtCore.QRect(490, 190, 200, 130))
        self.PendPay_card.setStyleSheet("""
        #PendPay_card {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }                            
        """)
        self.PendPay_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.PendPay_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.PendPay_card.setObjectName("PendPay_card")

        #payment icon
        self.pay_icon = QtWidgets.QLabel(parent=self.PendPay_card)
        self.pay_icon.setGeometry(QtCore.QRect(10, 15, 30, 30))
        self.pay_icon.setStyleSheet("background: transparent;")
        bil_icon2 = QtGui.QIcon(f"{filepath}Billing2.svg")
        pixmap3 = bil_icon2.pixmap(25, 25)
        self.pay_icon.setPixmap(pixmap3)

        #Pending Payment
        self.label_4 = QtWidgets.QLabel(parent=self.PendPay_card)
        self.label_4.setGeometry(QtCore.QRect(40, 20, 155, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(9)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_4.setObjectName("label_4")

        #Count Payment
        self.label_7 = QtWidgets.QLabel(parent=self.PendPay_card)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_7.setObjectName("label_7")

        #Completed Treatment Card
        self.ComTreat_card = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.ComTreat_card.setGeometry(QtCore.QRect(725, 190, 200, 130))
        self.ComTreat_card.setStyleSheet("""
        #ComTreat_card {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
         }
        """)
        self.ComTreat_card.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.ComTreat_card.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.ComTreat_card.setObjectName("ComTreat_card")

        #Treatment icon
        self.treat_icon = QtWidgets.QLabel(parent=self.ComTreat_card)
        self.treat_icon.setGeometry(QtCore.QRect(10, 15, 30, 30))
        self.treat_icon.setStyleSheet("background: transparent;")
        treat_icon = QtGui.QIcon(f"{filepath}Treatment.svg")
        pixmap4 = treat_icon.pixmap(25, 25)
        self.treat_icon.setPixmap(pixmap4)
        
        #Completed Treatment
        self.label_8 = QtWidgets.QLabel(parent=self.ComTreat_card)
        self.label_8.setGeometry(QtCore.QRect(35, 20, 155, 21))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(9)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_8.setObjectName("label_8")

        #Count Treatment
        self.label_9 = QtWidgets.QLabel(parent=self.ComTreat_card)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 51, 31))
        font = QtGui.QFont()
        font.setFamily("Inter")
        font.setPointSize(16)
        font.setBold(True)
        self.label_9.setFont(font)
        self.label_9.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_9.setObjectName("label_9")

        #Todays Appointment Frame
        self.frame_2 = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.frame_2.setGeometry(QtCore.QRect(30, 350, 580, 440))
        # frame_2 bg = #C6D7EC
        self.frame_2.setStyleSheet("""
        #frame_2 {
                background: red;
                border: 1px solid #fff;
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
        self.label_10.setStyleSheet("background: #C6D7EC; color: #37547A;")
        self.label_10.setObjectName("label_10")

        #Todays Appointment Table
        self.UpAp_table = QtWidgets.QTableWidget(parent=self.frame_2)
        self.UpAp_table.setGeometry(QtCore.QRect(40, 80, 500, 340))
        self.UpAp_table.setShowGrid(False)
        self.UpAp_table.setStyleSheet("""
        QTableWidget {
        background-color: #C6D7EC;
        border: none;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
        }
        QHeaderView::section {
                border: none;
                background-color: #C6D7EC;
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

  
        self.UpAp_table.setColumnWidth(0, 120)  # Pat. Name
        self.UpAp_table.setColumnWidth(1, 70)  # Time
        self.UpAp_table.setColumnWidth(2, 150)  # Treatment Proc
        self.UpAp_table.setColumnWidth(3, 60)  # Status
        self.UpAp_table.setColumnWidth(4, 100)  # Actions
        
        self.UpAp_table.verticalHeader().setDefaultSectionSize(60)
        
        self.UpAp_pagination = TablePagination(self.UpAp_table, rows_per_page=10)
        self.UpAp_pagination.setup_pagination_controls(self.frame_2, y_offset=-20)
  
        # Calendar Frame
        self.frame_3 = QtWidgets.QFrame(parent=self.Dashboard_page)
        self.frame_3.setGeometry(QtCore.QRect(620, 350, 310, 440))
        self.frame_3.setStyleSheet("""
        #frame_3 {
        background: #1F1F21;
        border: 1px solid #5e93bf;
        border-radius: 12px;
        }
        """)
        self.frame_3.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame_3.setObjectName("frame_3")

        layout = QtWidgets.QVBoxLayout(self.frame_3)
        layout.setContentsMargins(12, 12, 12, 12)

        self.calendar = QCalendarWidget(parent=self.frame_3)
        self.calendar.setSelectionMode(QtWidgets.QCalendarWidget.SelectionMode.NoSelection)
        self.calendar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        prev_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
        next_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
        left = QtGui.QIcon(f"{filepath}Left.svg")
        right = QtGui.QIcon(f"{filepath}Right.svg")
        prev_btn.setIcon(left)
        next_btn.setIcon(right)
        prev_btn.setIconSize(QtCore.QSize(20, 20))
        next_btn.setIconSize(QtCore.QSize(20, 20))
        
        weekend_format = QTextCharFormat()
        weekend_format.setForeground(QColor("#7c94a3"))
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
        self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)
        self.calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.calendar.setStyleSheet("""
        QCalendarWidget {
        background: transparent;
        border: none;
        }

        QCalendarWidget QWidget#qt_calendar_navigationbar {
        background: transparent;
        border: none;
        }

        QCalendarWidget QWidget#qt_calendar_calendarview {
        background: transparent;
        border-radius: 12px;
        }

        QCalendarWidget QAbstractItemView {
        background: transparent;
        selection-background-color: #5e93bf;
        color: white;
        gridline-color: #5e93bf;
        border-radius: 12px;
        }
        
        QCalendarWidget QAbstractItemView::item {
        outline: none;            
        border: none;             
        }

        QCalendarWidget QToolButton {
        background: transparent;
        color: white;
        font-weight: bold;
        border: none;
        padding: 5px;
        border-top-left-radius: 12px;
        border-top-right-radius: 12px;
        }
        QCalendarWidget QAbstractItemView:item:selected:!active,
        QCalendarWidget QAbstractItemView:item:selected:active {
        background-color: #5e93bf;
        border-radius: 15px;
        color: white;
        }

        QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover {
        color: white;  
        }

        QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(6) {
        color: #7c94a3;  
        }

        QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(7) {
        color: #7c94a3;  
        }
        """)

        font = QtGui.QFont("Inter", 9)
        self.calendar.setFont(font)
        self.calendar.setFixedHeight(300)
        self.calendar.setFixedWidth(300) 
        

        self.scheduled_label = QtWidgets.QLabel("Scheduled:                                                                 0")
        self.completed_label = QtWidgets.QLabel("Completed:                                                                0")
        self.cancelled_label = QtWidgets.QLabel("Cancelled:                                                                  0")

        self.scheduled_label.setStyleSheet("color: #8DB8E0; background-color: None; font-size: 14px; font-family: Inter;")   
        self.completed_label.setStyleSheet("color: #8DB8E0; background-color: None; font-size: 14px; font-family: Inter;")
        self.cancelled_label.setStyleSheet("color: #8DB8E0; background-color: None; font-size: 14px; font-family: Inter;")

        layout.addWidget(self.calendar)
        layout.addWidget(self.scheduled_label)
        layout.addWidget(self.completed_label)
        layout.addWidget(self.cancelled_label)

        self.Pages.addWidget(self.Dashboard_page)

        #Patients Page
        self.Patients_page = QtWidgets.QWidget()
        self.Patients_page.setObjectName("Patients_page")
        
        #Patients top bar
        self.frame_4 = QtWidgets.QFrame(parent=self.Patients_page)
        self.frame_4.setObjectName("frame_4")
        self.frame_4.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.frame_4.setStyleSheet("""
                #frame_4 { background-color: #B2CDE9;
                        }
                         """)
        #Patients page title
        self.label_12 = QtWidgets.QLabel(parent=self.frame_4)
        self.label_12.setGeometry(QtCore.QRect(20, 25, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(18)
        font.setBold(True)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("background-color: #B2CDE9; color: #0E283F;")
        self.label_12.setObjectName("label_12")


        #Search patient
        self.search_patient = QtWidgets.QLineEdit(parent=self.frame_4)
        self.search_patient.setGeometry(QtCore.QRect(580, 25, 211, 31))
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
        self.add_icon.setStyleSheet("background-color: #0E283F; border-radius: 8px; color: white;")
        add_icon = QtGui.QIcon(f"{filepath}Add.svg")
        self.add_icon.setIcon(add_icon)
        self.add_icon.setIconSize(QtCore.QSize(23, 23))
        self.add_icon.setObjectName("add_icon")

        #Patient Table Frame
        self.Pat_table_Frame = QtWidgets.QFrame(parent=self.Patients_page)
        self.Pat_table_Frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.Pat_table_Frame.setStyleSheet("""
        #Pat_table_Frame {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
                
        }
        """)
        self.Pat_table_Frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Pat_table_Frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Pat_table_Frame.setObjectName("Pat_table_Frame")

        #Patients table
        self.Patients_table = QtWidgets.QTableWidget(parent=self.Pat_table_Frame)
        self.Patients_table.setGeometry(QtCore.QRect(10, 20, 880, 655))
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
                background-color: #C6D7EC;
                border: none;
                color: #64748B;
                gridline-color: transparent;
        }
        QTableWidget::item {
                border-bottom: 1px solid #8DB8E0;
                text-align: center;
        }
        QHeaderView::section {
                border: none;
                color: #64748B;
                background: #C6D7EC;
        }
        """)
        self.Patients_table.horizontalHeader().setStyleSheet("""
        QHeaderView::section {
                font-family: "Inter"; 
                font-size: 14px;        
                color: #64748B;
                background: #C6D7EC;                
        }
        """)
        
        #Sizing
        self.Patients_table.setColumnWidth(0, 162)  # Name
        self.Patients_table.setColumnWidth(1, 67)  # Gender
        self.Patients_table.setColumnWidth(2, 70)  # Birthdate
        self.Patients_table.setColumnWidth(3, 115)  # Contact
        self.Patients_table.setColumnWidth(4, 120)  # Email
        self.Patients_table.setColumnWidth(5, 145)  # Address
        self.Patients_table.setColumnWidth(6, 160)  # Actions

        #Row height for each patient
        self.Patients_table.verticalHeader().setDefaultSectionSize(60)

        self.patients_pagination = TablePagination(self.Patients_table, rows_per_page=10)
        self.patients_pagination.setup_pagination_controls(self.Patients_page, y_offset=85)
        
        #Appointments Page
        
        #Appointments top bar
        self.Appointments_page = QtWidgets.QWidget()
        self.Appointments_page.setObjectName("Appointments_page")
        self.app_frame = QtWidgets.QFrame(parent=self.Appointments_page)
        self.app_frame.setObjectName("app_frame")
        self.app_frame.setGeometry(QtCore.QRect(0, 0, 940, 71))
        self.app_frame.setStyleSheet("""
                #app_frame { background-color: #B2CDE9;
                        }
                         """)
        self.label_13 = QtWidgets.QLabel(parent=self.app_frame)
        self.label_13.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(18)
        font.setBold(True)
        self.label_13.setFont(font)
        self.label_13.setStyleSheet("background-color: #B2CDE9; color: #0E283F;")
        self.label_13.setObjectName("label_13")


        #Search Appointment
        self.Search_app = QtWidgets.QLineEdit(parent=self.app_frame)
        self.Search_app.setGeometry(QtCore.QRect(540, 25, 211, 31))
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
        self.AddApp_btn.setStyleSheet("background-color: #0E283F; border-radius: 8px; color: white;")
        self.AddApp_btn.setIcon(add_icon)
        self.AddApp_btn.setIconSize(QtCore.QSize(23, 23))
        self.AddApp_btn.setObjectName("AddApp_btn")

        #Appointment Table Frame
        self.app_table_frame = QtWidgets.QFrame(parent=self.Appointments_page)
        self.app_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.app_table_frame.setStyleSheet("""
        #app_table_frame {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.app_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.app_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.app_table_frame.setObjectName("app_table_frame")

        #Appointment Table
        self.Appointments_table = QtWidgets.QTableWidget(parent=self.app_table_frame)
        self.Appointments_table.setGeometry(QtCore.QRect(40, 60, 820, 615))
        self.Appointments_table.setObjectName("Appointments_table")
        self.Appointments_table.setColumnCount(5)
        self.Appointments_table.setRowCount(0)
        self.Appointments_table.setStyleSheet("""
        QTableWidget {
                background-color: #C6D7EC;
                border: none;
                gridline-color: transparent;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
                color: #64748B;
        }
        QHeaderView::section {
                border: none;
                background-color: #C6D7EC;
                color: #64748B;
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
                background-color: #C6D7EC;            
        }
        """)
        
        #Appointment table sizing
        self.Appointments_table.setColumnWidth(0, 200)  # Pat. Name
        self.Appointments_table.setColumnWidth(1, 150)  # Date
        self.Appointments_table.setColumnWidth(2, 150)  # Status
        self.Appointments_table.setColumnWidth(3, 117)  # Treatment
        self.Appointments_table.setColumnWidth(4, 160)  # Actions
        
        self.Appointments_table.verticalHeader().setDefaultSectionSize(60)

        self.appointments_pagination = TablePagination(self.Appointments_table, rows_per_page=10)
        self.appointments_pagination.setup_pagination_controls(self.Appointments_page, y_offset=85)
        
        #Appointments buttons layout
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.app_table_frame)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 10, 461, 41))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setStyleSheet("background-color: #C6D7EC;")
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                #Bill_frame {background-color: #B2CDE9;
                }
                """)
        self.Bill_frame.setObjectName("Bill_frame")

        #Billing
        self.label_14 = QtWidgets.QLabel(parent=self.Bill_frame)
        self.label_14.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(18)
        font.setBold(True)
        self.label_14.setFont(font)
        self.label_14.setStyleSheet("background-color: #B2CDE9; color: #0E283F;")
        self.label_14.setObjectName("label_14")

        #Search bill
        self.Search_bill = QtWidgets.QLineEdit(parent=self.Bill_frame)
        self.Search_bill.setGeometry(QtCore.QRect(580, 25, 211, 31))
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
        self.AddBill_btn.setStyleSheet("background-color: #0E283F; border-radius: 8px; color: white;")
        self.AddBill_btn.setIcon(add_icon)
        self.AddBill_btn.setIconSize(QtCore.QSize(23, 23))
        self.AddBill_btn.setObjectName("AddBill_btn")

        #Billing Table Frame
        self.bill_table_frame = QtWidgets.QFrame(parent=self.Billing_page)
        self.bill_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.bill_table_frame.setStyleSheet("""
        #bill_table_frame {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.bill_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.bill_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.bill_table_frame.setObjectName("bill_table_frame")

        #Billing Table
        self.Billing_table = QtWidgets.QTableWidget(parent=self.bill_table_frame)
        self.Billing_table.setGeometry(QtCore.QRect(40, 60, 840, 615))
        self.Billing_table.setObjectName("Billing_table")
        self.Billing_table.setColumnCount(6)
        self.Billing_table.setRowCount(0)
        self.Billing_table.setStyleSheet("""
        QTableWidget {
                background-color: #C6D7EC;
                border: none;
                gridline-color: transparent;
        }
        QTableWidget::item {
                border-bottom: 1px solid #e5e7eb;
                color: #64748B;
        }
        QHeaderView::section {
                border: none;
                background-color: #C6D7EC;
                color: #64748B;
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
        }
        """)
 
        # Bill Sizing
        self.Billing_table.setColumnWidth(0, 90)  # Bill ID 
        self.Billing_table.setColumnWidth(1, 206)  # Pat. Name
        self.Billing_table.setColumnWidth(2, 120)  # App. ID
        self.Billing_table.setColumnWidth(3, 150)  # Total Amount
        self.Billing_table.setColumnWidth(4, 130)  # Method
        self.Billing_table.setColumnWidth(5, 110)  # Status

        
        self.Billing_table.verticalHeader().setDefaultSectionSize(60)

        self.Billing_pagination = TablePagination(self.Billing_table, rows_per_page=10)
        self.Billing_pagination.setup_pagination_controls(self.Billing_page, y_offset=85)
        
        #Billing buttons layout
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(parent=self.bill_table_frame)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(20, 10, 461, 41))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setStyleSheet("background-color: #C6D7EC;")
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                        background-color: #C6D7EC;
                        border: none;
                        color: #37547A;
                        font-size: 16px;
                        text-align: center;
                        font-family: Inter;                
                }
                QPushButton:hover {
                        background-color: #8DB8E0;
                        color: #37547A;
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
                #Reports_topbar_frame {background-color: #B2CDE9;
                }
                """)
        self.Reports_topbar_frame.setObjectName("Reports_topbar_frame")

        #Reports
        self.label_15 = QtWidgets.QLabel(parent=self.Reports_topbar_frame)
        self.label_15.setGeometry(QtCore.QRect(20, 25, 180, 31))
        font = QtGui.QFont()
        font.setFamily("Katarine")
        font.setPointSize(18)
        font.setBold(True)
        self.label_15.setFont(font)
        self.label_15.setStyleSheet("background-color: #B2CDE9; color: #0E283F;")
        self.label_15.setObjectName("label_15")

        
        #Reports table frame
        self.Reports_table_frame = QtWidgets.QFrame(parent=self.Reports_page)
        self.Reports_table_frame.setGeometry(QtCore.QRect(20, 80, 900, 680))
        self.Reports_table_frame.setStyleSheet("""
        #Reports_table_frame {
                background: #C6D7EC;
                border: 1px solid #fff;  
                border-radius: 12px;
        }
        """)
        self.Reports_table_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.Reports_table_frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.Reports_table_frame.setObjectName("Reports_table_frame")
        self.Pages.addWidget(self.Reports_page)
        
        # #Add patient page into pages
        # self.patient_page = PatientPage()
        # self.Pages.addWidget(self.patient_page)

        #User popup dialog
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1067, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        self.Pages.setCurrentIndex(0)
        self.set_active_button(self.Dash_btn) 
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
        self.label_2.setText(_translate("MainWindow", "Total Patients"))
        self.label_5.setText(_translate("MainWindow", "0"))
        self.label_3.setText(_translate("MainWindow", "Today's Appointments"))
        self.label_6.setText(_translate("MainWindow", "0"))
        self.label_4.setText(_translate("MainWindow", "Pending Payments"))
        self.label_7.setText(_translate("MainWindow", "0"))
        self.label_8.setText(_translate("MainWindow", "Completed Treatments"))
        self.label_9.setText(_translate("MainWindow", "0"))
        
        self.label_10.setText(_translate("MainWindow", "Todays Appointments"))
        item = self.UpAp_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Patient Name"))
        item = self.UpAp_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Time"))
        item = self.UpAp_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Treatment Procedure"))
        item = self.UpAp_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Status"))
        item = self.UpAp_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Actions"))
        #TODO fix the todays appointments table size

        #Patients Tab
        self.label_12.setText(_translate("MainWindow", "Patients"))
        self.search_patient.setPlaceholderText(_translate("MainWindow", "Search patients..."))
        self.add_icon.setText(_translate("MainWindow", "Add Patient"))
        item = self.Patients_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.Patients_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Gender"))
        item = self.Patients_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Birthdate"))
        item = self.Patients_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Contact"))
        item = self.Patients_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Email"))
        item = self.Patients_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Address"))
        item = self.Patients_table.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Actions"))

        #Appointments Tab
        self.label_13.setText(_translate("MainWindow", "Appointments"))
        self.Search_app.setPlaceholderText(_translate("MainWindow", "Search appointments..."))
        self.AddApp_btn.setText(_translate("MainWindow", "Add Appointments"))
        item = self.Appointments_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Patient Name"))
        item = self.Appointments_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Date"))
        item = self.Appointments_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Status"))
        item = self.Appointments_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Treatment/s"))
        item = self.Appointments_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Actions"))
        self.pushButton_8.setText(_translate("MainWindow", "All"))
        self.pushButton_9.setText(_translate("MainWindow", "Scheduled"))
        self.pushButton_7.setText(_translate("MainWindow", "Completed"))
        self.pushButton_6.setText(_translate("MainWindow", "Canceled"))

        
        #Billings Tab
        self.label_14.setText(_translate("MainWindow", "Billing"))
        self.Search_bill.setPlaceholderText(_translate("MainWindow", "Search invoices..."))
        self.AddBill_btn.setText(_translate("MainWindow", "New Invoice"))
        item = self.Billing_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Billing ID"))
        item = self.Billing_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Patient Name"))
        item = self.Billing_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Appointment ID"))
        item = self.Billing_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Total Amount"))
        item = self.Billing_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Method"))
        item = self.Billing_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Status"))
        self.pushButton_12.setText(_translate("MainWindow", "All"))
        self.pushButton_13.setText(_translate("MainWindow", "Paid"))
        self.pushButton_14.setText(_translate("MainWindow", "Pending"))
        self.pushButton_15.setText(_translate("MainWindow", "Overdue"))
        
        #Reports Tab
        self.label_15.setText(_translate("MainWindow", "Reports"))

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_pos:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            event.accept()

    def mouseReleaseEvent(MainWindow, event):
        MainWindow.oldPos = None
            
    def toggle_dropdown(self, userbtn, centralwidget, user_menu):
        if not userbtn.isVisible():
                btn_pos = userbtn.mapTo(centralwidget, QtCore.QPoint(0, userbtn.height()))
                userbtn.move(btn_pos)
        user_menu.setVisible(not user_menu.isVisible())

    def set_active_button(self, button):
        for btn in [self.Dash_btn, self.Patient_btn, self.Apntmnt_btn, self.Bill_btn, self.Rep_btn]:
                btn.setChecked(btn == button)
    
    def toggle_theme(self):
        # Switch themes
        self.dark_mode = not self.dark_mode
        dark_icon = QtGui.QIcon(f"{filepath}Dark.svg")
        light_icon = QtGui.QIcon(f"{filepath}Light.svg")
        self.apply_theme(light_icon, dark_icon)
        
        
    def apply_theme(self, light_icon, dark_icon):
        if self.dark_mode:
                # Dark theme colors
                sidebar_bg = "#1F1F21"
                sidebar_text = "#FFFFFF"
                button_hover = "#4D4D4D"
                main_bg = "#2D2D2D"
                main_text = "#FFFFFF"
                card_bg = "#3D3D3D"
                card_bd = "gray"
                card_text = "#FFFFFF"
                table_bg = "#3D3D3D"
                table_text = "#FFFFFF"
                search_bg = "gray"
                add_bg = "#0E283F"
                row_sep = "light gray"
                
                self.theme_btn.setIcon(light_icon)
        else:
                # Original/Light color
                sidebar_bg = "#1F1F21"
                sidebar_text = "#fff"
                button_hover = "#8DB8E0"
                main_bg = "#B2CDE9"
                main_text = "#0E283F"
                card_bg = "#C6D7EC"
                card_bd = "#fff"
                card_text = "#37547A"
                table_bg = "#C6D7EC"
                table_text = "#64748B"
                search_bg = "#F1F5F9"
                add_bg = "#0E283F"
                row_sep = "#e5e7eb"
                self.theme_btn.setIcon(dark_icon)

        
        # Apply to Pages
        self.Pages.setStyleSheet(f"""
                background: {main_bg};
                color: {main_text};
        """)
        
        #Apply to user card
        self.UserCard.setStyleSheet(f"background-color: {main_bg} ; border-radius: 10px;")
        
        # Apply to top bars
        for frame in [self.dash_graph, self.frame_4, self.app_frame, self.Bill_frame, self.Reports_topbar_frame]:
                frame.setStyleSheet(f"background-color: {main_bg};")
        
        # Apply to labels in top bars
        for label in [self.label_12, self.label_13, self.label_14, self.label_15]:
                label.setStyleSheet(f"background-color: {main_bg}; color: {main_text};")
        
        # Apply to cards
        for card in [self.dash_graph, self.TotPat_card, self.TodApp_card, self.PendPay_card, self.ComTreat_card, 
                        self.frame_2, self.frame_3, self.Pat_table_Frame, self.app_table_frame, 
                        self.bill_table_frame, self.Reports_table_frame]:
                card.setStyleSheet(f"""
                background: {card_bg};
                border: 1px solid {card_bg};  
                border-radius: 12px;
                """)
        
        # Apply to card labels
        for label in [self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, 
                        self.label_7, self.label_8, self.label_9, self.label_10]:
                label.setStyleSheet(f"background: {card_bg}; color: {card_text};")
        
        # Apply to sidebar buttons
        sidebar_buttons = [self.Dash_btn, self.Patient_btn, self.Apntmnt_btn, self.Bill_btn, self.Rep_btn]
        for btn in sidebar_buttons:
                btn.setStyleSheet(f"""
                QPushButton {{
                        text-align: left;
                        padding: 10px;
                        background-color: transparent;
                        border: none;
                        color: {sidebar_text};
                        font-size: 16px;
                        font-family: Ondo;
                        font-weight: bold;
                }}
                QPushButton:hover{{
                        background-color: {button_hover};
                        color: {sidebar_text};
                        border-radius: 8px;
                }}
                QPushButton:checked {{
                        background-color: {button_hover};
                        color: {sidebar_text};
                        border-radius: 8px;
                }}
                                       """)
    
        # Apply to headers (TOP BAR)
        for header in [self.frame_4,self.app_frame,self.Bill_frame,self.Reports_topbar_frame]:
                header.setStyleSheet(f"""
                        background-color: {main_bg};
                                     """)
        
        # Apply to header labels (TOP BAR)
        for title in [self.label_12,self.label_13,self.label_14,self.label_15]:
                title.setStyleSheet(f"""
                        background-color: {main_bg};
                        color: {main_text};
                                    """)
        
        # DASHBOARD PAGE
        # Apply to Card frames
        for card_fr in [self.dash_graph,self.TotPat_card, self.TodApp_card, self.PendPay_card, self.ComTreat_card]:
                card_fr.setStyleSheet(f"""
                        background-color: {card_bg};
                        border: 1px solid {card_bd};
                        border-radius: 12px;
                                      """)
        
        # Apply to Card icons
        for card_icon in [self.totpat_icon, self.totapp_icon, self.pay_icon, self.treat_icon]:
                card_icon.setStyleSheet("""
                        background: transparent; 
                        border: none;
                        """)
                
        # Apply to Dashboard titles
        for titles in [self.graph_label, self.label_2, self.label_3, self.label_4, self.label_8, self.label_10]:
                titles.setStyleSheet(f"""
                        background: {card_bg};
                        color: {card_text};
                        border: none;
                        """)
        
        # Apply to Card count
        for card_count in [self.label_5, self.label_6, self.label_7, self.label_9]:
                card_count.setStyleSheet(f"""
                        background: {card_bg};
                        color: {card_text};
                        border: none;                     
                        """)
        
        # Apply to Dashboard table frame
        self.frame_2.setStyleSheet(f"""
                #frame_2{{
                        background: {table_bg};
                        border: 1px solid {card_bd};
                        border-radius: 12px;}}
                        """)
        
        self.frame_3.setStyleSheet(f"""
                #frame_3{{
                        background: {table_bg};
                        border: 1px solid {card_bd};
                        border-radius: 12px;
                        }}                
                        """)

        # Apply to Dashboard table
        for dash_app in [self.UpAp_table]:
                dash_app.setStyleSheet(f"""
                QTableWidget{{
                        background-color: {table_bg};
                        border: none;
                        border-radius: 0;
                }}
                QTableWidget::item {{
                        border-bottom: 1px solid {row_sep};
                }}
                QHeaderView::section {{
                        border: none;
                        background-color: {table_bg};
                }}

                QHeaderView::section {{
                        border: none !important;  
                        background-color: {table_bg};
                        padding: 5px;
                }}
                        """)
                dash_app.horizontalHeader().setStyleSheet(f"""
                QHeaderView::section {{
                        font-family: "Inter"; 
                        font-size: 14px;        
                        color: {table_text};       
                        padding: 5px;  
                        background-color: {table_bg};      
                }}
                """)
                
        # Apply to user card
        self.UserCard.setStyleSheet(f"background-color: {main_bg} ; border-radius: 10px;")
        
        # Apply to all search
        for search in [self.search_patient, self.Search_app, self.Search_bill]:
                search.setStyleSheet(f"""
                        background-color: {search_bg}; 
                        border-radius: 8px;        
                                     
                        """)

        # Apply to all add buttons
        for add_btn in [self.add_icon, self.AddApp_btn, self.AddBill_btn]:
                add_btn.setStyleSheet(f"""
                        background-color: {add_bg}; 
                        border-radius: 8px; 
                        color: white;                        
                        """)
        # TABLE FRAMES
        # Apply to Patient table frame
        self.Pat_table_Frame.setStyleSheet(f"""
                #Pat_table_Frame{{
                        background: {table_bg};
                        border: 1px solid {card_bd};  
                        border-radius: 12px;
                        }}                                
                        """)
        
        # Apply to Appointment table frame
        self.app_table_frame.setStyleSheet(f"""
                #app_table_frame {{
                        background: {table_bg};
                        border: 1px solid {card_bd};  
                        border-radius: 12px;
                        }}
                        """)
        
        # Apply to Billing table frame
        self.bill_table_frame.setStyleSheet(f"""
                #bill_table_frame {{
                        background: {table_bg};
                        border: 1px solid {card_bd};  
                        border-radius: 12px;
                        }}
                        """)
        
        # Apply to Report table frame
        self.Reports_table_frame.setStyleSheet(f"""
                #Reports_table_frame {{
                        background: {table_bg};
                        border: 1px solid {card_bd};
                        border-radius: 12px;
                        }}
                        """)
        
        # Apply to all tables
        for tables in [self.Patients_table, self.Appointments_table, self.Billing_table]:
                tables.setStyleSheet(f"""
                        QTableWidget {{
                                background-color: {table_bg};
                                border: none;
                                gridline-color: transparent;
                        }}
                        QTableWidget::item {{
                                border-bottom: 1px solid {row_sep};
                                color: {table_text};
                        }}
                        QHeaderView::section {{
                                border: none;
                                background-color: {table_bg};
                                color: {table_text};
                        }}
                        """)             
                tables.horizontalHeader().setStyleSheet(f"""
                        QHeaderView::section {{
                                font-family: "Inter"; 
                                font-size: 14px;        
                                color: {table_text};                
                        }}
                        """)                     

        # Apply to button filter frames
        for fil_bg in [self.horizontalLayoutWidget, self.horizontalLayoutWidget_2]:
                fil_bg.setStyleSheet(f"""
                        background-color: {table_bg};           
                                     
                        """)
        
        # Apply to button filter in Appointment and Billing page
        for fil_btn in [self.pushButton_8, self.pushButton_9, self.pushButton_7, self.pushButton_6, 
                        self.pushButton_12, self.pushButton_13, self.pushButton_14, self.pushButton_15]:
                fil_btn.setStyleSheet(f"""
                        QPushButton {{
                                text-align: left;
                                padding: 10px;
                                background-color: {table_bg};
                                border: none;
                                color: {card_text};
                                font-size: 16px;
                                text-align: center;
                                font-family: Inter;                
                        }}
                        QPushButton:hover {{
                                background-color: {button_hover};
                                color: {card_text};
                                border-radius: 8px;
                        }}
                        """)         
       #Apply to calendar
        if not self.dark_mode:
                # Restore frame_3 original style
                self.frame_3.setStyleSheet("""
                #frame_3 {
                background: #1F1F21;
                border: 1px solid #5e93bf;
                border-radius: 12px;
                }
                """)

                # Restore calendar original styles
                self.calendar.setStyleSheet("""
                QCalendarWidget {
                background: transparent;
                border: none;
                }

                QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: transparent;
                border: none;
                }

                QCalendarWidget QWidget#qt_calendar_calendarview {
                background: transparent;
                border-radius: 12px;
                }

                QCalendarWidget QAbstractItemView {
                background: transparent;
                selection-background-color: #5e93bf;
                color: white;
                gridline-color: #5e93bf;
                border-radius: 12px;
                }

                QCalendarWidget QAbstractItemView::item {
                outline: none;
                border: none;
                }

                QCalendarWidget QToolButton {
                background: transparent;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                }

                QCalendarWidget QAbstractItemView:item:selected:!active,
                QCalendarWidget QAbstractItemView:item:selected:active {
                background-color: #5e93bf;
                border-radius: 15px;
                color: white;
                }

                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover {
                color: white;
                }

                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(6),
                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(7) {
                color: #7c94a3;
                }
                """)

                weekend_format = QtGui.QTextCharFormat()
                weekend_format.setForeground(QtGui.QColor("#7c94a3"))
                self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
                self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)

                font = QtGui.QFont("Inter", 9)
                self.calendar.setFont(font)
                self.calendar.setFixedHeight(300)
                self.calendar.setFixedWidth(300)

                prev_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
                next_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
                left = QtGui.QIcon(f"{filepath}Left.svg")
                right = QtGui.QIcon(f"{filepath}Right.svg")
                prev_btn.setIcon(left)
                next_btn.setIcon(right)
                prev_btn.setIconSize(QtCore.QSize(20, 20))
                next_btn.setIconSize(QtCore.QSize(20, 20))

        else:
                # Dark mode - you can add calendar styles here if you want to style it differently
                # Or keep it with dark colors like you did with other cards (optional)
                self.frame_3.setStyleSheet(f"""
                background: {card_bg};
                border: 1px solid {card_bg};  
                border-radius: 12px;
                """)

                self.calendar.setStyleSheet(f"""
                QCalendarWidget {{
                background: transparent;
                border: none;
                }}
                QCalendarWidget QWidget#qt_calendar_navigationbar {{
                background: transparent;
                border: none;
                }}
                QCalendarWidget QWidget#qt_calendar_calendarview {{
                background: transparent;
                border-radius: 12px;
                }}
                QCalendarWidget QAbstractItemView {{
                background: transparent;
                selection-background-color: #5e93bf;
                color: white;
                gridline-color: #5e93bf;
                border-radius: 12px;
                }}
                QCalendarWidget QAbstractItemView::item {{
                outline: none;
                border: none;
                }}
                QCalendarWidget QToolButton {{
                background: transparent;
                color: white;
                font-weight: bold;
                border: none;
                padding: 5px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                }}
                QCalendarWidget QAbstractItemView:item:selected:!active,
                QCalendarWidget QAbstractItemView:item:selected:active {{
                background-color: #5e93bf;
                border-radius: 15px;
                color: white;
                }}
                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover {{
                color: white;
                }}
                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(6),
                QCalendarWidget QAbstractItemView:item:enabled:!selected:!hover:nth-child(7) {{
                color: #7c94a3;
                }}
                """)

                weekend_format = QtGui.QTextCharFormat()
                weekend_format.setForeground(QtGui.QColor("#7c94a3"))
                self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Saturday, weekend_format)
                self.calendar.setWeekdayTextFormat(Qt.DayOfWeek.Sunday, weekend_format)

                font = QtGui.QFont("Inter", 9)
                self.calendar.setFont(font)
                self.calendar.setFixedHeight(300)
                self.calendar.setFixedWidth(300)

                prev_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_prevmonth")
                next_btn = self.calendar.findChild(QtWidgets.QToolButton, "qt_calendar_nextmonth")
                left = QtGui.QIcon(f"{filepath}Left.svg")
                right = QtGui.QIcon(f"{filepath}Right.svg")
                prev_btn.setIcon(left)
                next_btn.setIcon(right)
                prev_btn.setIconSize(QtCore.QSize(20, 20))
                next_btn.setIconSize(QtCore.QSize(20, 20))
        
        #TODO all tables should not be editable
        #TODO all column in a row should be selectable