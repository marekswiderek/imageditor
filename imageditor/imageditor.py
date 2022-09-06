from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np 
from editor.editor import save_ndarray_as_image, convert_pixmap_to_ndarray, convert_ndarray_to_pixmap, rgb_to_grayscale, negative_image, only_red_channel, only_green_channel, only_blue_channel
import traceback

class ProgramWindow(object):
	def __init__(self):
		self.image = None
		self.image_ndarray = None
		self.image_ndarray_backup = None
		self.filters_dict = {'Grayscale': rgb_to_grayscale, 'Negative': negative_image, 'RedOnly': only_red_channel, 'GreenOnly': only_green_channel, 'BlueOnly': only_blue_channel}

	def setupUi(self, MainWindow):
		MainWindow.setObjectName("MainWindow")
		MainWindow.setEnabled(True)
		MainWindow.resize(686, 550)
		MainWindow.setAnimated(True)
		MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
		MainWindow.setDockNestingEnabled(False)
		MainWindow.setUnifiedTitleAndToolBarOnMac(False)
		self.centralWidget = QtWidgets.QWidget(MainWindow)
		self.centralWidget.setEnabled(True)
		self.centralWidget.setObjectName("centralWidget")
		self.imagePreview = QtWidgets.QLabel(self.centralWidget)
		self.imagePreview.setGeometry(QtCore.QRect(10, 10, 530, 530))
		self.imagePreview.setText("")
		#self.imagePreview.setPixmap(QtGui.QPixmap("./test.png"))
		self.imagePreview.setScaledContents(True)
		self.imagePreview.setObjectName("imagePreview")
		self.rgbBox = QtWidgets.QGroupBox(self.centralWidget)
		self.rgbBox.setGeometry(QtCore.QRect(550, 110, 130, 131))
		self.rgbBox.setAccessibleDescription("")
		self.rgbBox.setAutoFillBackground(True)
		self.rgbBox.setFlat(True)
		self.rgbBox.setCheckable(False)
		self.rgbBox.setObjectName("rgbBox")
		self.rBox = QtWidgets.QSpinBox(self.rgbBox)
		self.rBox.setGeometry(QtCore.QRect(10, 20, 52, 22))
		self.rBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.rBox.setMaximum(255)
		self.rBox.setObjectName("rBox")
		self.gBox = QtWidgets.QSpinBox(self.rgbBox)
		self.gBox.setGeometry(QtCore.QRect(10, 40, 52, 22))
		self.gBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.gBox.setMaximum(255)
		self.gBox.setObjectName("gBox")
		self.bBox = QtWidgets.QSpinBox(self.rgbBox)
		self.bBox.setGeometry(QtCore.QRect(10, 60, 52, 22))
		self.bBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.UpDownArrows)
		self.bBox.setMaximum(255)
		self.bBox.setObjectName("bBox")
		self.rLabel = QtWidgets.QLabel(self.rgbBox)
		self.rLabel.setGeometry(QtCore.QRect(70, 20, 47, 22))
		self.rLabel.setObjectName("rLabel")
		self.gLabel = QtWidgets.QLabel(self.rgbBox)
		self.gLabel.setGeometry(QtCore.QRect(70, 40, 47, 22))
		self.gLabel.setObjectName("gLabel")
		self.bLabel = QtWidgets.QLabel(self.rgbBox)
		self.bLabel.setGeometry(QtCore.QRect(70, 60, 47, 22))
		self.bLabel.setObjectName("bLabel")
		self.manipulateButton = QtWidgets.QPushButton(self.rgbBox)
		self.manipulateButton.setGeometry(QtCore.QRect(10, 90, 75, 23))
		self.manipulateButton.setObjectName("manipulateButton")
		self.navBox = QtWidgets.QGroupBox(self.centralWidget)
		self.navBox.setGeometry(QtCore.QRect(550, 10, 130, 101))
		self.navBox.setAutoFillBackground(True)
		self.navBox.setFlat(True)
		self.navBox.setObjectName("navBox")
		self.loadImageButton = QtWidgets.QPushButton(self.navBox)
		self.loadImageButton.setGeometry(QtCore.QRect(0, 20, 118, 41))
		self.loadImageButton.setObjectName("loadImageButton")
		self.saveImageButton = QtWidgets.QPushButton(self.navBox)
		self.saveImageButton.setGeometry(QtCore.QRect(0, 60, 118, 41))
		self.saveImageButton.setObjectName("saveImageButton")
		self.filterBox = QtWidgets.QGroupBox(self.centralWidget)
		self.filterBox.setGeometry(QtCore.QRect(550, 250, 130, 81))
		self.filterBox.setAutoFillBackground(True)
		self.filterBox.setFlat(True)
		self.filterBox.setObjectName("filterBox")
		self.filterComboBox = QtWidgets.QComboBox(self.filterBox)
		self.filterComboBox.clear()
		self.filterComboBox.addItems(self.filters_dict.keys())
		self.filterComboBox.setGeometry(QtCore.QRect(10, 20, 111, 22))
		self.filterComboBox.setObjectName("filterComboBox")
		self.filterButton = QtWidgets.QPushButton(self.filterBox)
		self.filterButton.setGeometry(QtCore.QRect(10, 50, 111, 23))
		self.filterButton.setObjectName("filterButton")
		MainWindow.setCentralWidget(self.centralWidget)
		self.statusbar = QtWidgets.QStatusBar(MainWindow)
		self.statusbar.setEnabled(False)
		self.statusbar.setObjectName("statusbar")
		MainWindow.setStatusBar(self.statusbar)
		
		self.resetBox = QtWidgets.QGroupBox(self.centralWidget)
		self.resetBox.setGeometry(QtCore.QRect(550, 330, 130, 40))
		self.resetBox.setAutoFillBackground(True)
		self.resetBox.setFlat(True)
		self.resetButton = QtWidgets.QPushButton(self.resetBox)
		self.resetButton.setGeometry(QtCore.QRect(10,10,111,23))
		self.resetButton.setObjectName("resetButton")
		
		self.retranslateUi(MainWindow)
		QtCore.QMetaObject.connectSlotsByName(MainWindow)
		
		#map functions to buttons on-click
		self.loadImageButton.clicked.connect(self.load_image)
		self.saveImageButton.clicked.connect(self.save_image)
		self.filterButton.clicked.connect(self.add_filter)
		self.resetButton.clicked.connect(self.reset_image)
		
	def retranslateUi(self, MainWindow):
		_translate = QtCore.QCoreApplication.translate
		MainWindow.setWindowTitle(_translate("MainWindow", "Imageditor"))
		self.rgbBox.setTitle(_translate("MainWindow", "RGB manipulation"))
		self.rLabel.setText(_translate("MainWindow", "R"))
		self.gLabel.setText(_translate("MainWindow", "G"))
		self.bLabel.setText(_translate("MainWindow", "B"))
		self.manipulateButton.setText(_translate("MainWindow", "Manipulate"))
		self.navBox.setTitle(_translate("MainWindow", "Navigation"))
		self.loadImageButton.setText(_translate("MainWindow", "Load image"))
		self.saveImageButton.setText(_translate("MainWindow", "Save image"))
		self.filterBox.setTitle(_translate("MainWindow", "Filters"))
		self.filterButton.setText(_translate("MainWindow", "Add filter"))
		self.resetButton.setText(_translate("MainWindow", "RESET"))

	def load_image(self):
		#show choose file dialog window and load image
		try:
			image_path = QtWidgets.QFileDialog.getOpenFileName()
			self.image = QtGui.QPixmap(image_path[0])
			self.imagePreview.setPixmap(self.image)
			#image variable for editing, image_backup variable for "reset" feature
			self.image_ndarray = self.image_ndarray_backup =  convert_pixmap_to_ndarray(self.image)
		except Exception:
			traceback.print_exc()
			
	def save_image(self):
		try:
			image_path = QtWidgets.QFileDialog.getSaveFileName()[0]
			save_ndarray_as_image(self.image_ndarray, image_path)
		except Exception:
			traceback.print_exc()

	def reload_image(self):
		self.image = convert_ndarray_to_pixmap(self.image_ndarray)
		self.imagePreview.setPixmap(QtGui.QPixmap(self.image))
	
	def add_filter(self):
		self.image_ndarray = self.filters_dict[str(self.filterComboBox.currentText())](self.image_ndarray)
		self.reload_image()

	def reset_image(self):
		self.image_ndarray = self.image_ndarray_backup.copy()
		self.reload_image()
	
if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	MainWindow = QtWidgets.QMainWindow()
	ProgramWindow = ProgramWindow()
	ProgramWindow.setupUi(MainWindow)
	MainWindow.show()
	
	sys.exit(app.exec_())


