from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from qfluentwidgets import ScrollArea

from PageInterfaces.Card import SampleCard, EmojiCard

class TestInterface(ScrollArea):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.view = QWidget(self)  # 作为 ScrollArea 的 viewport
		self.vBoxLayout = QVBoxLayout(self.view)  # 垂直布局，用于添加卡片
		self.vBoxLayout.setAlignment(Qt.AlignTop)
		self.setWidget(self.view)  # 将 view 设置为 ScrollArea 的子组件
		self.setWidgetResizable(True)  # 使 ScrollArea 可根据内容大小调整

		self.setViewportMargins(0, 160, 0, 5)  # 设置视口边距
		self.enableTransparentBackground()  # 启用透明背景

		card1 = EmojiCard(iconPath=":/qfluentwidgets/images/logo.png", name="PyQt-Fluent-Widgets", )
		card1.clicked.connect(lambda: print("点击卡片"))
		card5 = SampleCard(icon=":/qfluentwidgets/images/logo.png", title="PyQt-Fluent-Widgets", content="Shokokawaii Inc.")
		card5.clicked.connect(lambda: print("点击卡片"))
		self.vBoxLayout.addWidget(card1)  # 添加第一个卡片到布局
		self.vBoxLayout.addWidget(card5)
