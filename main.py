import sys
import Images

from PyQt5.QtCore import QSize, QEventLoop, QTimer, QUrl, Qt
from PyQt5.QtGui import QDesktopServices, QIcon
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentWindow, MessageBox, NavigationWidget, SplashScreen, FluentIcon, NavigationItemPosition, Theme, setTheme

from PageInterfaces.CrawlerInterface import CrawlerInterface
from PageInterfaces.TestInterface import TestInterface
from PageInterfaces.HomeInterface import HomeInterface

class MainWindow(FluentWindow):
	def __init__(self):
		super().__init__()
		setTheme(Theme.DARK)

		self.homeInterface = HomeInterface('HomeInterface')
		self.crawlerInterface = CrawlerInterface('CrawlerInterface')
		self.testInterface = TestInterface('TestInterface')
		self.splashScreen = SplashScreen(':Images/DisPlay_Png/HoYo.png', self)

		self.initWindow()
		self.initSplashScreen()
		self.initNavigation()

		self.splashScreen.finish()

	def initWindow(self):
		self.resize(1400, 800)
		self.setMinimumSize(1400, 800)
		self.setWindowTitle('米游社评论区抓取工具')
		self.setWindowIcon(QIcon(':Images/DisPlay_Png/HoYo.png'))

		desktop = QApplication.desktop().availableGeometry()
		width, high = desktop.width(), desktop.height()
		self.move((width - self.width()) // 2, (high - self.height()) // 2)

	def initSplashScreen(self):
		self.splashScreen.setIconSize(QSize(102, 102))
		self.initDelay(100)
		self.show()

	def initNavigation(self):
		self.addSubInterface(self.homeInterface, FluentIcon.HOME, '首页', NavigationItemPosition.TOP)
		self.addSubInterface(self.crawlerInterface, FluentIcon.LABEL, '爬虫', NavigationItemPosition.TOP)
		self.navigationInterface.addSeparator()
		self.addSubInterface(self.testInterface, FluentIcon.BRUSH, '测试', NavigationItemPosition.SCROLL)

		self.initDelay(2000)

	def initDelay(self, time: int):
		loop = QEventLoop(self)
		QTimer.singleShot(time, loop.quit)
		loop.exec()

class HighDpiScaleFactorRoundingPolicy:
	def __init__(self):
		super().__init__()
		QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
		QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
		QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

def main():
	HighDpiScaleFactorRoundingPolicy()
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())

'''
pyinstaller -i .\Images\DisPlay_Png\HoYo.png -w -F .\main.py
name = 'Fluent_HoYo_Window',
pyinstaller  main.spec
'''

if __name__ == '__main__':
	main()
