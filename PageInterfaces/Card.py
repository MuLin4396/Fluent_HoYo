from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget
from future import StyleSheet
from qfluentwidgets import ElevatedCardWidget, FlowLayout, IconWidget, BodyLabel, CaptionLabel, PushButton, TransparentToolButton, FluentIcon, ImageLabel

class SampleCard(ElevatedCardWidget):

	def __init__(self, icon, title, content, url, parent=None):
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

		self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))

class SampleCardView(QWidget):
	def __init__(self, title: str, parent=None):
		super().__init__(parent=parent)
		self.titleLabel = QLabel(title, self)
		self.vBoxLayout = QVBoxLayout(self)
		self.flowLayout = FlowLayout()

		self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
		self.vBoxLayout.setSpacing(10)
		self.flowLayout.setContentsMargins(0, 0, 0, 0)
		self.flowLayout.setHorizontalSpacing(12)
		self.flowLayout.setVerticalSpacing(12)

		self.vBoxLayout.addWidget(self.titleLabel)
		self.vBoxLayout.addLayout(self.flowLayout, 1)

		self.titleLabel.setObjectName('viewTitleLabel')
		StyleSheet.SAMPLE_CARD.apply(self)

	def addSampleCard(self, icon, title, content, url):
		card = SampleCard(icon, title, content, url, self)
		self.flowLayout.addWidget(card)

class EmojiCard(ElevatedCardWidget):

	def __init__(self, icon, title, url, parent=None):
		super().__init__(parent)
		self.iconWidget = ImageLabel(icon, self)
		self.label = CaptionLabel(title, self)

		self.iconWidget.scaledToHeight(68)

		self.vBoxLayout = QVBoxLayout(self)
		self.vBoxLayout.setAlignment(Qt.AlignCenter)
		self.vBoxLayout.addStretch(1)
		self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
		self.vBoxLayout.addStretch(1)
		self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)

		# self.setFixedSize(168, 176)
		self.setFixedHeight(180)

		self.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
