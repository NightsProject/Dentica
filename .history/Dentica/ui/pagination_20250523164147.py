from PyQt6 import QtWidgets, QtCore

class PaginationSystem:
    def __init__(self, parent):
        self.parent = parent
        self.rows_per_page = 10  # Default rows per page
        
        # Initialize pagination for Patients table
        self.init_patients_pagination()
        
        # Initialize pagination for Appointments table
        self.init_appointments_pagination()
    
    def init_patients_pagination(self):
        """Initialize pagination controls for Patients table"""
        # Create pagination frame
        self.pat_pagination_frame = QtWidgets.QFrame(parent=self.parent.Pat_table_Frame)
        self.pat_pagination_frame.setGeometry(QtCore.QRect(10, 580, 880, 50))
        self.pat_pagination_frame.setStyleSheet("background: transparent;")
        
        # Create pagination layout
        self.pat_pagination_layout = QtWidgets.QHBoxLayout(self.pat_pagination_frame)
        self.pat_pagination_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add pagination controls
        self.pat_prev_btn = QtWidgets.QPushButton("Previous", parent=self.pat_pagination_frame)
        self.pat_next_btn = QtWidgets.QPushButton("Next", parent=self.pat_pagination_frame)
        self.pat_page_info = QtWidgets.QLabel("Page 1 of 1", parent=self.pat_pagination_frame)
        self.pat_rows_per_page = QtWidgets.QComboBox(parent=self.pat_pagination_frame)
        self.pat_rows_per_page.addItems(["5", "10", "20", "50", "100"])
        self.pat_rows_per_page.setCurrentText("10")
        
        # Add widgets to layout
        self.pat_pagination_layout.addWidget(self.pat_prev_btn)
        self.pat_pagination_layout.addWidget(self.pat_next_btn)
        self.pat_pagination_layout.addWidget(self.pat_page_info)
        self.pat_pagination_layout.addStretch()
        self.pat_pagination_layout.addWidget(QtWidgets.QLabel("Rows per page:", parent=self.pat_pagination_frame))
        self.pat_pagination_layout.addWidget(self.pat_rows_per_page)
        
        # Connect signals
        self.pat_prev_btn.clicked.connect(lambda: self.prev_page(self.parent.Patients_table, "patients"))
        self.pat_next_btn.clicked.connect(lambda: self.next_page(self.parent.Patients_table, "patients"))
        self.pat_rows_per_page.currentTextChanged.connect(lambda: self.change_rows_per_page(self.parent.Patients_table, "patients"))
        
        # Initialize pagination variables
        self.pat_current_page = 1
        self.pat_total_pages = 1
        self.pat_total_rows = 0
    
    def init_appointments_pagination(self):
        """Initialize pagination controls for Appointments table"""
        # Create pagination frame
        self.app_pagination_frame = QtWidgets.QFrame(parent=self.parent.app_table_frame)
        self.app_pagination_frame.setGeometry(QtCore.QRect(40, 580, 820, 50))
        self.app_pagination_frame.setStyleSheet("background: transparent;")
        
        # Create pagination layout
        self.app_pagination_layout = QtWidgets.QHBoxLayout(self.app_pagination_frame)
        self.app_pagination_layout.setContentsMargins(0, 0, 0, 0)
        
        # Add pagination controls
        self.app_prev_btn = QtWidgets.QPushButton("Previous", parent=self.app_pagination_frame)
        self.app_next_btn = QtWidgets.QPushButton("Next", parent=self.app_pagination_frame)
        self.app_page_info = QtWidgets.QLabel("Page 1 of 1", parent=self.app_pagination_frame)
        self.app_rows_per_page = QtWidgets.QComboBox(parent=self.app_pagination_frame)
        self.app_rows_per_page.addItems(["5", "10", "20", "50", "100"])
        self.app_rows_per_page.setCurrentText("10")
        
        # Add widgets to layout
        self.app_pagination_layout.addWidget(self.app_prev_btn)
        self.app_pagination_layout.addWidget(self.app_next_btn)
        self.app_pagination_layout.addWidget(self.app_page_info)
        self.app_pagination_layout.addStretch()
        self.app_pagination_layout.addWidget(QtWidgets.QLabel("Rows per page:", parent=self.app_pagination_frame))
        self.app_pagination_layout.addWidget(self.app_rows_per_page)
        
        # Connect signals
        self.app_prev_btn.clicked.connect(lambda: self.prev_page(self.parent.Appointments_table, "appointments"))
        self.app_next_btn.clicked.connect(lambda: self.next_page(self.parent.Appointments_table, "appointments"))
        self.app_rows_per_page.currentTextChanged.connect(lambda: self.change_rows_per_page(self.parent.Appointments_table, "appointments"))
        
        # Initialize pagination variables
        self.app_current_page = 1
        self.app_total_pages = 1
        self.app_total_rows = 0
    
    def update_pagination(self, table, table_type):
        if table_type == "patients":
            total_rows = table.rowCount()
            rows_per_page = int(self.pat_rows_per_page.currentText())
            total_pages = max(1, (total_rows + rows_per_page - 1) // rows_per_page)
            
            self.pat_total_rows = total_rows
            self.pat_total_pages = total_pages
            self.pat_current_page = min(self.pat_current_page, total_pages)
            
            # Update page info
            self.pat_page_info.setText(f"Page {self.pat_current_page} of {self.pat_total_pages}")
            
            # Enable/disable buttons
            self.pat_prev_btn.setEnabled(self.pat_current_page > 1)
            self.pat_next_btn.setEnabled(self.pat_current_page < self.pat_total_pages)
            
            # Show/hide rows based on current page
            start_row = (self.pat_current_page - 1) * rows_per_page
            end_row = min(start_row + rows_per_page, total_rows)
            
            for row in range(total_rows):
                table.setRowHidden(row, not (start_row <= row < end_row))
        
        elif table_type == "appointments":
            total_rows = table.rowCount()
            rows_per_page = int(self.app_rows_per_page.currentText())
            total_pages = max(1, (total_rows + rows_per_page - 1) // rows_per_page)
            
            self.app_total_rows = total_rows
            self.app_total_pages = total_pages
            self.app_current_page = min(self.app_current_page, total_pages)
            
            # Update page info
            self.app_page_info.setText(f"Page {self.app_current_page} of {self.app_total_pages}")
            
            # Enable/disable buttons
            self.app_prev_btn.setEnabled(self.app_current_page > 1)
            self.app_next_btn.setEnabled(self.app_current_page < self.app_total_pages)
            
            # Show/hide rows based on current page
            start_row = (self.app_current_page - 1) * rows_per_page
            end_row = min(start_row + rows_per_page, total_rows)
            
            for row in range(total_rows):
                table.setRowHidden(row, not (start_row <= row < end_row))
    
    def prev_page(self, table, table_type):
        if table_type == "patients":
            if self.pat_current_page > 1:
                self.pat_current_page -= 1
                self.update_pagination(table, table_type)
        elif table_type == "appointments":
            if self.app_current_page > 1:
                self.app_current_page -= 1
                self.update_pagination(table, table_type)
    
    def next_page(self, table, table_type):
        if table_type == "patients":
            if self.pat_current_page < self.pat_total_pages:
                self.pat_current_page += 1
                self.update_pagination(table, table_type)
        elif table_type == "appointments":
            if self.app_current_page < self.app_total_pages:
                self.app_current_page += 1
                self.update_pagination(table, table_type)
    
    def change_rows_per_page(self, table, table_type):
        if table_type == "patients":
            self.pat_current_page = 1  
            self.update_pagination(table, table_type)
        elif table_type == "appointments":
            self.app_current_page = 1  
            self.update_pagination(table, table_type)
    