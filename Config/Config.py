from qfluentwidgets import QConfig, ConfigItem, BoolValidator, qconfig, Theme

class Config(QConfig):
	enableAcrylicBackgroundCard = ConfigItem('personalGroup', 'enableAcrylicBackgroundCard', True, BoolValidator())
# themeModeCard = ConfigItem('personalGroup', 'themeModeCard', True, BoolValidator())

config = Config()
config.themeMode.value = Theme.DARK
qconfig.load('Config/config.json', config)
