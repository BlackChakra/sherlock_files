from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QFileDialog
)
from PySide6.QtCore import QThread, Signal, QObject

import os

# ✅ Worker class for running the file search in a separate thread
class FileSearchWorker(QObject):
    finished = Signal(list)  # Signal to send the results back

    def __init__(self, folder, keyword):
        super().__init__()
        self.folder = folder
        self.keyword = keyword

    def run(self):
        matches = []
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if self.keyword.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        self.finished.emit(matches)


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


# ✅ Folder picker action
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")


# ✅ Search complete handler (defined at top level, not inside another function!)
def on_search_complete(results, thread, worker):
    # Stop and clean up the thread
    thread.quit()
    thread.wait()
    worker.deleteLater()
    thread.deleteLater()

    # Show the search results
    results_list.clear()
    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")


# ✅ Search action (now runs in a thread)
def on_search():
    keyword = search_input.text().strip()
    results_list.clear()

    if not keyword:
        results_list.addItem("Please enter a search keyword.")
        return

    results_list.addItem("Searching, please wait...")
    QApplication.processEvents()

    # Start the worker thread
    worker = FileSearchWorker(selected_folder, keyword)
    thread = QThread()
    worker.moveToThread(thread)

    # When the thread starts, run the worker's run() method
    thread.started.connect(worker.run)

    # When finished, call on_search_complete
    worker.finished.connect(lambda results: on_search_complete(results, thread, worker))

    # Start the thread
    thread.start()


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
