import asyncio

from PyQt5.QtCore import Qt, QCoreApplication, QDir
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, InfoBarIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, SplitPushButton
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicComboBox, AcrylicToolTipFilter

from Servers.CrawlingHoYo import spider_main

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
	def __init__(self, plain_TextEdit, general_Setting):
		self.plain_TextEdit = plain_TextEdit
		self.general_Setting = general_Setting

	def perform_Action(self, text):
		self.plain_TextEdit.appendPlainText(text)
		QCoreApplication.processEvents()

	def run_function(self):
		inputID = self.general_Setting.lineEdit_1.text()
		inputRequest = self.general_Setting.lineEdit_2.text()
		inputSave = self.general_Setting.lineEdit_3.text()
		self.perform_Action(f'动态ID值:{inputID}')
		self.perform_Action(f'单次请求数:{inputRequest}')
		self.perform_Action(f'单轮保存数:{inputSave}')
		if len(inputID) & len(inputRequest) & len(inputSave):
			asyncio.run(spider_main(inputID, inputRequest, inputSave, self))
			QCoreApplication.processEvents()
		else:
			self.perform_Action('为空，错误')

class TextEdit(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('📄  运 行')

		self.plain_TextEdit = PlainTextEdit(self)
		self.plain_TextEdit.setReadOnly(True)

		self.menu_Button = AcrylicSystemTrayMenu(self)
		self.action_1 = Action(FluentIcon.PAUSE, '全选')
		self.action_2 = Action(FluentIcon.COPY, 'Copy')
		self.action_3 = Action(FluentIcon.SAVE, 'Save')
		self.menu_Button.addActions([self.action_1, self.action_2, self.action_3])

		self.splitToolButton = SplitPushButton(FluentIcon.PAUSE, '清空', self)
		self.splitToolButton.setFlyout(self.menu_Button)
		self.splitToolButton.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.splitToolButton.installEventFilter(AcrylicToolTipFilter(self.splitToolButton, 0, ToolTipPosition.TOP))

		self.headerLayout.addWidget(self.splitToolButton)
		self.viewLayout.addWidget(self.plain_TextEdit)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def appendPlainText(self, text):
		self.plain_TextEdit.appendPlainText(text)

class DisplayCard(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('💖  插 图')

		self.flipView = HorizontalFlipView(self)

		self.flipView.setBorderRadius(4)
		self.flipView.setSpacing(5)
		self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
		self.flipView.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.flipView.installEventFilter(AcrylicToolTipFilter(self.flipView, 0, ToolTipPosition.TOP))

		self.LoadImage(':Images/DisPlay_Png/', '*.png')
		self.LoadImage(':Images/DisPlay_Jpg/', '*.jpg')

		self.viewLayout.addWidget(self.flipView)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def LoadImage(self, directory, pattern):
		direct = QDir(directory)
		files = direct.entryList([pattern], QDir.Files)
		for filename in files:
			file_path = f'{directory}{filename}'
			pixmap = QPixmap(file_path)
			self.flipView.addImage(pixmap)

class GeneralSetting(GroupHeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('⚙️  配 置')

		self.comboBox = AcrylicComboBox(self)
		self.lineEdit_1 = LineEdit(self)
		self.lineEdit_2 = LineEdit(self)
		self.lineEdit_3 = LineEdit(self)
		self.comboBox.setFixedWidth(200)
		self.lineEdit_1.setFixedWidth(200)
		self.lineEdit_2.setFixedWidth(200)
		self.lineEdit_3.setFixedWidth(200)
		self.comboBox.setPlaceholderText('✨选择分区不生效')
		self.lineEdit_1.setPlaceholderText('✨输入评论区ID')
		self.lineEdit_2.setPlaceholderText('✨输入≤50的正整数')
		self.lineEdit_3.setPlaceholderText('✨输入1W-10W的正整数')
		self.setIntegerValidator(self.lineEdit_1, 0, 1000000000)
		self.setIntegerValidator(self.lineEdit_2, 0, 50)
		self.setIntegerValidator(self.lineEdit_3, 0, 100000)
		self.comboBox.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_1.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_2.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_3.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.comboBox.installEventFilter(AcrylicToolTipFilter(self.comboBox, 0, ToolTipPosition.TOP))
		self.lineEdit_1.installEventFilter(AcrylicToolTipFilter(self.lineEdit_1, 0, ToolTipPosition.TOP))
		self.lineEdit_2.installEventFilter(AcrylicToolTipFilter(self.lineEdit_2, 0, ToolTipPosition.TOP))
		self.lineEdit_3.installEventFilter(AcrylicToolTipFilter(self.lineEdit_3, 0, ToolTipPosition.TOP))
		self.comboBox.addItems(['✨崩坏学园2', '✨崩坏3', '✨原神', '✨未定事件簿', '✨绝区零', '✨大别野'])
		self.comboBox.setCurrentIndex(-1)

		self.compile_Action = CompileAction(parent.plain_TextEdit, self)

		self.menu_Button = AcrylicSystemTrayMenu(self)
		self.action_1 = Action('✨高松灯', triggered=lambda: self.compile_Action.perform_Action('是会虚情假意呢🙄️'))
		self.action_2 = Action('✨千早爱音', triggered=lambda: self.compile_Action.perform_Action('想演奏是你们的自由，你们就请便吧🖐'))
		self.action_3 = Action('✨要乐奈', triggered=lambda: self.compile_Action.perform_Action('到现在都还执着于过去，真难看🙄️'))
		self.action_4 = Action('✨长崎爽世', triggered=lambda: self.compile_Action.perform_Action('你也差不多该忘记了吧😒'))
		self.action_5 = Action('✨椎名立希', triggered=lambda: self.compile_Action.perform_Action('那么那个乐团算什么😅'))
		self.menu_Button.addActions([self.action_1, self.action_2, self.action_3, self.action_4, self.action_5])

		self.hintIcon = IconWidget(InfoBarIcon.INFORMATION)
		self.hintLabel = BodyLabel('点击开始运行 🤣👉')
		self.compileButton = PrimarySplitPushButton("✨BanG Dream! It's MyGO!!!!!✨")
		self.hintIcon.setFixedSize(16, 16)
		self.compileButton.setFlyout(self.menu_Button)
		self.compileButton.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.compileButton.installEventFilter(AcrylicToolTipFilter(self.compileButton, 0, ToolTipPosition.TOP))
		self.compileButton.clicked.connect(self.compile_Action.run_function)

		self.bottomLayout = QHBoxLayout()
		self.bottomLayout.setSpacing(10)
		self.bottomLayout.setContentsMargins(24, 15, 24, 20)
		self.bottomLayout.addWidget(self.hintIcon)
		self.bottomLayout.addWidget(self.hintLabel)
		self.bottomLayout.addStretch(1)
		self.bottomLayout.addWidget(self.compileButton)

		self.addGroup(FluentIcon.PIN, '动态分区', '✨选择动态所在的分区', self.comboBox)
		self.addGroup(FluentIcon.LABEL, '动态 ID 值', '✨输入动态ID值', self.lineEdit_1)
		self.addGroup(FluentIcon.LABEL, '单次请求数', '✨输入单次请求数量', self.lineEdit_2)
		self.addGroup(FluentIcon.LABEL, '单轮保存数', '✨输入单轮保存数', self.lineEdit_3)
		self.groupWidgets[3].setSeparatorVisible(True)
		self.vBoxLayout.addLayout(self.bottomLayout)

	def setIntegerValidator(self, line_edit, min_value, max_value):
		validator = QIntValidator(min_value, max_value, self)
		line_edit.setValidator(validator)

		def adjust_input():
			text = line_edit.text()
			if text:
				value = int(text)
				if value < min_value:
					line_edit.setText(str(min_value))
				elif value > max_value:
					line_edit.setText(str(max_value))

		line_edit.textChanged.connect(adjust_input)
