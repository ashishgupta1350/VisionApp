import sys
import webbrowser

try:
    import urllib.request
    import numpy as np
except:
    print('Install urllib and numpy to use mobile cam else it will now work')

try:
    import cv2
except:
    print('Please install OpenCV first to run this!')
    exit(1)

try:
    from PyQt5 import QtCore
    from PyQt5 import uic
    from PyQt5.QtCore import pyqtSlot, QTimer
    from PyQt5.QtGui import QImage, QPixmap, QIcon
    from PyQt5.QtWidgets import QFileDialog, QApplication, QMessageBox, QAction, QMainWindow, QLineEdit, QPushButton, \
    QInputDialog, QWidget, QFormLayout, QTextBrowser
except:
    print("Please install PyQt5 first to run the interface!")
    exit(1)

try:
    import matplotlib.pyplot as plt
except:
    print('Please install matplotlib, some features like [Histograms] will not work')


# -- Decorators -- #
# This code uses decorators to import class functions. To add any function filled file, just add ( +
# file_name.functions) in it. for that, we need 1) import the file 2) In file, add functions as a variable and
# functions = ( function_names, .., .., ..), 3) add to below lib function! End:)

import lib
import morphologicalTransforms
import encryptionCode
import paintCode
import ImageProcessingFilters
import cameraCode
import cornerDetection


# Global Variables for multi window code
IPCamURL = ''
IPCamFlag = False
codeString = '<b> No code selected yet </b>' \
             '\n'


class textEditor(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        uic.loadUi(r'assets/textEditor.ui', self)
        self.initializeButtons()
        self.setWindowTitle('<Code>')
        self.show()
        self.textBrowser.setText(codeString)
        self.textBrowser.setAcceptRichText(True)
        qtb = QTextBrowser()
        qtb.setAcceptRichText(True)
        qtb.setText(codeString)


    def initializeButtons(self):
        self.okButton.clicked.connect(self.okButtonClicked)

    def okButtonClicked(self):
        self.close()

class IPCamDialog(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.label1 = QLineEdit('http://192.168.12.160:8080', self)
        self.label1.move(10, 50)
        self.label1.setFixedWidth(230)
        # btn1 = QPushButton("Button 1", self)
        # btn1.move(30, 50)

        self.btn2 = QPushButton("OK", self)
        self.btn2.move(250, 50)

        self.btn2.clicked.connect(self.buttonClicked)

        self.statusBar()

        self.setGeometry(300, 300, 360, 100)
        self.setWindowTitle('Set IP for IPCAM')
        self.show()

    def buttonClicked(self):
        global IPCamURL
        IPCamURL = str(self.label1.text()) # get the url from the source!
        print('Debug -- in class')
        IPCamURL = IPCamURL + '/shot.jpg'
        IPCamFlag = True
        print(IPCamURL)
        cv2.destroyAllWindows()
        self.close()



@lib.add_functions_as_methods(
    morphologicalTransforms.functions
    + encryptionCode.functions
    + paintCode.functions
    + ImageProcessingFilters.functions
    + cameraCode.functions
    + cornerDetection.functions)

class gui(QMainWindow):
    def __init__(self):
        super(gui,self).__init__()
        print("Welcome to Photoshop.\n You can encrpyt, decrypt data to images.\n You can apply filters to images.\n"
              "Advanced cut edge algorithms are applied in a snap. \n Video filters can be applied in real time without"
              "writing the code! The code can be ported with any python application to produce a real time application!"
              ".")
        uic.loadUi(r'assets/photoshopDesignUI',self)
        self.initializePaint()
        self.cap = None
        self.globalDrawing = False
        self.processedImage = cv2.imread(r'images/img22.jpg')
        self.originalImage = cv2.imread(r'images/img22.jpg')
        self.displayImage(2)
        self.filterFlag = int(1) # imp
        self.initializeSlider()
        self.colorContainer = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0),
                               (255, 255, 255), (100, 100, 100), (100, 100, 255), (100, 255, 100), (255, 100, 0),
                               (0, 100, 200)]
        # For displaying code
        self.codeString = codeString
        self.mainCodeHelper() # to load main code.py to getCode()

        # IP cam code
        self.ipCamURL = 'http://192.168.1.5:8080/shot.jpg'
        self.nd = 0 # The button clicked on gui ( bad name )
        self.ipCamIpButton.clicked.connect(self.loadVideoFromMobile)
        self.mobileCamButton.clicked.connect(self.loadVideoFromMobile)

        # Load Save and Reset Buttons
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        self.resetButton.clicked.connect(self.saveClicked)

        # Update original image( V Important)
        self.updateOriginal.clicked.connect(self.updateOriginalImage)

        # Filters, thresholds, image processing QCombo box
        self.filters.activated.connect(self.applyFilter)
        self.thresholds.activated.connect(self.applyThresholds)
        self.imageProcessingQComboBox.activated.connect(self.applyImageProcessing)

        # About and instructions buttons
        self.aboutButton.clicked.connect(self.aboutClicked)
        self.instructionButton.clicked.connect(self.instructionClicked)

        self.slider.valueChanged.connect(self.sliderClicked)
        self.lineEditSliderValue.returnPressed.connect(self.lineEditSliderValueClicked)
        self.mainMenuClicked()

        # Camera Buttons
        self.camButtonStart.clicked.connect(self.camButtonStartClicked)
        self.camButtonStop.clicked.connect(self.camButtonStopClicked)

        # Paint Buttons
        self.paintButtonStart.clicked.connect(self.paintButtonStartClicked)
        self.paintButtonStop.clicked.connect(self.paintButtonStopClicked)

        # image encryption and watermark
        self.watermarkImage.clicked.connect(self.waterMarkImageClicked)
        self.encryptData.clicked.connect(self.encryptDataClicked)
        self.decryptData.clicked.connect(self.decryptDataClicked)
        self.checkWatermarkButton.clicked.connect(self.checkWatermark)


        # THIS IS LITERALLY ONE LINE CODE TO CALL GAME
        # play button
        self.playButton.clicked.connect(self.playButtonClicked)

        # Video Load button
        self.loadVideoButton.clicked.connect(self.loadVideoButtonClicked)
        self.stopVideoButton.clicked.connect(self.stopVideoButtonClicked)
        self.stopVideo = False

        # corner Detection buttons

        # Depricated code
        self.cornerDetectionQComboBox.activated.connect(self.applyCornerDetection)

        # getCode
        self.getCodeButton.clicked.connect(self.getCodeButtonClicked)

        # Paint 2 initialzied

        self.backupImage = None
        self.img = None
        self.prevX = None
        self.prevY = None
        self.localMouseDown = False

        self.paint2Button.clicked.connect(self.paintButtonClicked)

    def getCodeButtonClicked(self):
        codeEditor = textEditor(self)
        codeEditor.show()