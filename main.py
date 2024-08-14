import sys
import Images

from PyQt5.QtCore import QSize, QEventLoop, QTimer, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import MSFluentWindow, setTheme, Theme, SplashScreen, FluentIcon, NavigationItemPosition

from PageInterfaces.HomeInterface import HomeInterface
from PageInterfaces.SettingInterface import SettingInterface

class MainWindow(MSFluentWindow):
	def __init__(self):
		super().__init__()
		self.initWindow()

	# 主界面
	def initWindow(self):
		# 主界面配置
		setTheme(Theme.DARK)
		self.resize(1400, 800)
		self.setMinimumWidth(1400)
		self.setMinimumHeight(800)
		self.setWindowTitle('米游社评论区抓取工具')
		self.setWindowIcon(QIcon(":Images/DisPlay_Png/HoYo.png"))
		# 居中界面
		desktop = QApplication.desktop().availableGeometry()
		width, high = desktop.width(), desktop.height()
		self.move((width - self.width()) // 2, (high - self.height()) // 2)
		# 加载启动界面
		self.initSplashScreen()

	# 启动界面
	def initSplashScreen(self):
		# 启动界面配置
		self.splashScreen = SplashScreen(self.windowIcon(), self)
		self.splashScreen.setIconSize(QSize(102, 102))
		# 100ms延时
		self.initDelay(100)
		# 加载侧边栏&关闭启动界面
		self.show()
		self.initNavigation()
		self.splashScreen.finish()

	# 侧边栏
	def initNavigation(self):
		# 加载子界面
		self.initPageInterface()
		# 侧边栏配置
		self.addSubInterface(self.homeInterface, FluentIcon.HOME, '首页', FluentIcon.HOME_FILL, NavigationItemPosition.TOP)
		self.addSubInterface(self.settingInterface, FluentIcon.SETTING, '设置', FluentIcon.SETTING, NavigationItemPosition.BOTTOM)
		# 1000ms延时
		self.initDelay(2000)

	# 子界面
	def initPageInterface(self):
		# 加载子界面
		self.homeInterface = HomeInterface('HomeInterface')
		self.settingInterface = SettingInterface('SettingInterface')

	# 延时
	def initDelay(self, time: int):
		loop = QEventLoop(self)
		QTimer.singleShot(time, loop.quit)
		loop.exec()

class HighDpiScaleFactorRoundingPolicy:
	def __init__(self):
		super().__init__()
		# 自适应分辨率
		QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
		QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

def main():
	# 主函数
	HighDpiScaleFactorRoundingPolicy()
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

# pyinstaller -i .\Images\DisPlay_Png\HoYo.png -w -F .\main.py
# name = 'Fluent_HoYo_Window',
# pyinstaller  main.spec

if __name__ == '__main__':
	main()
