from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout
from qfluentwidgets import ElevatedCardWidget, IconWidget, BodyLabel, CaptionLabel, PushButton, TransparentToolButton, FluentIcon, ImageLabel

class SampleCard(ElevatedCardWidget):

	def __init__(self, icon, title, content, parent=None):
		super().__init__(parent)
		self.iconWidget = IconWidget(icon)
		self.titleLabel = BodyLabel(title, self)
		self.contentLabel = CaptionLabel(content, self)

		self.hBoxLayout = QHBoxLayout(self)
		self.vBoxLayout = QVBoxLayout()

		self.setFixedSize(360, 90)
		self.iconWidget.setFixedSize(48, 48)
		self.contentLabel.setTextColor("#606060", "#d2d2d2")

		self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
		self.hBoxLayout.setSpacing(15)
		self.hBoxLayout.addWidget(self.iconWidget)

		self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
		self.vBoxLayout.setSpacing(0)
		self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
		self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
		self.vBoxLayout.setAlignment(Qt.AlignVCenter)
		self.hBoxLayout.addLayout(self.vBoxLayout)

class EmojiCard(ElevatedCardWidget):

	def __init__(self, iconPath: str, name: str, parent=None):
		super().__init__(parent)
		self.iconWidget = ImageLabel(iconPath, self)
		self.label = CaptionLabel(name, self)

		self.iconWidget.scaledToHeight(68)

		self.vBoxLayout = QVBoxLayout(self)
		self.vBoxLayout.setAlignment(Qt.AlignCenter)
		self.vBoxLayout.addStretch(1)
		self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
		self.vBoxLayout.addStretch(1)
		self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

		self.setFixedSize(168, 176)
