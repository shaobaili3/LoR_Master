import sys
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QGroupBox
)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LoR Master Tracker")
        self.resize(480, 480)
        # Create a top-level layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        # Create the tab widget with two tabs
        tabs = QTabWidget()
        tabs.addTab(self.console(), "Console")
        tabs.addTab(self.inspection(), "Inspection")
        tabs.addTab(self.preferences(), "Preferences")
        layout.addWidget(tabs)

    def console(self):
        generalTab = QWidget
        consoleTab = QGroupBox("Group 1")
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("General Option 1"))
        layout.addWidget(QCheckBox("General Option 2"))
        # generalTab.group
        layout.addStretch(1)
        consoleTab.setLayout(layout)
        return consoleTab

    def inspection(self):
        networkTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Network Option 1"))
        layout.addWidget(QCheckBox("Network Option 2"))
        networkTab.setLayout(layout)
        return networkTab

    def preferences(self):
        networkTab = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(QCheckBox("Network Option 1"))
        layout.addWidget(QCheckBox("Network Option 2"))
        networkTab.setLayout(layout)
        return networkTab


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
