import asyncio
import threading

from PyQt5.QtCore import Qt, QCoreApplication, QDir, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap, QIntValidator
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from qfluentwidgets import PlainTextEdit, BodyLabel, GroupHeaderCardWidget, FluentIcon, IconWidget, LineEdit, HeaderCardWidget, HorizontalFlipView, PrimarySplitPushButton, ToolTipPosition, Action, CommandBarView, FlyoutAnimationType, Flyout, themeColor, LargeTitleLabel, SpinBox
from qfluentwidgets.components.material import AcrylicSystemTrayMenu, AcrylicToolTipFilter, AcrylicEditableComboBox

from Servers.ActionController import ActionController
from Servers.CrawlingHoYo import spider_main

class CrawlerInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.label = LargeTitleLabel(text)
		self.plain_TextEdit = TextEdit(self)
		self.general_Setting = GeneralSetting(self)
		self.hBoxLayout_1 = QHBoxLayout()
		self.hBoxLayout_2 = QHBoxLayout(self)
		self.vBoxLayout_1 = QVBoxLayout()

		self.general_Setting.setFixedWidth(500)
		self.plain_TextEdit.setBorderRadius(8)
		self.general_Setting.setBorderRadius(8)

		self.hBoxLayout_1.addLayout(self.vBoxLayout_1)
		self.hBoxLayout_1.addWidget(self.plain_TextEdit)
		self.hBoxLayout_2.addLayout(self.hBoxLayout_1)
		self.vBoxLayout_1.addWidget(self.label)
		self.vBoxLayout_1.addWidget(self.general_Setting)
		self.vBoxLayout_1.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

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

		self._is_paused = threading.Event()
		self._is_stopped = threading.Event()
		self.action_Controller.set_control_events(self._is_paused, self._is_stopped)
		self.thread = threading.Thread()

	def performAction(self, text):
		self.plain_TextEdit.appendPlainText(text)
		QCoreApplication.processEvents()

	def startFunction(self):
		self._is_paused.clear()
		self._is_stopped.clear()
		self.toggleButtonSignal.emit(True)
		self.thread = threading.Thread(target=self.startTask)
		self.thread.start()

	def startTask(self):
		inputName = self.general_Setting.comboBox.text()
		inputID = self.general_Setting.lineEdit.text()
		inputRequest = self.general_Setting.spinBox_1.text()
		inputSave = self.general_Setting.spinBox_2.text()
		self.updateTextSignal.emit(f'✨启动\n\t命名:{inputName}\n\t动态ID值:{inputID}\n\t单次请求数:{inputRequest}\n\t单轮保存数:{inputSave}K')
		if bool(inputName) & bool(inputID) & bool(inputRequest) & bool(inputSave):
			asyncio.run(spider_main(self.action_Controller, inputName, inputID, inputRequest, int(inputSave) * 1000, self.performAction))
		else:
			self.updateTextSignal.emit('F')
		self.toggleButtonSignal.emit(False)

	def pauseFunction(self):
		self._is_paused.set()
		self.performAction('✨暂停')

	def resumeFunction(self):
		self._is_paused.clear()
		self.performAction('✨继续')

	def stopFunction(self):
		self._is_paused.clear()
		self._is_stopped.set()
		if self.thread is not None and self.thread.is_alive():
			self.thread.join()
		self.thread = None
		self.performAction('✨终止')

	def retryFunction(self):
		self.performAction('✨重启')
		self.stopFunction()
		self.startFunction()

class TextEdit(HeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('📄  运 行')

		self.plain_TextEdit = PlainTextEdit(self)
		self.scrollbar = self.plain_TextEdit.verticalScrollBar()

		self.plain_TextEdit.setReadOnly(True)
		self.plain_TextEdit.setContextMenuPolicy(Qt.CustomContextMenu)
		self.plain_TextEdit.customContextMenuRequested.connect(self.showCommandBar)

		self.viewLayout.addWidget(self.plain_TextEdit)
		self.viewLayout.setContentsMargins(10, 5, 10, 10)

	def appendPlainText(self, text):
		self.plain_TextEdit.appendPlainText(text)
		self.scrollbar.setValue(self.scrollbar.maximum())

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

class GeneralSetting(GroupHeaderCardWidget):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setTitle('⚙️  配 置')

		self.comboBox = AcrylicEditableComboBox(self)
		self.lineEdit = LineEdit(self)
		self.spinBox_1 = SpinBox(self)
		self.spinBox_2 = SpinBox(self)

		self.comboBox.setFixedWidth(200)
		self.comboBox.setPlaceholderText('✨选择分区不生效')
		self.comboBox.setToolTip("✨BanG Dream! It's MyGO!!!!!✨")
		self.comboBox.installEventFilter(AcrylicToolTipFilter(self.comboBox, 0, ToolTipPosition.TOP))
		self.comboBox.addItems(['✨崩坏学园2', '✨崩坏3', '✨原神', '✨未定事件簿', '✨绝区零', '✨大别野'])
		self.comboBox.setCurrentIndex(-1)

		self.lineEdit.setFixedWidth(200)
		self.lineEdit.setPlaceholderText('✨输入评论区ID')
		self.lineEdit.setValidator(QIntValidator())

		self.spinBox_1.setFixedWidth(200)
		self.spinBox_1.setRange(1, 50)
		self.spinBox_1.setValue(30)

		self.spinBox_2.setFixedWidth(200)
		self.spinBox_2.setRange(1, 100)
		self.spinBox_2.setValue(10)

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
		self.action_2_2 = Action('✨终止', triggered=lambda: self.action_Controller.stop(self.performAction))
		self.action_2_3 = Action('✨重试', triggered=lambda: self.action_Controller.retry(self.performAction))
		self.action_2_4 = Action('✨Ave Mujica', triggered=lambda: self.performAction('✨BanG Dream! Ave Mujica✨'))
		self.action_2_5 = Action('✨三角初华', triggered=lambda: self.performAction('是会虚情假意呢🙄️'))
		self.action_2_6 = Action('✨若叶睦', triggered=lambda: self.performAction('想演奏是你们的自由，你们就请便吧🖐'))
		self.action_2_7 = Action('✨八幡海铃', triggered=lambda: self.performAction('到现在都还执着于过去，真难看🙄️'))
		self.action_2_8 = Action('✨祐天寺若麦', triggered=lambda: self.performAction('你也差不多该忘记了吧😒'))
		self.action_2_9 = Action('✨丰川祥子', triggered=lambda: self.performAction('那么那个乐团算什么😅'))
		self.menu_Button_1.addActions([self.action_1_1, self.action_1_2, self.action_1_3, self.action_1_4, self.action_1_5])
		self.menu_Button_2.addActions([self.action_2_1, self.action_2_2, self.action_2_3, self.action_2_4, self.action_2_5, self.action_2_6, self.action_2_7, self.action_2_8, self.action_2_9])

		self.compileButton_Run = PrimarySplitPushButton('✨运行✨')
		self.compileButton_Stop = PrimarySplitPushButton('✨暂停✨')
		self.compileButton_Run.setFlyout(self.menu_Button_1)
		self.compileButton_Stop.setFlyout(self.menu_Button_2)
		self.compileButton_Run.clicked.connect(lambda: self.action_Controller.start(self.performAction))
		self.compileButton_Stop.clicked.connect(lambda: self.action_Controller.pause(self.performAction))

		self.compile_Action.toggleButtonSignal.connect(self.toggleButtonShow)
		self.compileButton_Run.setEnabled(True)
		self.compileButton_Stop.setEnabled(False)

		self.hintIcon = IconWidget(FluentIcon.INFO)
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

		self.addGroup(FluentIcon.PIN, '文件命名', '✨选择或输入文件名', self.comboBox)
		self.addGroup(FluentIcon.LABEL, '动态 ID 值', '✨输入动态ID值', self.lineEdit)
		self.addGroup(FluentIcon.LABEL, '单次请求数', '✨输入单次请求数量', self.spinBox_1)
		self.addGroup(FluentIcon.LABEL, '单轮保存数', '✨输入单轮保存数，以K为单位', self.spinBox_2)
		self.groupWidgets[3].setSeparatorVisible(True)
		self.vBoxLayout.addLayout(self.bottomLayout)

	def toggleButtonShow(self, show):
		if show:
			self.compileButton_Run.setEnabled(False)
			self.compileButton_Stop.setEnabled(True)
		else:
			self.compileButton_Run.setEnabled(True)
			self.compileButton_Stop.setEnabled(False)
