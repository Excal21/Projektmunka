from PyQt6 import QtCore, QtGui, QtWidgets
import style
import preferences
isRecRunning=False
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
        self.pushButton.clicked.connect(self.startRecognition)
        self.horizontalLayout.addWidget(self.pushButton)

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
        self.horizontalLayout_2.addWidget(self.label_3)

        self.label_2 = QtWidgets.QLabel(parent=self.horizontalWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Create the settings window instance here
        self.settingsWindow = QtWidgets.QMainWindow()
        self.ui_settings = Ui_settingsWindow()
        self.ui_settings.setupUi(self.settingsWindow)

    def openSettings(self):
        self.settingsWindow.show()
    def startRecognition(self):
        global isRecRunning
        #itt kéne a mozdulatok felismerésének kezdődnie
        if isRecRunning:
            self.pushButton.setText("Használat")
            isRecRunning=False
        else:
            self.pushButton.setText("Megállítás")
            isRecRunning=True
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GestureMaster"))
        self.pushButton.setText(_translate("MainWindow", "Használat"))
        self.pushButton_2.setText(_translate("MainWindow", "Beállítások"))
        self.label.setText(_translate("MainWindow", "GestureMaster"))
        self.label_3.setText(_translate("MainWindow", style.projectDescription()))
        self.label_2.setText(_translate("MainWindow", style.contacts()))

class Ui_settingsWindow(object):
    def setupUi(self, settingsWindow):
        settingsWindow.setObjectName("settingsWindow")
        settingsWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(parent=settingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet(style.mainWindowStyle())
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 731, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
       
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.label_2 = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2, 0, QtCore.Qt.AlignmentFlag.AlignHCenter|QtCore.Qt.AlignmentFlag.AlignVCenter)
        
        self.gridLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(450, 130, 400,500))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        
        self.thumbsDown = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.thumbsDown.setObjectName("thumbsDown")
        self.thumbsDown.addItems(["Thumbs down", "Ctrl+C", "Ctrl+V", "Fényerő növelése", "Fényerő csökkentése", "Böngésző megnyitása"])
        self.thumbsDown.model().item(0).setEnabled(False)
        self.thumbsDown.setStyleSheet(style.dropDownMenu())
        self.gridLayout.addWidget(self.thumbsDown, 1, 0, 1, 1)
        
        self.victory = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.victory.setObjectName("victory")
        self.victory.addItems(["Victory", "Ctrl+C", "Ctrl+V", "Fényerő növelése", "Fényerő csökkentése", "Böngésző megnyitása"])
        self.victory.model().item(0).setEnabled(False)
        self.victory.setStyleSheet(style.dropDownMenu())
        self.gridLayout.addWidget(self.victory, 0, 1, 1, 1)
        
        self.pointingUp = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.pointingUp.setObjectName("pointingUp")
        self.pointingUp.addItems(["Pointing up", "Ctrl+C", "Ctrl+V", "Fényerő növelése", "Fényerő csökkentése", "Böngésző megnyitása"],)
        self.pointingUp.model().item(0).setEnabled(False)
        self.pointingUp.setStyleSheet(style.dropDownMenu())
        self.gridLayout.addWidget(self.pointingUp, 1, 1, 1, 1)
        
        self.thumbsUp = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.thumbsUp.setObjectName("thumbsUp")
        self.thumbsUp.addItems(["Thumbs up", "Ctrl+C", "Ctrl+V", "Fényerő növelése", "Fényerő csökkentése", "Böngésző megnyitása"])
        self.thumbsUp.model().item(0).setEnabled(False)
        self.thumbsUp.setStyleSheet(style.dropDownMenu())
        self.gridLayout.addWidget(self.thumbsUp, 0, 0, 1, 1)
        
        self.inputSourceLabel = QtWidgets.QLabel(parent=self.gridLayoutWidget)
        self.inputSourceLabel.setObjectName("inputSourceLabel")
        self.inputSourceLabel.setStyleSheet("max-height: 30px;")
        self.gridLayout.addWidget(self.inputSourceLabel, 2, 0, 1, 2, QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Connect signals to the slot to ensure unique selections
        self.thumbsDown.currentIndexChanged.connect(self.updateComboBoxes)
        self.victory.currentIndexChanged.connect(self.updateComboBoxes)
        self.pointingUp.currentIndexChanged.connect(self.updateComboBoxes)
        self.thumbsUp.currentIndexChanged.connect(self.updateComboBoxes)

        self.inputSource = QtWidgets.QComboBox(parent=self.gridLayoutWidget)
        self.inputSource.setObjectName("inputSource")
        self.inputSource.addItems(["eszköz kamerája", "telefon kamerája"])
        self.inputSource.setStyleSheet(style.dropDownMenu())
        self.gridLayout.addWidget(self.inputSource, 3, 0, 1, 2)

        self.saveSettings = QtWidgets.QPushButton(parent=self.gridLayoutWidget)
        self.saveSettings.setObjectName("saveSettings")
        self.saveSettings.setStyleSheet(style.button())
        self.saveSettings.clicked.connect(self.savePreferences)  # Pass the method reference without parentheses
        self.gridLayout.addWidget(self.saveSettings, 4, 0, 1, 2)
        
        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.gridLayoutWidget_2 = QtWidgets.QWidget(parent=self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(30, 130, 371, 471))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
       
        self.label_3 = QtWidgets.QLabel(parent=self.gridLayoutWidget_2)
        self.label_3.setObjectName("label_3")
        
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 2)
        
        self.label_5 = QtWidgets.QLabel(parent=self.gridLayoutWidget_2)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.label_4 = QtWidgets.QLabel(parent=self.gridLayoutWidget_2)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.label_6 = QtWidgets.QLabel(parent=self.gridLayoutWidget_2)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        self.label_7 = QtWidgets.QLabel(parent=self.gridLayoutWidget_2)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 1, 1, 1, QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        settingsWindow.setCentralWidget(self.centralwidget)
        

        self.retranslateUi(settingsWindow)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)

    def savePreferences(self):
            # Your code to handle the button click event
            selected= [self.thumbsDown.currentText(), self.victory.currentText(), self.pointingUp.currentText(), self.thumbsUp.currentText(),self.inputSource.currentText()]
            preferences.create_preferences(selected)
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
            msg.setText("Beállítások elmentve!")
            msg.setWindowTitle("Sikeres mentés")
            msg.exec()


    def updateComboBoxes(self):
            selected_items = {
            self.thumbsDown: self.thumbsDown.currentText(),
            self.victory: self.victory.currentText(),
            self.pointingUp: self.pointingUp.currentText(),
            self.thumbsUp: self.thumbsUp.currentText()
            }

            for combo in [self.thumbsDown, self.victory, self.pointingUp, self.thumbsUp]:
                for i in range(combo.count()):
                    item_text = combo.itemText(i)
                    if item_text in selected_items.values() and selected_items[combo] != item_text:
                        combo.model().item(i).setEnabled(False)
                    else:
                        combo.model().item(i).setEnabled(True)

    def retranslateUi(self, settingsWindow):
        _translate = QtCore.QCoreApplication.translate
        settingsWindow.setWindowTitle(_translate("settingsWindow", "Settings"))
        self.label.setText(_translate("settingsWindow", "Használati Útmutató"))
        self.label_2.setText(_translate("settingsWindow", "Vezérlőpult"))
        self.saveSettings.setText(_translate("settingsWindow", "Beállítások mentése"))
        self.inputSourceLabel.setText(_translate("settingsWindow", "Bemeneti forrás kiválasztása"))
        self.label_3.setText(_translate("settingsWindow", style.hasbara()))
        self.label_5.setText(_translate("settingsWindow", style.victory()))
        self.label_4.setText(_translate("settingsWindow", style.thumbsUp()))
        self.label_6.setText(_translate("settingsWindow", style.thumbsDown()))
        self.label_7.setText(_translate("settingsWindow", style.pointingUp()))
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
