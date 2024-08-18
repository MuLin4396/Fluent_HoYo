from qfluentwidgets import QConfig, ConfigItem, BoolValidator, qconfig

class Config(QConfig):
	enableAcrylicBackgroundCard = ConfigItem('personalGroup', 'enableAcrylicBackgroundCard', True, BoolValidator())
# themeModeCard = ConfigItem('personalGroup', 'themeModeCard', True, BoolValidator())

config = Config()
qconfig.load('Config/config.json', config)
