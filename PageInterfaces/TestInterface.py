import ast
import asyncio
import threading

from PyQt5.QtCore import Qt, QCoreApplication, QDir, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QTableWidgetItem
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, CommandBarView, FlyoutAnimationType, Flyout, themeColor, LargeTitleLabel, SingleDirectionScrollArea, TableWidget
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicToolTipFilter, AcrylicEditableComboBox

from Servers.ActionController import ActionController
from Servers.CrawlingHoYo import spider_main

class TestInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.label = LargeTitleLabel(text=text)

		self.table_Widget = TableWidgets(self)
		# self.table_Widget.setFixedWidth(500)
		self.table_Widget.setBorderRadius(8)

		self.verticalLayout = QVBoxLayout(self)
		self.verticalLayout.addWidget(self.table_Widget)

class TableWidgets(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('🗂️  表 格')

		self.viewLayout.setContentsMargins(10, 5, 10, 10)

		self.table_Widget = TableWidget(self)
		self.table_Widget.setBorderVisible(True)
		self.table_Widget.setBorderRadius(8)

		self.tableInfos = [['success', 'time', 'userPhone', 'userName', 'orderNo', 'userAddress', 'userLicenseType', 'targetId', 'targetType']]
		self.table_Widget.setRowCount(len(self.tableInfos))
		self.table_Widget.setColumnCount(len(self.tableInfos[0]))

		for i, tableInfo in enumerate(self.tableInfos):
			for j in range(len(self.tableInfos[0])):
				self.table_Widget.setItem(i, j, QTableWidgetItem(tableInfo[j]))

		self.table_Widget.setHorizontalHeaderLabels(['状态', '时间', '手机号', '姓名', 'Old_No', '地址', '驾照类型', '驾校/教练ID', 'ID类型'])
		self.table_Widget.resizeColumnsToContents()
		# self.table_Widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
		self.table_Widget.setSortingEnabled(True)
		self.table_Widget.horizontalHeader().setEnabled(False)
		self.viewLayout.addWidget(self.table_Widget)

	def addRow(self, json_data):
		# json_data = ast.literal_eval(json_data)
		json_data = list(ast.literal_eval(json_data).values())

		row_position = self.table_Widget.rowCount()
		self.table_Widget.insertRow(row_position)

		for column, data in enumerate(json_data):
			self.table_Widget.setItem(row_position, column + 1, QTableWidgetItem(str(data)))

		self.table_Widget.resizeColumnsToContents()
