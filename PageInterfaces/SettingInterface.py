from PyQt5.QtWidgets import QFrame, QWidget, QLabel, QHBoxLayout, QVBoxLayout
from qfluentwidgets import ExpandLayout, SwitchSettingCard, SettingCardGroup, FluentIcon, OptionsSettingCard, ComboBoxSettingCard, LargeTitleLabel, qconfig, QConfig, ConfigItem, BoolValidator, OptionsConfigItem, OptionsValidator, ConfigSerializer, setTheme, Theme, toggleTheme, isDarkTheme, CustomColorSettingCard

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
		# self.themeModeCard = OptionsSettingCard(config.themeMode, FluentIcon.BRUSH, '主题模式', '改变软件的主题模式', texts=['暗色', '亮色', '跟随系统设置'], parent=self.personalGroup)
		self.themeCard = OptionsSettingCard(
				config.themeMode,
				FluentIcon.BRUSH,
				self.tr('Application theme'),
				self.tr("Change the appearance of your application"),
				texts=[
					self.tr('Light'), self.tr('Dark'),
					self.tr('Use system setting')
				],
				parent=self.personalGroup
		)
		self.themeColorCard = CustomColorSettingCard(
				config.themeColor,
				FluentIcon.PALETTE,
				self.tr('Theme color'),
				self.tr('Change the theme color of you application'),
				self.personalGroup
		)


		self.personalGroup.addSettingCard(self.enableAcrylicBackgroundCard)
		# self.personalGroup.addSettingCard(self.themeModeCard)
		self.personalGroup.addSettingCard(self.themeCard)
		self.personalGroup.addSettingCard(self.themeColorCard)

		self.expandLayout.addWidget(self.personalGroup)

		self.hBoxLayout.addWidget(self.settingLabel)
		self.hBoxLayout.addWidget(self.scrollWidget)

		self.__connectSignalToSlot()

	def __onThemeModo(self, theme=Theme):
		setTheme(Theme.LIGHT)

	def __connectSignalToSlot(self):
		# self.enableAcrylicCard.checkedChanged.connect(self.acrylicEnableChanged)

		self.themeCard.optionChanged.connect(lambda ci: setTheme(config.get(ci)))
		# self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

		config.themeChanged.connect(self.__onThemeModo)
