import asyncio
import threading

from PyQt5.QtCore import Qt, QCoreApplication, QDir, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, CommandBarView, FlyoutAnimationType, Flyout, themeColor, LargeTitleLabel, SingleDirectionScrollArea
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicToolTipFilter, AcrylicEditableComboBox

from Servers.ActionController import ActionController
from Servers.CrawlingHoYo import spider_main

class TestInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.label = LargeTitleLabel(text=text)
		self.scrollArea = SingleDirectionScrollArea(orient=Qt.Vertical)
		self.verticalLayout = QVBoxLayout(self)

