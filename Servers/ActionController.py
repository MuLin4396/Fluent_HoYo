from PyQt5.QtCore import pyqtSignal, QObject

class ActionController(QObject):
	startSignal = pyqtSignal()
	pauseSignal = pyqtSignal()
	resumeSignal = pyqtSignal()
	stopSignal = pyqtSignal()
	retrySignal = pyqtSignal()

	def __init__(self, parent=None):
		super().__init__(parent)
		self._is_paused = None
		self._is_stopped = None

	def set_control_events(self, is_paused, is_stopped):
		self._is_paused = is_paused
		self._is_stopped = is_stopped

	def start(self, performAction):
		self._is_paused.clear()
		self._is_stopped.clear()
		self.startSignal.emit()

	def pause(self, performAction):
		self._is_paused.set()
		self.pauseSignal.emit()

	def resume(self, performAction):
		self._is_paused.clear()
		self.resumeSignal.emit()

	def stop(self, performAction):
		self._is_paused.clear()
		self._is_stopped.set()
		self.stopSignal.emit()

	def retry(self, performAction):
		self.retrySignal.emit()
