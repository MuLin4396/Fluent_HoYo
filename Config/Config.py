from qfluentwidgets import QConfig, qconfig, Theme

class Config(QConfig):
	pass

config = Config()
config.themeMode.value = Theme.DARK
qconfig.load('Config/config.json', config)
