#!/usr/bin/python
from ui import Ui_Dialog
from PyQt5 import QtCore, QtGui, QtWidgets, QtWidgets
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QApplication, QWidget, QShortcut, QLabel, QHBoxLayout
import sys

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	Kalkulacka = QtWidgets.QMainWindow()
	ui = Ui_Dialog()
	ui.setupUi(Kalkulacka)
	Kalkulacka.show()
	sys.exit(app.exec_())