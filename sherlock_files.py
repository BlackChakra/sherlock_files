from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QFileDialog
)
from PySide6.QtCore import QThread, Signal, QObject, Qt
import subprocess
import platform
import os

# 🌟 Worker thread class
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
                    matches.append(os.path.join(root, file))
        self.finished.emit(matches)

    def cancel(self):
        self._is_cancelled = True


# 🌟 Open files/folders on double-click
def on_item_double_clicked(item):
    path = item.text()

    if not os.path.exists(path):
        return

    if platform.system() == "Windows":
        os.startfile(path)
    elif platform.system() == "Darwin":
        subprocess.run(["open", path])
    else:
        subprocess.run(["xdg-open", path])


# 🌟 App setup
app = QApplication([])
window = QWidget()
window.setWindowTitle("Sherlock Files 🕵️‍♂️")
window.setFixedSize(600, 400)

main_layout = QVBoxLayout()
search_layout = QHBoxLayout()

search_input = QLineEdit()
search_input.setPlaceholderText("Enter file name to search")

results_list = QListWidget()
results_list.itemDoubleClicked.connect(on_item_double_clicked)

status_label = QLabel("Ready.")

# 🌟 Buttons
choose_folder_button = QPushButton("Choose Folder")
search_button = QPushButton("Search")
cancel_button = QPushButton("Cancel Search")

# 🌟 Default search folder = Desktop for easier testing
selected_folder = os.path.join(os.path.expanduser("~"), "Desktop")
current_worker = None
current_thread = None


# 🌟 Folder picker
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")


# 🌟 Search complete
def on_search_complete(results):
    global current_worker, current_thread

    results_list.clear()
    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")

    status_label.setText("Search complete.")

    # Clean up the worker and thread
    if current_thread:
        current_thread.quit()
        current_thread.wait()
        current_thread.deleteLater()

    if current_worker:
        current_worker.deleteLater()

    # Clear references
    current_worker = None
    current_thread = None


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

    # ✅ FIX: Have the worker emit results and let the main thread clean up
    worker.finished.connect(lambda results: on_search_complete(results))

    current_worker = worker
    current_thread = thread

    thread.start()


# 🌟 Cancel action
def on_cancel_search():
    global current_worker
    if current_worker:
        current_worker.cancel()
        status_label.setText("Cancelling...")
    else:
        status_label.setText("No active search.")


# 🌟 Add widgets to layout
search_layout.addWidget(search_input)
search_layout.addWidget(choose_folder_button)
search_layout.addWidget(search_button)
search_layout.addWidget(cancel_button)

main_layout.addLayout(search_layout)
main_layout.addWidget(QLabel("Search Results:"))
main_layout.addWidget(results_list)
main_layout.addWidget(status_label)

window.setLayout(main_layout)
window.show()

# 🌟 Connect buttons
choose_folder_button.clicked.connect(on_choose_folder)
search_button.clicked.connect(on_search)
cancel_button.clicked.connect(on_cancel_search)

# 🌟 Start event loop
app.exec()
