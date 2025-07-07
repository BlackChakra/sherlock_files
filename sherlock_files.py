from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QFileDialog
)

import os

# 🔍 Function to find matching files in a folder
def find_files(search_folder, keyword):
    matches = []
    for root, dirs, files in os.walk(search_folder):
        for file in files:
            if keyword.lower() in file.lower():
                full_path = os.path.join(root, file)
                matches.append(full_path)
    return matches

# 🌟 Start the app
app = QApplication([])

# 🌟 Create the main window
window = QWidget()
window.setWindowTitle("Sherlock Files 🕵️‍♂️")
window.setFixedSize(600, 400)

# 🌟 Layouts
main_layout = QVBoxLayout()
search_layout = QHBoxLayout()

# 🌟 Search input
search_input = QLineEdit()
search_input.setPlaceholderText("Enter file name to search")

# 🌟 Results list
results_list = QListWidget()

# 🌟 Default search folder
selected_folder = os.path.expanduser("~/Documents")

# 🌟 Buttons
choose_folder_button = QPushButton("Choose Folder")
search_button = QPushButton("Search")

# 🌟 Folder picker action
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")

# 🌟 Search action
def on_search():
    keyword = search_input.text().strip()
    results_list.clear()

    search_folder = selected_folder
    results = find_files(search_folder, keyword)

    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")

# 🌟 Connect buttons
choose_folder_button.clicked.connect(on_choose_folder)
search_button.clicked.connect(on_search)

# 🌟 Add widgets to layouts
search_layout.addWidget(search_input)
search_layout.addWidget(choose_folder_button)
search_layout.addWidget(search_button)

main_layout.addLayout(search_layout)
main_layout.addWidget(QLabel("Search Results:"))
main_layout.addWidget(results_list)

# 🌟 Finalize window
window.setLayout(main_layout)
window.show()

# 🌟 Start the app event loop
app.exec()
