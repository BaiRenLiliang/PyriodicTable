import json
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QComboBox, QScrollArea, QTableView,
)



# Set up main window
class PyriodicTableApp(QMainWindow):
    def __init__(self, element_data):
        super().__init__()
        self.setWindowTitle('Pyriodic Table')
        self.setGeometry(100, 100, 800, 600)

        # Load element data
        self.element_data = element_data

        # Create main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layouts
        main_layout = QVBoxLayout(self.central_widget)

        # Periodic Table Section
        self.table_layout = QGridLayout()
        self.create_periodic_table()
        main_layout.addLayout(self.table_layout)

        # Filter Section
        self.filter_layout = QHBoxLayout()
        self.add_filter()
        main_layout.addLayout(self.filter_layout)

    # Create Periodic Table
    def create_periodic_table(self):
        for element in self.element_data:
            atomic_number = element['AtomicNumber']
            symbol = element['Symbol']
            row, col = element['ypos'], element['xpos']

            # Create button for each element
            btn = QPushButton(f'{symbol}\n{atomic_number}')
            btn.setFixedSize(50, 50)
            btn.clicked.connect(lambda _, e=element: self.show_element_details(e))
            self.table_layout.addWidget(btn, row, col)

    # Add Filter
    def add_filter(self):
        self.criteria_dropdown = QComboBox()
        self.criteria_dropdown.addItems(['Density', 'Melting Point', 'Boiling Point'])
        self.filter_layout.addWidget(QLabel("Filter by:"))
        self.filter_layout.addWidget(self.criteria_dropdown)

        # Filter button
        filter_btn = QPushButton("Apply Filter")
        filter_btn.clicked.connect(self.apply_filter)
        self.filter_layout.addWidget(filter_btn)

    # Show Element Details
    def show_element_details(self, element):
        # Show details in a popup or status bar
        details = (
            f"Name: {element['name']}\n"
            f"Symbol: {element['symbol']}\n"
            f"Atomic Number: {element['atomicNumber']}\n"
            f"Density: {element.get('density', 'N/A')}\n"
            f"Melting Point: {element.get('meltingPoint', 'N/A')} K\n"
            f"Boiling Point: {element.get('boilingPoint', 'N/A')} K"
        )
        self.statusBar().showMessage(details)

    # Apply Filter
    def apply_filter(self):
        # Get selected criteria
        criteria = self.criteria_dropdown.currentText()
        
        # Sort elements by the chosen criteria
        sorted_data = sorted(
            self.element_data, 
            key=lambda x: x.get(criteria.lower(), float('inf'))
        )
        
        # Refresh periodic table
        self.table_layout.deleteLater()  # Clear the current table
        self.table_layout = QGridLayout()  # Create a new layout
        self.create_periodic_table()  # Recreate with sorted data



# Import Periodic Table JSON
with open('periodic_table.json', 'r') as f:
    elements = json.load(f)['elements']







# Run the Application
app = QApplication(sys.argv)
window = PyriodicTableApp(elements)
window.show()
sys.exit(app.exec_())