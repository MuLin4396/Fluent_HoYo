import fnmatch
import os

from PyQt5.QtCore import Qt, QCoreApplication
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, InfoBarIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, SplitPushButton
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicComboBox, AcrylicToolTipFilter

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

	def perform_Action(self, text: str):
		self.text_edit.appendPlainText(text)
		QCoreApplication.processEvents()

class TextEdit(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('📄  运 行')

		self.plain_TextEdit = PlainTextEdit(self)
		self.plain_TextEdit.setReadOnly(True)

		self.menu_Button = AcrylicSystemTrayMenu(self)
		self.action_1 = Action(FluentIcon.SEND, '全选')
		self.action_2 = Action(FluentIcon.COPY, 'Copy')
		self.action_3 = Action(FluentIcon.SAVE, 'Save')
		self.menu_Button.addActions([self.action_1, self.action_2, self.action_3])

		self.splitToolButton = SplitPushButton(FluentIcon.GITHUB.icon(), '清空', self)
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

		self.LoadImage('Images/DisPlay_Png/', '*.Png')
		self.LoadImage('Images/DisPlay_Jpg/', '*.jpg')

		self.viewLayout.addWidget(self.flipView)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def LoadImage(self, directory, pattern):
		for filename in os.listdir(directory):
			if fnmatch.fnmatch(filename, pattern):
				file_path = os.path.join(directory, filename)
				self.flipView.addImage(file_path)

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
		self.comboBox.setPlaceholderText('✨选择')
		self.lineEdit_1.setPlaceholderText('✨输入')
		self.lineEdit_2.setPlaceholderText('✨输入')
		self.lineEdit_3.setPlaceholderText('✨输入')
		self.lineEdit_1.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_2.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_3.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.comboBox.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.lineEdit_1.installEventFilter(AcrylicToolTipFilter(self.lineEdit_1, 0, ToolTipPosition.TOP))
		self.lineEdit_2.installEventFilter(AcrylicToolTipFilter(self.lineEdit_2, 0, ToolTipPosition.TOP))
		self.lineEdit_3.installEventFilter(AcrylicToolTipFilter(self.lineEdit_3, 0, ToolTipPosition.TOP))
		self.comboBox.installEventFilter(AcrylicToolTipFilter(self.comboBox, 0, ToolTipPosition.TOP))
		self.comboBox.addItems(['✨崩坏学园2', '✨崩坏3', '✨原神', '✨未定事件簿', '✨绝区零', '✨大别野', '✨shoko 🥰', '✨西宫硝子', '✨宝多六花', '✨小鸟游六花'])
		self.comboBox.setCurrentIndex(-1)

		self.compile_Action = CompileAction(parent.plain_TextEdit)

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
		self.compileButton.clicked.connect(lambda: self.compile_Action.perform_Action('迷子でもいい、迷子でも進め。'))

		self.bottomLayout = QHBoxLayout()
		self.bottomLayout.setSpacing(10)
		self.bottomLayout.setContentsMargins(24, 15, 24, 20)
		self.bottomLayout.addWidget(self.hintIcon)
		self.bottomLayout.addWidget(self.hintLabel)
		self.bottomLayout.addStretch(1)
		self.bottomLayout.addWidget(self.compileButton)

		self.addGroup(FluentIcon.BACKGROUND_FILL, '选择分区', '选择评论区所在的分区', self.comboBox)
		self.addGroup(FluentIcon.BACKGROUND_FILL, '动态ID', '选择软件的入口脚本', self.lineEdit_1)
		self.addGroup(FluentIcon.BACKGROUND_FILL, '入口脚本', '选择软件的入口脚本', self.lineEdit_2)
		group = self.addGroup(FluentIcon.BACKGROUND_FILL, '入口脚本', '选择软件的入口脚本', self.lineEdit_3)
		group.setSeparatorVisible(True)
		self.vBoxLayout.addLayout(self.bottomLayout)
