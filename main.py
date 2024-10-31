import threading
from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import style
import json
import webbrowser
import gesture_detection as gd
import settings

global usedTaskFile
usedTaskFile = "gesture_recognizer.task"
recognizer = gd.Recognition(usedTaskFile)
global selected_prefs
selected_prefs = recognizer.labels_with_alias

possible_commands = ["", "Ctrl+C", "Ctrl+V", "Böngésző megnyitása", "fényerő növelése", "fényerő csökkentése"]

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(style.mainWindowStyle())
        
        # Central widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Navigation buttons widget
        self.navButtonsWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.navButtonsWidget.setGeometry(QtCore.QRect(40, 420, 721, 101))
        self.navButtonsWidget.setStyleSheet("horizontal-alignment: center;")
        self.navButtonsWidget.setObjectName("navButtonsWidget")
        
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.navButtonsWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Buttons
        self.pushButton = QtWidgets.QPushButton(parent=self.navButtonsWidget)
        self.pushButton.setMinimumSize(QtCore.QSize(0, 28))
        self.pushButton.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButton.setStyleSheet(style.button())
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.pushButton.clicked.connect(self.startRecognition)

        self.pushButton_2 = QtWidgets.QPushButton(parent=self.navButtonsWidget)
        self.pushButton_2.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.pushButton_2.setStyleSheet(style.button())
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.openSettings)
        self.horizontalLayout.addWidget(self.pushButton_2)
        
        # Label
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(260, 30, 281, 81))
        self.label.setStyleSheet("text-align: center;")
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")

        # Other labels
        self.horizontalWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalWidget.setGeometry(QtCore.QRect(40, 130, 721, 271))
        self.horizontalWidget.setObjectName("horizontalWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.label_3 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label_3.setStyleSheet(style.descLabelStyle())
        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_2 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_2.setStyleSheet(style.descLabelStyle())
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.RichText)
        self.label_2.setText(style.contacts())
        self.horizontalLayout_2.addWidget(self.label_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Create the settings window instance here
        self.settingsWindow = QtWidgets.QMainWindow()
        self.ui_settings = settings.Ui_settingsWindow(selected_prefs)
        self.ui_settings.setupUi(self.settingsWindow)
    
    def startRecognition(self):
        try:
            with open('preferences.json', 'r', encoding='utf-8') as file:
                data = json.load(file)
                global usedTaskFile
                if data:  # Check if data is not empty
                    camFeed = data.get('camFeed')
                    sensitivity = data.get('sensitivity')
                    ipAddress = data.get('ip_address', None)  # Use get method with default value
                    x = None
                    if self.pushButton.text() == "Használat":
                        x = threading.Thread(target=recognizer.Run, args=())
                        x.start()
                        self.pushButton.setText("megállítás")  # Change button text to "megállítás"
                        self.pushButton_2.setEnabled(False)  # Disable pushButton_2
                    else:
                        recognizer.Stop()
                        self.pushButton.setText("Használat")  # Change button text back to "Használat"
                        self.pushButton_2.setEnabled(True)  # Enable pushButton_2
        except Exception as e:
            print(f"Error in startRecognition: {e}")
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Hiba")
            message.setText("Nincs kiválasztott fájl!")
            message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message.exec()
            return
        
    def openSettings(self):
        self.settingsWindow.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GestureMaster"))
        self.pushButton.setText(_translate("MainWindow", "Használat"))
        self.pushButton_2.setText(_translate("MainWindow", "Beállítások"))
        self.label.setText(_translate("MainWindow", "GestureMaster"))
        self.label_3.setText(_translate("MainWindow", style.projectDescription()))
        open('preferences.json', 'w').close()
    
if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())