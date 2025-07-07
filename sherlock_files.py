from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QFileDialog
)
from PySide6.QtCore import QThread, Signal, QObject
import os

# ✅ Worker class with cancel support
class FileSearchWorker(QObject):
    finished = Signal(list)

    def __init__(self, folder, keyword):
        super().__init__()
        self.folder = folder
        self.keyword = keyword
        self._is_cancelled = False

    def run(self):
        matches = []
        for root, dirs, files in os.walk(self.folder):
            if self._is_cancelled:
                break
            for file in files:
                if self._is_cancelled:
                    break
                if self.keyword.lower() in file.lower():
                    full_path = os.path.join(root, file)
                    matches.append(full_path)
        self.finished.emit(matches)

    def cancel(self):
        self._is_cancelled = True


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

import subprocess
import platform

# 🌟 Open files/folders when double-clicked
def on_item_double_clicked(item):
    path = item.text()

    if not os.path.exists(path):
        return

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":  # macOS
        subprocess.run(["open", path])
    else:  # Linux
        subprocess.run(["xdg-open", path])

# 🌟 Results list
results_list = QListWidget()
results_list.itemDoubleClicked.connect(on_item_double_clicked)

# 🌟 Results list
results_list = QListWidget()
results_list.itemDoubleClicked.connect(on_item_double_clicked)


# 🌟 Default search folder
selected_folder = os.path.expanduser("~/Documents")

# 🌟 Buttons and labels
choose_folder_button = QPushButton("Choose Folder")
search_button = QPushButton("Search")
cancel_button = QPushButton("Cancel Search")
status_label = QLabel("Ready.")

# 🌟 Global variables to manage worker + thread
current_worker = None
current_thread = None


# 🌟 Folder picker action
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")


# 🌟 Search complete handler
def on_search_complete(results, thread, worker):
    global current_worker, current_thread

    thread.quit()
    thread.wait()
    worker.deleteLater()
    thread.deleteLater()

    current_worker = None
    current_thread = None

    results_list.clear()
    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")

    status_label.setText("Search complete.")


# 🌟 Search action
def on_search():
    global current_worker, current_thread

    keyword = search_input.text().strip()
    results_list.clear()
    status_label.setText("Searching...")

    if not keyword:
        results_list.addItem("Please enter a search keyword.")
        status_label.setText("Ready.")
        return

    results_list.addItem("Searching, please wait...")
    QApplication.processEvents()

    worker = FileSearchWorker(selected_folder, keyword)
    thread = QThread()
    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    worker.finished.connect(lambda results: on_search_complete(results, thread, worker))

    current_worker = worker
    current_thread = thread

    thread.start()


# 🌟 Cancel search action
def on_cancel_search():
    global current_worker, current_thread

    if current_worker and current_thread:
        current_worker.cancel()
        status_label.setText("Cancelling...")
    else:
        status_label.setText("No active search.")


# 🌟 Connect buttons
choose_folder_button.clicked.connect(on_choose_folder)
search_button.clicked.connect(on_search)
cancel_button.clicked.connect(on_cancel_search)


# 🌟 Add widgets to layouts
search_layout.addWidget(search_input)
search_layout.addWidget(choose_folder_button)
search_layout.addWidget(search_button)
search_layout.addWidget(cancel_button)

main_layout.addLayout(search_layout)
main_layout.addWidget(QLabel("Search Results:"))
main_layout.addWidget(results_list)
main_layout.addWidget(status_label)

# 🌟 Finalize window
window.setLayout(main_layout)
window.show()

# 🌟 Start the app event loop
app.exec()
