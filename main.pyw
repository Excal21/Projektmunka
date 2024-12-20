import time
import threading
from PyQt6 import QtCore, QtWidgets
import sys
import style
import json
import gesture_detection as gd
import settings

global usedTaskFile
usedTaskFile = "gesture_recognizer.task"
recognizer = gd.Recognition(usedTaskFile)
global selected_prefs
selected_prefs = recognizer.labels_with_alias

try:
    selected_prefs.pop('None')
    selected_prefs.pop('NONE')
    selected_prefs.pop('none')
except KeyError:
    pass

possible_commands = ["", "Ctrl+C", "Ctrl+V", "Böngésző megnyitása", "Jobbra", "Balra",
                     "Asztal megjelenítése", "Számológép indítása", "Lejátszás/ megállítás", "Következő", "Előző",
                     "Hangerő növelése", "Hangerő csökkentése"]


class ThreadWithException(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ThreadWithException, self).__init__(*args, **kwargs)
        self._exception = None

    def run(self):
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        except BaseException as e:
            self._exception = e

    def join_with_exception(self):
        if self._exception:
            raise self._exception


def monitor_thread(thread):
    while thread.is_alive():
        time.sleep(1)
    thread.join_with_exception()


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
                    frameCount = data.get('frameCount')
                    x = None
                    recognizer.camera = ipAddress
                    gesture_dict = {}
                    # Read key-value pairs from data and store them in gesture_dict
                    for key, value in data.items():
                        gesture_dict[key] = value
                    recognizer.commands = gesture_dict
                    recognizer.confidence = int(sensitivity)
                    recognizer.camerafeed = camFeed
                    recognizer.framecount = frameCount

                    if self.pushButton.text() == "Használat":
                        x = ThreadWithException(target=recognizer.Run)
                        x.start()

                        # Monitor the thread to catch exceptions
                        monitor_thread_thread = threading.Thread(target=monitor_thread, args=(x,))
                        monitor_thread_thread.start()

                        self.pushButton.setText("megállítás")  # Change button text to "megállítás"
                        self.pushButton_2.setEnabled(False)  # Disable pushButton_2
                        time.sleep(1)
                        if x.is_alive() and recognizer.error:
                            recognizer.Stop()
                            recognizer.error = False
                            self.pushButton.setText("Használat")  # Change button text back to "Használat"
                            self.pushButton_2.setEnabled(True)  # Enable pushButton_2
                            raise ConnectionError

                    else:
                        recognizer.Stop()
                        self.pushButton.setText("Használat")  # Change button text back to "Használat"
                        self.pushButton_2.setEnabled(True)  # Enable pushButton_2
        except ConnectionError:
            print("Error in startRecognition: ConnectionError")
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Hiba")
            message.setText("Nem sikerült kapcsolódni a kameraához. Kérlek, ellenőrizd az IP címet!")
            message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            message.exec()
            return

        except Exception as e:
            print(f"Error in startRecognition: {e}")
            message = QtWidgets.QMessageBox()
            message.setWindowTitle("Hiba")
            message.setText("Kérlek, add meg a gesztusvezérlés beállításait!")
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
    
if __name__ == "__main__": 
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
