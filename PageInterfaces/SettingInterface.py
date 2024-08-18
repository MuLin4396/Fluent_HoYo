from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout
from qfluentwidgets import ExpandLayout, SettingCardGroup, FluentIcon, OptionsSettingCard, LargeTitleLabel, setTheme, CustomColorSettingCard, setThemeColor
from Config.Config import config

class SettingInterface(QFrame):
	def __init__(self, text: str):
		super().__init__()
		self.setObjectName(text)

		self.hBoxLayout = QVBoxLayout(self)
		self.scrollWidget = QWidget()
		self.expandLayout = ExpandLayout(self.scrollWidget)
		self.settingLabel = LargeTitleLabel(text)

		self.personalGroup = SettingCardGroup('个性化', self.scrollWidget)
		self.themeCard = OptionsSettingCard(config.themeMode, FluentIcon.BRUSH, '主题模式', '改变主题模式', texts=['亮色', '深色', '跟随系统设置'])
		self.themeColorCard = CustomColorSettingCard(config.themeColor, FluentIcon.PALETTE, '主题颜色', '改变主题颜色')

		self.personalGroup.addSettingCard(self.themeCard)
		self.personalGroup.addSettingCard(self.themeColorCard)
		self.expandLayout.addWidget(self.personalGroup)
		self.hBoxLayout.addWidget(self.settingLabel)
		self.hBoxLayout.addWidget(self.scrollWidget)

		self.__connectSignalToSlot()

	def __connectSignalToSlot(self):
		self.themeCard.optionChanged.connect(lambda ci: setTheme(config.get(ci)))
		self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))
