from PyQt5.QtCore import pyqtSignal, QObject

class ActionController(QObject):
	startSignal = pyqtSignal()
	pauseSignal = pyqtSignal()
	resumeSignal = pyqtSignal()
	stopSignal = pyqtSignal()
	retrySignal = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)

	def start(self, performAction):
		performAction('启动！')
		self.startSignal.emit()

	def pause(self, performAction):
		performAction('暂停')
		self.pauseSignal.emit()

	def resume(self, performAction):
		performAction('继续')
		self.resumeSignal.emit()

	def stop(self, performAction):
		performAction('终止')
		self.stopSignal.emit()

	def retry(self, performAction):
		performAction('重启')
		self.retrySignal.emit()
