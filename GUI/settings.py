from PyQt6 import QtCore, QtGui, QtWidgets
import sys
import style
import preferences
import json
import webbrowser
import main

class Ui_settingsWindow(QtCore.QObject):
    taskFileUpdated = QtCore.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.usedTaskFile = None  # Store the passed task file locally

    def setupUi(self, settingsWindow):
        settingsWindow.setObjectName("settingsWindow")
        settingsWindow.resize(900, 700)
        settingsWindow.setStyleSheet(style.mainWindowStyle())

        # Central widget
        self.centralwidget = QtWidgets.QWidget(parent=settingsWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Horizontal Layout Widget for Label and Button
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 731, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Label
        self.label = QtWidgets.QLabel(parent=self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Button to open File Dialog
        self.fileDialogButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.fileDialogButton.setObjectName("fileDialogButton")
        self.fileDialogButton.setText("tallózás")
        self.fileDialogButton.setStyleSheet(style.button())
        self.fileDialogButton.clicked.connect(self.openFileDialog)
        self.horizontalLayout.addWidget(self.fileDialogButton, 0, QtCore.Qt.AlignmentFlag.AlignHCenter)

        # Main content layout
        self.mainContentWidget = QtWidgets.QWidget(self.centralwidget)
        self.mainContentWidget.setGeometry(QtCore.QRect(30, 100, 840, 500))
        self.mainContentWidget.setObjectName("mainContentWidget")

        self.mainContentLayout = QtWidgets.QHBoxLayout(self.mainContentWidget)
        self.mainContentLayout.setObjectName("mainContentLayout")

        # Create widgets to hold the grid layouts
        self.leftWidget = QtWidgets.QWidget(self.mainContentWidget)
        self.leftWidget.setObjectName("leftWidget")
        self.rightWidget = QtWidgets.QWidget(self.mainContentWidget)
        self.rightWidget.setObjectName("rightWidget")

        # Create grid layouts and set them to the widgets
        self.leftGrid = QtWidgets.QGridLayout(self.leftWidget)
        self.leftGrid.setObjectName("leftGrid")
        self.rightGrid = QtWidgets.QGridLayout(self.rightWidget)
        self.rightGrid.setObjectName("rightGrid")

        # Add the widgets to the main content layout
        self.mainContentLayout.addWidget(self.leftWidget)
        self.mainContentLayout.addWidget(self.rightWidget)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setStyleSheet(style.button())
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Mentés")
        self.saveButton.setGeometry(QtCore.QRect(30, 600, 731, 80))
        self.saveButton.setEnabled(False)
        self.saveButton.setVisible(False)
        settingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(settingsWindow)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)
        
    def retranslateUi(self, settingsWindow):
        _translate = QtCore.QCoreApplication.translate
        settingsWindow.setWindowTitle(_translate("settingsWindow", "Beállítások"))
        self.label.setText(_translate("settingsWindow", "JSON fájl kiválasztása"))

    def openFileDialog(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(
            parent=self.centralwidget,  # Parent set to centralwidget for better modality
            caption="Select JSON File",
            directory="",  # Initial directory
            filter="JSON Files (*.json);;All Files (*)",  # File types filter
        )
        if fileName:
            try:
                with open(fileName, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    if isinstance(data, dict):
                        self.usedTaskFile = data.get("task")
                        data.pop("task", None)  # Remove "task" key if it exists
                        main.selected_prefs.append(data)
                        self.addOptions()
                        self.sendTaskFileToMain()
                    else:
                        message = QtWidgets.QMessageBox()
                        message.setWindowTitle("Error")
                        message.setText("A JSON fájl nem tartalmazza a megfelelő adatokat!")
                        message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                        message.exec()
            except Exception as e:
                message = QtWidgets.QMessageBox()
                message.setWindowTitle("Error")
                message.setText(f"Hiba a JSON fájl beolvasása közben: {e}")
                message.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                message.exec()

    def addOptions(self):
        # Clear existing widgets in the grids if needed
        for i in reversed(range(self.leftGrid.count())): 
            self.leftGrid.itemAt(i).widget().setParent(None)
        for i in reversed(range(self.rightGrid.count())): 
            self.rightGrid.itemAt(i).widget().setParent(None)
        
        # Add gesture label
        self.gestureLabel = QtWidgets.QLabel(parent=self.leftWidget)
        self.gestureLabel.setObjectName("gestureLabel")
        self.gestureLabel.setText("Gesztus")
        self.leftGrid.addWidget(self.gestureLabel, 0, 0, 1, 1)
        self.gestureLabel.setStyleSheet(style.mainContentLabel())
        
        # Add options label
        self.optionsLabel = QtWidgets.QLabel(parent=self.rightWidget)
        self.optionsLabel.setObjectName("optionsLabel")
        self.optionsLabel.setText("hozzárendelés")
        self.rightGrid.addWidget(self.optionsLabel, 0, 0, 1, 1)
        self.optionsLabel.setStyleSheet(style.mainContentLabel())
    
        # Store combo boxes for later access
        self.comboBoxes = []

        # Add dynamic options based on selected_prefs
        row = 1
        for gesture, description in main.selected_prefs[0].items():
            gestureLabel = QtWidgets.QLabel(parent=self.leftWidget)
            gestureLabel.setObjectName(f"{gesture}RadioButton")
            gestureLabel.setText(description)
            gestureLabel.setStyleSheet(style.mainContentLabel())
            self.leftGrid.addWidget(gestureLabel, row, 0, 1, 1)
            
            optionsComboBox = QtWidgets.QComboBox(parent=self.rightWidget)
            optionsComboBox.setObjectName(f"{gesture}ComboBox")
            optionsComboBox.addItems(main.possible_commands)
            optionsComboBox.setStyleSheet(style.mainContentCombobox())
            self.rightGrid.addWidget(optionsComboBox, row, 0, 1, 1)
            
            # Connect the signal to a slot to handle option selection
            optionsComboBox.currentIndexChanged.connect(self.updateComboBoxes)
            
            self.comboBoxes.append(optionsComboBox)
            row += 1
        self.IPlabel = QtWidgets.QLabel(parent=self.leftWidget)
        self.IPlabel.setObjectName("IPlabel")
        self.IPlabel.setText("IP cím (ha üres, alapértelmezett kamerát használja)")
        self.leftGrid.addWidget(self.IPlabel, row, 0, 1, 1) 
        self.ipInput = QtWidgets.QLineEdit(parent=self.rightWidget)
        self.ipInput.setObjectName("ipInput")
        self.ipInput.setStyleSheet(style.mainContentCombobox())
        self.rightGrid.addWidget(self.ipInput, row, 0, 1, 1)
        self.saveButton.setVisible(True)
        self.saveButton.clicked.connect(self.savePreferences)
        self.saveButton.setEnabled(True)
    
    def savePreferences(self):
        selected_choices = self.getComboBoxChoices()
        ipAddress = self.ipInput.text()
        message = QtWidgets.QMessageBox()
        message.setWindowTitle("Sikeres mentés")
        message.setText("A beállítások sikeresen elmentve!")
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.exec()
        preferences.createPreferences(main.selected_prefs, selected_choices, ipAddress)

    def getComboBoxChoices(self):
        choices = []
        for comboBox in self.comboBoxes:
            choices.append(comboBox.currentText())
        return choices
    
    def updateComboBoxes(self):
        selected_items = set()
        for comboBox in self.comboBoxes:
            selected_items.add(comboBox.currentText())
        
        for comboBox in self.comboBoxes:
            for index in range(comboBox.count()):
                item_text = comboBox.itemText(index)
                if item_text in selected_items and item_text != comboBox.currentText():
                    comboBox.model().item(index).setEnabled(False)
                else:
                    comboBox.model().item(index).setEnabled(True)

    def sendTaskFileToMain(self):
        self.taskFileUpdated.emit(self.usedTaskFile)

    def setTaskFile(self, task_file):
        self.usedTaskFile = task_file
