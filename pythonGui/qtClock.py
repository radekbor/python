#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import datetime
import math
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class Clock(QWidget):
	def minuteUp(self):
		self.minutesOffset = self.minutesOffset + 1

	def minuteDown(self):
		self.minutesOffset = self.minutesOffset - 1

	def __init__(self):
		QWidget.__init__(self)
		self.text = "init"
		self.initUI()
		self.r = 100
		self.centerY = 110
		self.centerX = 110
		self.minutesOffset = 0

	def tick(self):
		now = datetime.datetime.now()
		hoursOffset = 0
		minutesOffset = 0

		hoursOffset = self.minutesOffset // 60;
		if self.minutesOffset < 0:
			hoursOffset = -(-self.minutesOffset // 60)
		minutesOffset = self.minutesOffset % 60;

		self.hour = now.hour % 12 + hoursOffset
		self.minutes = now.minute + minutesOffset
		self.seconds = now.second
		self.text = "{} {} {}".format(self.hour, self.minutes, self.seconds)
		self.repaint()

	def initUI(self):
		self.setMaximumSize(250, 250)
		self.timer = QTimer()
		self.connect(self.timer, SIGNAL("timeout()"), self.tick)
		self.timer.start(500)  # number is msec

	def getSecondsLine(self):
		p1 = QPoint(110, 110)
		angle = math.radians(self.seconds * 6 - 90)

		X = self.r * math.cos(angle)
		Y = self.r * math.sin(angle)

		p2 = QPoint(self.centerX + X, self.centerY + Y)
		return [p1, p2]

	def getMinutesLine(self):
		p1 = QPoint(110, 110)
		angle = math.radians(self.minutes * 6 - 90)
		X = self.r * 0.75 * math.cos(angle)
		Y = self.r * 0.75 * math.sin(angle)

		p2 = QPoint(self.centerX + X, self.centerY + Y)
		return [p1, p2]

	def getHoursLine(self):
		p1 = QPoint(110, 110)
		angle = math.radians(self.hour * 30 - 90 + self.minutes / 2)
		X = self.r * 0.5 * math.cos(angle)
		Y = self.r * 0.5 * math.sin(angle)

		p2 = QPoint(self.centerX + X, self.centerY + Y)
		return [p1, p2]

	def paintEvent(self, event):
		qp = QPainter()
		qp.begin(self)

		rectangle = QRectF(10.0, 10.0, 210, 210);
		qp.drawEllipse(rectangle);
		pen = QPen(Qt.red, 5, Qt.DashDotLine, Qt.RoundCap, Qt.RoundJoin);
		qp.setPen(pen);
		qp.drawPoint(110, 110)

		# seconds
		pen = QPen(Qt.blue, 1, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		qp.setPen(pen);
		pointsToDrawSeconds = self.getSecondsLine()
		qp.drawLine(pointsToDrawSeconds[0], pointsToDrawSeconds[1])

		# minutes
		pen = QPen(Qt.blue, 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		qp.setPen(pen);
		pointsToDrawMinutes = self.getMinutesLine()
		qp.drawLine(pointsToDrawMinutes[0], pointsToDrawMinutes[1])

		# hours
		pen = QPen(Qt.blue, 4, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin);
		qp.setPen(pen);
		pointsToDrawHours = self.getHoursLine()
		qp.drawLine(pointsToDrawHours[0], pointsToDrawHours[1])

		# self.drawText(event, qp)
		qp.end()

	def drawText(self, event, qp):
		qp.setPen(QColor(168, 34, 3))
		qp.setFont(QFont('Decorative', 10))
		qp.drawText(event.rect(), Qt.AlignCenter, self.text)

class MyWindow(QMainWindow):
	def __init__(self, parent=None):
		super(MyWindow, self).__init__(parent)
		layout = QHBoxLayout()
		self.c = Clock()
		self.setCentralWidget(self.c)
		self.setWindowTitle("Zegarek")
		self.show()
		self.setMaximumSize(250, 250)
		self.setMinimumSize(250, 250)
		self.addMenu()


	def popup(self):
		QMessageBox.about(self, "Okno pomocy", "Witaj uzytkowniku! \nKorzystasz z aplikacji zegarka analogowego, zegarek posiada opcje przewiajania w przod oraz w tyl. \nAby tego dokonac nalezy wybrac opcje 'Minute w przod' lub 'Minute w tyl'.\nOsiagnac moznego tego rowniez poprzez skroty klawiszowe")
	def addMenu(self):
		# Create main menu
		mainMenu = self.menuBar()
		mainMenu.setNativeMenuBar(False)
		fileMenu = mainMenu.addMenu('Menu')

		# Add minute up action
		upButton = QAction('Minute w przod', self)
		upButton.setShortcut('Ctrl+U')
		upButton.setStatusTip('Prestaw zegarek o minute do przodu')
		upButton.triggered.connect(self.minuteUp)
		fileMenu.addAction(upButton)

		# Add minute down action
		downButton = QAction('Minute w tyl', self)
		downButton.setShortcut('Ctrl+J')
		downButton.setStatusTip('Przestaw zegarek o minute do tylu')
		downButton.triggered.connect(self.minuteDown)
		fileMenu.addAction(downButton)

		# Add popup window
		aboutButton = QAction('Pomoc', self)
		aboutButton.setShortcut('Ctrl+A')
		aboutButton.setStatusTip('Okno pomocy')
		aboutButton.triggered.connect(self.popup)
		fileMenu.addAction(aboutButton)


	def minuteUp(self):
		self.c.minuteUp()

	def minuteDown(self):
		self.c.minuteDown()


def main():
	app = QApplication(sys.argv)

	w = MyWindow()
	app.exec_()


if __name__ == '__main__':
	main()
