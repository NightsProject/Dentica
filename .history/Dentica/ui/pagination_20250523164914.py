from PyQt6 import QtWidgets, QtCore

class TablePagination:
    def __init__(self, table_widget, rows_per_page=10):
        self.table = table_widget
        self.rows_per_page = rows_per_page
        self.current_page = 1
        self.total_pages = 1
        self.total_rows = 0
        self.pagination_controls = None
        
    def setup_pagination_controls(self, parent_frame, y_offset=0):
        """Create and position pagination controls below the table"""
        self.pagination_controls = QtWidgets.QFrame(parent=parent_frame)
        self.pagination_controls.setGeometry(QtCore.QRect(
            self.table.geometry().x(),
            self.table.geometry().y() + self.table.geometry().height() + y_offset,
            self.table.geometry().width(),
            40
        ))
        self.pagination_controls.setStyleSheet("background: transparent;")
        
        # Layout for pagination controls
        hbox = QtWidgets.QHBoxLayout(self.pagination_controls)
        hbox.setContentsMargins(0, 0, 0, 0)
        
        # Previous button
        self.prev_btn = QtWidgets.QPushButton("Previous")
        self.prev_btn.setFixedWidth(80)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background: #8DB8E0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:disabled {
                background: #C6D7EC;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_page)
        
        # Page info label
        self.page_label = QtWidgets.QLabel()
        self.page_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.page_label.setStyleSheet("color: #64748B;")
        
        # Next button
        self.next_btn = QtWidgets.QPushButton("Next")
        self.next_btn.setFixedWidth(80)
        self.next_btn.setStyleSheet("""
            QPushButton {
                background: #8DB8E0;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 5px;
            }
            QPushButton:disabled {
                background: #C6D7EC;
            }
        """)
        self.next_btn.clicked.connect(self.next_page)
        
        # Add widgets to layout
        hbox.addWidget(self.prev_btn)
        hbox.addWidget(self.page_label)
        hbox.addWidget(self.next_btn)
        
        self.update_pagination_controls()
        
    def update_pagination_controls(self):
        """Update the state of pagination controls"""
        self.page_label.setText(f"Page {self.current_page} of {self.total_pages}")
        self.prev_btn.setDisabled(self.current_page == 1)
        self.next_btn.setDisabled(self.current_page == self.total_pages)
        
    def set_total_rows(self, total_rows):
        """Set the total number of rows and calculate total pages"""
        self.total_rows = total_rows
        self.total_pages = max(1, (total_rows + self.rows_per_page - 1) // self.rows_per_page)
        self.current_page = min(self.current_page, self.total_pages)
        self.update_pagination_controls()
        
    def get_current_page_rows(self):
        """Get the range of rows to display for current page"""
        start = (self.current_page - 1) * self.rows_per_page
        end = min(start + self.rows_per_page, self.total_rows)
        return start, end
        
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self.current_page -= 1
            self.update_pagination_controls()
            self.show_current_page()
            
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self.update_pagination_controls()
            self.show_current_page()
            
    def show_current_page(self):
        """Show only rows for current page"""
        start, end = self.get_current_page_rows()
        for row in range(self.table.rowCount()):
            self.table.setRowHidden(row, not (start <= row < end))