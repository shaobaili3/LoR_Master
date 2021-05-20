import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Models import leaderboard as lb

class Table(QWidget):
    def __init__(self,parent=None):
        super(Table, self).__init__(parent)
        lb.updateLeaderboard()
        leaderboards = lb.leaderboards
        self.setWindowTitle('LoR Master Tracker Leaderboard')
        self.resize(700,1000)
        self.model=QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['NA 美服','EU 欧服','ASIA 亚服','SEA 东南亚服'])

        for column, leaderboard in enumerate(leaderboards):
            players = leaderboard.get('players')
            for row, player in enumerate(players):
                item=QStandardItem(player.get('name') + '  [' + str(int(player.get('lp'))) + ']')
                item.setTextAlignment(Qt.AlignVCenter)
                #设置每个位置的文本值
                self.model.setItem(row,column,item)

        self.tableView=QTableView()
        self.tableView.setModel(self.model)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #self.tableView.setSpan(0, 0, 0.5, 0.5)

        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout=QVBoxLayout()
        layout.addWidget(self.tableView)
        self.setLayout(layout)
