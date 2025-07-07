from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget, QLabel, QFileDialog, QCompleter
)
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtGui import QIcon
from PySide6.QtCore import QStringListModel
import subprocess
import platform
import os


# 🌟 Worker class
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
                full_path = os.path.join(root, file)
                if self.keyword.lower() in full_path.lower():
                    matches.append(full_path)
        self.finished.emit(matches)

    def cancel(self):
        self._is_cancelled = True


# 🌟 Open file/folder on double-click
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


# 🌟 App Setup
app = QApplication([])
window = QWidget()
window.setWindowTitle("Sherlock Files 🕵️‍♂️")
window.setWindowIcon(QIcon("assets/icon.png"))
window.resize(600, 400)

main_layout = QVBoxLayout()
search_layout = QHBoxLayout()

# 🌟 Search input & autocomplete
search_input = QLineEdit()
search_input.setPlaceholderText("Enter file name or folder name to search")

search_history = []  # stores last 5 search terms
completer = QCompleter(search_history)
search_input.setCompleter(completer)

# 🌟 Results list
results_list = QListWidget()
results_list.itemDoubleClicked.connect(on_item_double_clicked)

# 🌟 Status + Folder labels
status_label = QLabel("Ready.")
selected_folder = os.path.join(os.path.expanduser("~"), "Desktop")
folder_label = QLabel(f"Folder: {selected_folder}")

# 🌟 Buttons
choose_folder_button = QPushButton("Choose Folder")
search_button = QPushButton("Search")
cancel_button = QPushButton("Cancel Search")
clear_button = QPushButton("Clear Results")

# 🌟 Search state
current_worker = None
current_thread = None


# 🌟 Folder picker
def on_choose_folder():
    global selected_folder
    folder = QFileDialog.getExistingDirectory(window, "Select Folder")
    if folder:
        selected_folder = folder
        folder_label.setText(f"Folder: {selected_folder}")
        results_list.clear()
        results_list.addItem(f"Searching in: {selected_folder}")


# 🌟 Search completion
def on_search_complete(results):
    global current_worker, current_thread

    results_list.clear()
    if results:
        for file_path in results:
            results_list.addItem(file_path)
    else:
        results_list.addItem("No files found.")

    status_label.setText("Search complete.")

    if current_thread:
        current_thread.quit()
        current_thread.wait()
        current_thread.deleteLater()

    if current_worker:
        current_worker.deleteLater()

    current_worker = None
    current_thread = None


# 🌟 Start search
def on_search():
    global current_worker, current_thread, search_history

    keyword = search_input.text().strip()
    results_list.clear()
    status_label.setText("Searching...")

    if not keyword:
        results_list.addItem("Please enter a search keyword.")
        status_label.setText("Ready.")
        return

    # ➕ Add keyword to search history (keep last 5)
    if keyword not in search_history:
        search_history.append(keyword)
        if len(search_history) > 5:
            search_history.pop(0)
        completer.setModel(QStringListModel(search_history))

    results_list.addItem("Searching, please wait...")
    QApplication.processEvents()

    worker = FileSearchWorker(selected_folder, keyword)
    thread = QThread()
    worker.moveToThread(thread)

    thread.started.connect(worker.run)
    worker.finished.connect(on_search_complete)

    current_worker = worker
    current_thread = thread

    thread.start()


# 🌟 Cancel search
def on_cancel_search():
    global current_worker
    if current_worker:
        current_worker.cancel()
        status_label.setText("Cancelling...")
    else:
        status_label.setText("No active search.")


# 🌟 Clear results
def on_clear():
    results_list.clear()
    status_label.setText("Results cleared.")


# 🌟 Layout wiring
search_layout.addWidget(search_input)
search_layout.addWidget(choose_folder_button)
search_layout.addWidget(search_button)
search_layout.addWidget(cancel_button)

main_layout.addLayout(search_layout)
main_layout.addWidget(folder_label)
main_layout.addWidget(QLabel("Search Results:"))
main_layout.addWidget(results_list)
main_layout.addWidget(clear_button)
main_layout.addWidget(status_label)

window.setLayout(main_layout)
window.show()

# 🌟 Button connections
choose_folder_button.clicked.connect(on_choose_folder)
search_button.clicked.connect(on_search)
cancel_button.clicked.connect(on_cancel_search)
clear_button.clicked.connect(on_clear)

# 🌟 Styling
app.setStyleSheet("""
    QWidget {
        font-family: Arial;
        font-size: 12pt;
    }
    QPushButton {
        padding: 6px 12px;
        font-weight: bold;
    }
    QLineEdit {
        padding: 4px;
    }
    QListWidget {
        padding: 4px;
    }
""")

# 🌟 Run app
app.exec()
