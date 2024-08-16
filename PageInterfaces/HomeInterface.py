import asyncio
import threading
import time

from PyQt5.QtCore import Qt, QCoreApplication, QDir, pyqtSignal, QThread, QObject
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QWidget
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, InfoBarIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, CommandBarView, FlyoutAnimationType, Flyout, themeColor
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicComboBox, AcrylicToolTipFilter

from Servers.ActionController import ActionController
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

		self.general_Setting.setFixedWidth(500)
		self.display_Card.setFixedWidth(500)
		self.plain_TextEdit.setBorderRadius(8)
		self.general_Setting.setBorderRadius(8)
		self.display_Card.setBorderRadius(8)

		self.horizontalLayout_1.addLayout(self.verticalLayout_1)
		self.horizontalLayout_1.addWidget(self.plain_TextEdit)
		self.horizontalLayout_2.addLayout(self.horizontalLayout_1)
		self.verticalLayout_1.addWidget(self.general_Setting)
		self.verticalLayout_1.addWidget(self.display_Card)
		self.verticalLayout_1.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

class CompileAction(QObject):
	updateTextSignal = pyqtSignal(str)
	toggleButtonSignal = pyqtSignal(bool)

	def __init__(self, plain_TextEdit, general_Setting, action_Controller: ActionController):
		super().__init__()
		self.action_Controller = action_Controller
		self.plain_TextEdit = plain_TextEdit
		self.general_Setting = general_Setting

		self.updateTextSignal.connect(self.performAction)
		self.action_Controller.startSignal.connect(self.startFunction)
		self.action_Controller.pauseSignal.connect(self.pauseFunction)
		self.action_Controller.resumeSignal.connect(self.resumeFunction)
		self.action_Controller.stopSignal.connect(self.stopFunction)
		self.action_Controller.retrySignal.connect(self.retryFunction)

		self._is_paused = False
		self._is_stopped = False
		self.thread = threading.Thread()

	def performAction(self, text):
		self.plain_TextEdit.appendPlainText(text)
		QCoreApplication.processEvents()

	def startFunction(self):
		self.toggleButtonSignal.emit(True)
		self.thread = threading.Thread(target=self.startTask)
		self.thread.start()

	def startTask(self):
		self._is_paused = False
		self._is_stopped = False
		inputID = self.general_Setting.lineEdit_1.text()
		inputRequest = self.general_Setting.lineEdit_2.text()
		inputSave = self.general_Setting.lineEdit_3.text()
		self.updateTextSignal.emit(
				f'✨启动'
				f'\n        动态ID值:{inputID}'
				f'\n        单次请求数:{inputRequest}'
				f'\n        单轮保存数:{inputSave}'
		)
		if bool(inputID) & bool(inputRequest) & bool(inputSave):
			# asyncio.run(spider_main(inputID, inputRequest, inputSave, self.performAction))
			for i in range(1000000):
				if self._is_stopped:
					break
				while self._is_paused:
					time.sleep(0.5)
					pass
				time.sleep(0.1)
				self.updateTextSignal.emit(f'{i}')
		else:
			self.updateTextSignal.emit('F')
		self.toggleButtonSignal.emit(False)

	def pauseFunction(self):
		self._is_paused = True
		self.performAction('✨暂停')

	def resumeFunction(self):
		self._is_paused = False
		self.performAction('✨继续')

	def stopFunction(self):
		self._is_paused = False
		self._is_stopped = True
		if self.thread is not None:
			self.thread.join()
			self.thread = None
		self.performAction('✨终止')

	def retryFunction(self):
		self.stopFunction()
		self.performAction('✨重启')
		self.startFunction()

class TextEdit(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('📄  运 行')

		self.plain_TextEdit = PlainTextEdit(self)

		self.plain_TextEdit.setReadOnly(True)
		self.plain_TextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
		self.plain_TextEdit.customContextMenuRequested.connect(self.showCommandBar)

		self.viewLayout.addWidget(self.plain_TextEdit)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def appendPlainText(self, text):
		self.plain_TextEdit.appendPlainText(text)

	def showCommandBar(self, pos):
		commandBarView = CommandBarView(self)
		commandBarView.addAction(Action(FluentIcon.SHARE, 'Share'))
		commandBarView.addSeparator()
		commandBarView.addAction(Action(FluentIcon.SAVE, 'Save'))
		commandBarView.addAction(Action(FluentIcon.DELETE, 'Delete'))
		commandBarView.addHiddenAction(Action(FluentIcon.APPLICATION, 'App', shortcut='Ctrl+A'))
		commandBarView.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
		commandBarView.resizeToSuitableWidth()
		Flyout.make(commandBarView, self.mapToGlobal(pos), self, FlyoutAnimationType.FADE_IN)

class DisplayCard(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('💖  插 图')

		self.flipView = HorizontalFlipView(self)

		self.flipView.setBorderRadius(4)
		self.flipView.setSpacing(5)
		self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)
		self.flipView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.flipView.customContextMenuRequested.connect(self.showCommandBar)

		self.loadImage(':Images/DisPlay_Png/', '*.png')
		self.loadImage(':Images/DisPlay_Jpg/', '*.jpg')

		self.viewLayout.addWidget(self.flipView)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def loadImage(self, directory, pattern):
		direct = QDir(directory)
		files = direct.entryList([pattern], QDir.Files)
		for filename in files:
			file_path = f'{directory}{filename}'
			pixmap = QPixmap(file_path)
			self.flipView.addImage(pixmap)

	def showCommandBar(self, pos):
		item = self.flipView.itemAt(pos)
		if item is None: return
		# item_rect = self.flipView.visualItemRect(item)
		# global_pos = self.flipView.viewport().mapToGlobal(item_rect.center())
		global_pos = self.flipView.viewport().mapToGlobal(pos)
		commandBarView = CommandBarView(self)
		commandBarView.addAction(Action(FluentIcon.SHARE, 'Share'))
		commandBarView.addSeparator()
		commandBarView.addAction(Action(FluentIcon.SAVE, 'Save'))
		commandBarView.addAction(Action(FluentIcon.DELETE, 'Delete'))
		commandBarView.addHiddenAction(Action(FluentIcon.APPLICATION, 'App', shortcut='Ctrl+A'))
		commandBarView.addHiddenAction(Action(FluentIcon.SETTING, 'Settings', shortcut='Ctrl+S'))
		commandBarView.resizeToSuitableWidth()
		Flyout.make(commandBarView, global_pos, self, FlyoutAnimationType.FADE_IN)

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
		self.comboBox.installEventFilter(AcrylicToolTipFilter(self.comboBox, 0, ToolTipPosition.TOP))
		self.comboBox.addItems(['✨崩坏学园2', '✨崩坏3', '✨原神', '✨未定事件簿', '✨绝区零', '✨大别野'])
		self.comboBox.setCurrentIndex(-1)

		self.action_Controller = ActionController()
		self.compile_Action = CompileAction(parent.plain_TextEdit, self, self.action_Controller)
		self.performAction = self.compile_Action.performAction

		self.menu_Button_1 = AcrylicSystemTrayMenu(self)
		self.menu_Button_2 = AcrylicSystemTrayMenu(self)
		self.action_1_1 = Action("✨It's MyGO!!!!!", triggered=lambda: self.performAction("✨BanG Dream! It's MyGO!!!!!✨"))
		self.action_1_2 = Action('✨高松灯', triggered=lambda: self.performAction('是会虚情假意呢🙄️'))
		self.action_1_3 = Action('✨千早爱音', triggered=lambda: self.performAction('想演奏是你们的自由，你们就请便吧🖐'))
		self.action_1_4 = Action('✨要乐奈', triggered=lambda: self.performAction('到现在都还执着于过去，真难看🙄️'))
		self.action_1_5 = Action('✨长崎爽世', triggered=lambda: self.performAction('你也差不多该忘记了吧😒'))
		self.action_1_6 = Action('✨椎名立希', triggered=lambda: self.performAction('那么那个乐团算什么😅'))
		self.action_2_1 = Action('✨继续', triggered=lambda: self.action_Controller.resume(self.performAction))
		self.action_2_2 = Action('✨停止', triggered=lambda: self.action_Controller.stop(self.performAction))
		self.action_2_3 = Action('✨重试', triggered=lambda: self.action_Controller.retry(self.performAction))
		self.action_2_4 = Action("✨Ave Mujica", triggered=lambda: self.performAction("✨BanG Dream! Ave Mujica✨"))
		self.action_2_5 = Action('✨三角初华', triggered=lambda: self.performAction('是会虚情假意呢🙄️'))
		self.action_2_6 = Action('✨若叶睦', triggered=lambda: self.performAction('想演奏是你们的自由，你们就请便吧🖐'))
		self.action_2_7 = Action('✨八幡海铃', triggered=lambda: self.performAction('到现在都还执着于过去，真难看🙄️'))
		self.action_2_8 = Action('✨祐天寺若麦', triggered=lambda: self.performAction('你也差不多该忘记了吧😒'))
		self.action_2_9 = Action('✨丰川祥子', triggered=lambda: self.performAction('那么那个乐团算什么😅'))
		self.menu_Button_1.addActions([self.action_1_1, self.action_1_2, self.action_1_3, self.action_1_4, self.action_1_5])
		self.menu_Button_2.addActions([self.action_2_1, self.action_2_2, self.action_2_3, self.action_2_4, self.action_2_5, self.action_2_6, self.action_2_7, self.action_2_8, self.action_2_9])

		self.compileButton_Run = PrimarySplitPushButton("✨运行✨")
		self.compileButton_Stop = PrimarySplitPushButton("✨暂停✨")
		self.compileButton_Run.setFlyout(self.menu_Button_1)
		self.compileButton_Stop.setFlyout(self.menu_Button_2)
		self.compileButton_Run.clicked.connect(lambda: self.action_Controller.start(self.performAction))
		self.compileButton_Stop.clicked.connect(lambda: self.action_Controller.pause(self.performAction))

		self.compile_Action.toggleButtonSignal.connect(self.toggleButtonShow)
		self.compileButton_Run.setEnabled(True)
		self.compileButton_Stop.setEnabled(False)

		self.hintIcon = IconWidget(FluentIcon.INFO.icon(color=themeColor()))
		self.hintLabel = BodyLabel('控制运行🤣👉')
		self.hintIcon.setFixedSize(16, 16)

		self.bottomLayout = QHBoxLayout()
		self.bottomLayout.setSpacing(10)
		self.bottomLayout.setContentsMargins(24, 15, 24, 20)
		self.bottomLayout.addWidget(self.hintIcon)
		self.bottomLayout.addWidget(self.hintLabel)
		self.bottomLayout.addStretch(1)
		self.bottomLayout.addWidget(self.compileButton_Run)
		self.bottomLayout.addWidget(self.compileButton_Stop)

		self.addGroup(FluentIcon.PIN, '动态分区', '✨选择动态所在的分区', self.comboBox)
		self.addGroup(FluentIcon.LABEL, '动态 ID 值', '✨输入动态ID值', self.lineEdit_1)
		self.addGroup(FluentIcon.LABEL, '单次请求数', '✨输入单次请求数量', self.lineEdit_2)
		self.addGroup(FluentIcon.LABEL, '单轮保存数', '✨输入单轮保存数', self.lineEdit_3)
		self.groupWidgets[3].setSeparatorVisible(True)
		self.vBoxLayout.addLayout(self.bottomLayout)

	def toggleButtonShow(self, show):
		if show:
			self.compileButton_Run.setEnabled(False)
			self.compileButton_Stop.setEnabled(True)
		else:
			self.compileButton_Run.setEnabled(True)
			self.compileButton_Stop.setEnabled(False)

	def setIntegerValidator(self, line_edit, min_value, max_value):
		validator = QIntValidator(min_value, max_value, self)
		line_edit.setValidator(validator)

		def limitInput():
			text = line_edit.text()
			if text:
				value = int(text)
				if value < min_value:
					line_edit.setText(str(min_value))
				elif value > max_value:
					line_edit.setText(str(max_value))

		line_edit.textChanged.connect(limitInput)
