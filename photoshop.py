# --import dependencies for the project

import sys
import webbrowser

try:
    import urllib.request
    import numpy as np
except:
    print('Install urllib and numpy to use mobile cam else it will now work')

# --Opencv
try:
    import cv2
except:
    print('Please install OpenCV first to run this!')
    exit(1)

# --Pyqt
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

# -- additional dependencies
try:
    import matplotlib.pyplot as plt
except:
    print('Please install matplotlib, some features like [Histograms] will not work')


# -- Decorators -- #

class gui(QMainWindow):
    # init class
    def __init__(self):
        super(gui, self).__init__()
        print(
            'Welcome to Mini Photoshop. This Gui is designed to edit photos. You can apply filters, detect faces and '
            'eyes in image, encrypt the data in the image and a lot more!\n\n\n')
        uic.loadUi(r'assets/miniPhotoshopDesignMainWindow_Paint.ui', self)

        self.initializePaint()
        self.cap = None
        self.globalDrawing = False
        self.processedImage = cv2.imread(r'images/img22.jpg')
        self.originalImage = cv2.imread(r'images/img22.jpg')
        self.displayImage(2)
        self.filterFlag = int(1)
        self.lastFilter = 'No Filter Used'
        self.initializeSlider()
        self.colorContainer = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255), (255, 255, 0),
                               (255, 255, 255), (100, 100, 100), (100, 100, 255), (100, 255, 100), (255, 100, 0),
                               (0, 100, 200)]
        self.codeString = codeString
        self.mainCodeHelper() # To load main code .py to getCode() button

        #IP Cam code
        self.ipCamURL = 'http://192.168.1.5:8080/shot.jpg'
        self.nd = 0  # this is for example GUI on button clicked
        self.ipCamIpButton.clicked.connect(self.loadVideoFromMobile)
        self.mobileCamButton.clicked.connect(self.loadVideoFromMobileHelper)


        # Load Save and Reset Buttons
        self.loadButton.clicked.connect(self.loadClicked)
        self.saveButton.clicked.connect(self.saveClicked)
        self.resetButton.clicked.connect(self.resetClicked)

        # Filter, Thresholds, Image Processing QCombo Boxes
        self.filters.activated.connect(self.applyFilter)
        self.thresholds.activated.connect(self.applyThresholds)
        self.imageProcessingQComboBox.activated.connect(self.applyImageProcessing)

        self.updateOriginal.clicked.connect(self.updateOriginalImage)

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

        # Face Detection:
        self.face_cascade = cv2.CascadeClassifier(
            r'assets/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(
            r'assets/haarcascade_eye.xml')
        self.actionFaceDetection.triggered.connect(self.actionFaceDetectionClicked)
        self.checkWatermarkButton.clicked.connect(self.checkWatermark)

        # image encryption and watermark
        self.watermarkImage.clicked.connect(self.waterMarkImageClicked)
        self.encryptData.clicked.connect(self.encryptDataClicked)
        self.decryptData.clicked.connect(self.decryptDataClicked)

        # play button
        self.playButton.clicked.connect(self.playButtonClicked)

        # Video Load button
        self.loadVideoButton.clicked.connect(self.loadVideoButtonClicked)
        self.stopVideoButton.clicked.connect(self.stopVideoButtonClicked)
        self.stopVideo = False

        # corner Detection buttons
        self.cornerDetectionQComboBox.activated.connect(self.applyCornerDetection)

        # menu and menu within menu
        self.createMenuBar()

        # getCode
        self.getCodeButton.clicked.connect(self.getCodeButtonClicked)

        # Paint2.0 initialization
        # global vars for paint

        self.backupImage = None
        self.img = None
        self.prevX = None
        self.prevY = None
        self.localMouseDown = False

        self.paint2Button.clicked.connect(self.paintButtonClicked)

    #Helper functions for getting code in getCode button!

    # End of helper functions

    # play button code

    # play button, links to the chrome dinasour game

    # video load option to allow users to load and apply filters on videos as well


    # Rotate Button clicked connect

    # Rotate Code End

    # Slider Code!
    # slider helper function

    # Slider Clicked(Signal Encoded)

    # Slider Code Clicked End

    # Instructions and About Code

    # Close(1 line)

    # Instructions and About Code

    # Saved Clicked

    # Most important function using QPixMap

    # Update Original Image

    # Reset Image

    # Load Clicked


    # ---------------------- Code for Morphological Transforms Was Here Before Refactoring ------------------- #

    # code shifted to file via decorators

    # Morphological code ends

    # IP cam Code for Mobile Imaging

app = QApplication(sys.argv)
window = gui()
window.setWindowTitle('Photoshop')
window.show()
sys.exit(app.exec_())
