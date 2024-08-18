from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ExpandLayout, SwitchSettingCard, SettingCardGroup, FluentIcon, OptionsSettingCard, ComboBoxSettingCard, LargeTitleLabel, qconfig, QConfig, ConfigItem, BoolValidator, OptionsConfigItem, OptionsValidator, ConfigSerializer, setTheme, Theme, toggleTheme, isDarkTheme

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
		self.enableAcrylicBackgroundCard = SwitchSettingCard(FluentIcon.TRANSPARENT, '亚克力效果', '使用亚克力效果', configItem=config.enableAcrylicBackgroundCard, parent=self.personalGroup)
		self.themeModeCard = OptionsSettingCard(config.themeMode, FluentIcon.BRUSH, '主题模式', '改变软件的主题模式', texts=['暗色', '亮色', '跟随系统设置'], parent=self.personalGroup)

		self.personalGroup.addSettingCard(self.enableAcrylicBackgroundCard)
		self.personalGroup.addSettingCard(self.themeModeCard)

		self.expandLayout.addWidget(self.personalGroup)

		self.hBoxLayout.addWidget(self.settingLabel)
		self.hBoxLayout.addWidget(self.scrollWidget)

	def __onThemeModo(self, theme=Theme):
		setTheme(Theme.LIGHT)

	def __connectSignalToSlot(self):
		self.enableAcrylicCard.checkedChanged.connect(self.acrylicEnableChanged)
		config.themeChanged.connect(self.__onThemeModo)
