from PyQt5.QtWidgets import QFrame

class SettingInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)