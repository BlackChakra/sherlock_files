from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel
)

# Create the main app
app = QApplication([])

# Create the main window
window = QWidget()
window.setWindowTitle("Sherlock Files 🕵️‍♂️")
window.setFixedSize(600, 400)  # Window size

# Vertical layout: stacks widgets from top to bottom
main_layout = QVBoxLayout()

# Horizontal layout for the search bar and button
search_layout = QHBoxLayout()

# Input where user types the filename
search_input = QLineEdit()
search_input.setPlaceholderText("Enter file name to search")

# Search button
search_button = QPushButton("Search")

# Add input and button to the search bar layout
search_layout.addWidget(search_input)
search_layout.addWidget(search_button)

# List to display search results
results_list = QListWidget()

# Add everything to the main layout
main_layout.addLayout(search_layout)
main_layout.addWidget(QLabel("Search Results:"))
main_layout.addWidget(results_list)

# Set the layout on the main window
window.setLayout(main_layout)

# Show the window
window.show()

# Start the event loop
app.exec()
