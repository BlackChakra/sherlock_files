from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel
)
from PySide6.QtWidgets import QFileDialog

import os

def find_files(search_folder, keyword):
    matches = []
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if keyword.lower() in file.lower():
                full_path = os.path.join(root, file)
                matches.append(full_path)
    return matches

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

# Variable to hold the default search folder
selected_folder = os.path.expanduser("~/Documents")

# Choose Folder button
choose_folder_button = QPushButton("Choose Folder")

# Search button
search_button = QPushButton("Search")

# Action when Choose Folder button is clicked
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")

# Action when Search button is clicked
def on_search():
    # 1. Get search text from the input box
    keyword = search_input.text().strip()

    # 2. Clear previous results
    results_list.clear()

    # 3. Use the selected folder
    search_folder = selected_folder

    # 4. Run the file search
    results = find_files(search_folder, keyword)

    # 5. Show the results
    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")

# Connect buttons to their functions
choose_folder_button.clicked.connect(on_choose_folder)
search_button.clicked.connect(on_search)

# Add input and buttons to the search bar layout
search_layout.addWidget(search_input)
search_layout.addWidget(choose_folder_button)
search_layout.addWidget(search_button)


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
