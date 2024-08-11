import fnmatch
import os

from PyQt5.QtCore import Qt, QEventLoop, QTimer, QCoreApplication
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import ComboBox, PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, InfoBarIcon, PrimaryPushButton, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView

class HomeInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.plain_TextEdit = TextEdit(self)
		self.general_Setting = GeneralSetting(self)
		self.display_Card = DisplayCard(self)

		self.horizontalLayout_1 = QHBoxLayout()
		self.horizontalLayout_2 = QHBoxLayout(self)
		self.verticalLayout_1 = QVBoxLayout()

		self.horizontalLayout_1.addLayout(self.verticalLayout_1)
		self.horizontalLayout_1.addWidget(self.plain_TextEdit)
		self.horizontalLayout_2.addLayout(self.horizontalLayout_1)
		self.verticalLayout_1.addWidget(self.general_Setting)
		self.verticalLayout_1.addWidget(self.display_Card)

		self.general_Setting.setFixedWidth(500)
		self.display_Card.setFixedWidth(500)
		self.horizontalLayout_2.setContentsMargins(20, 20, 20, 23)

		self.verticalLayout_1.setContentsMargins(-1, -1, 15, -1)
		self.verticalLayout_1.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

class CompileAction:
	def __init__(self, plain_TextEdit: PlainTextEdit):
		self.text_edit = plain_TextEdit

	def perform_Action(self):
		for i in range(100):
			self.text_edit.appendPlainText("编译按钮被点击了！" + str(i))
			QCoreApplication.processEvents()

class TextEdit(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('运行状态')

		self.plain_TextEdit = PlainTextEdit(self)
		self.plain_TextEdit.setReadOnly(True)

		self.viewLayout.addWidget(self.plain_TextEdit)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def appendPlainText(self, text):
		self.plain_TextEdit.appendPlainText(text)

class DisplayCard(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle("图片")

		self.flipView = HorizontalFlipView(self)

		self.LoadImage('images/DisPlay/','*.jpg')

		self.flipView.setBorderRadius(4)
		self.flipView.setSpacing(5)
		self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

		self.viewLayout.addWidget(self.flipView)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def LoadImage(self,directory,pattern):
		for filename in os.listdir(directory):
			if fnmatch.fnmatch(filename, pattern):
				file_path = os.path.join(directory, filename)
				self.flipView.addImage(file_path)

class GeneralSetting(GroupHeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle("设置")

		self.comboBox = ComboBox()
		self.comboBox.setFixedWidth(200)
		self.comboBox.addItems(["崩坏学园2", "崩坏3", "原神", "未定事件簿", "绝区零", "大别野"])

		self.lineEdit_1 = LineEdit()
		self.lineEdit_2 = LineEdit()
		self.lineEdit_3 = LineEdit()
		self.lineEdit_1.setFixedWidth(200)
		self.lineEdit_2.setFixedWidth(200)
		self.lineEdit_3.setFixedWidth(200)
		self.lineEdit_1.setPlaceholderText("输入")
		self.lineEdit_2.setPlaceholderText("输入")
		self.lineEdit_3.setPlaceholderText("输入")

		self.hintIcon = IconWidget(InfoBarIcon.INFORMATION)
		self.hintLabel = BodyLabel("点击运行按钮以开始运行 🤣👉")
		self.compileButton = PrimaryPushButton(FluentIcon.PLAY_SOLID, "运行")
		self.compile_Action = CompileAction(parent.plain_TextEdit)

		self.bottomLayout = QHBoxLayout()

		self.hintIcon.setFixedSize(16, 16)
		self.compileButton.setFixedWidth(100)
		self.compileButton.clicked.connect(self.compile_Action.perform_Action)
		self.bottomLayout.setSpacing(10)
		self.bottomLayout.setContentsMargins(24, 15, 24, 20)
		self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignLeft)
		self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
		self.bottomLayout.addStretch(1)
		self.bottomLayout.addWidget(self.compileButton, 0, Qt.AlignRight)
		self.bottomLayout.setAlignment(Qt.AlignVCenter)

		self.addGroup(FluentIcon.BACKGROUND_FILL, "选择分区", "选择评论区所在的分区", self.comboBox)
		self.addGroup(FluentIcon.BACKGROUND_FILL, "动态ID", "选择软件的入口脚本", self.lineEdit_1)
		self.addGroup(FluentIcon.BACKGROUND_FILL, "入口脚本", "选择软件的入口脚本", self.lineEdit_2)
		group = self.addGroup(FluentIcon.BACKGROUND_FILL, "入口脚本", "选择软件的入口脚本", self.lineEdit_3)
		group.setSeparatorVisible(True)
		self.vBoxLayout.addLayout(self.bottomLayout)
