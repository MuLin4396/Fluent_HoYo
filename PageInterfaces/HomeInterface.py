from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QVBoxLayout
from qfluentwidgets import FlowLayout, ScrollArea

from PageInterfaces.Card import SampleCard, EmojiCard

class HomeInterface(ScrollArea):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.view = QWidget(self)
		self.vBoxLayout = QVBoxLayout(self.view)

		self.hBoxLayout = QHBoxLayout()
		self.flowLayout = FlowLayout()

		self.vBoxLayout.addLayout(self.hBoxLayout)
		self.vBoxLayout.addLayout(self.flowLayout)

		self.setWidget(self.view)
		self.setWidgetResizable(True)

		self.setViewportMargins(0, 300, 0, 0)
		self.enableTransparentBackground()

		self.initEmojiCard()
		self.initSampleCard()

	def initEmojiCard(self):
		card1 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card2 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card3 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card4 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card5 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card6 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		card7 = EmojiCard(':/qfluentwidgets/images/logo.png', 'PyQt-Fluent-Widgets', 'https://www.miyoushe.com/sr/')
		self.hBoxLayout.addWidget(card1)
		self.hBoxLayout.addWidget(card2)
		self.hBoxLayout.addWidget(card3)
		self.hBoxLayout.addWidget(card4)
		self.hBoxLayout.addWidget(card5)
		self.hBoxLayout.addWidget(card6)
		self.hBoxLayout.addWidget(card7)

	def initSampleCard(self):
		card1 = SampleCard(
				':/qfluentwidgets/images/logo.png',
				'PyQt-Fluent-Widgets',
				'Shokokawaii Inc.',
				'https://www.miyoushe.com/sr/'
		)

		self.flowLayout.addWidget(card1)
