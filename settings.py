from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
import style
import main
import json

class Ui_settingsWindow(QtCore.QObject):
    taskFileUpdated = QtCore.pyqtSignal(str)
    
    def __init__(self, selected_prefs):
        super().__init__()
        self.selected_prefs = selected_prefs

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
        self.addOptions()
        # Add the widgets to the main content layout
        self.mainContentLayout.addWidget(self.leftWidget)
        self.mainContentLayout.addWidget(self.rightWidget)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setStyleSheet(style.button())
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Mentés")
        self.saveButton.setGeometry(QtCore.QRect(30, 600, 731, 80))
        self.saveButton.clicked.connect(self.savePreferences)
        settingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(settingsWindow)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)
        
    def retranslateUi(self, settingsWindow):
        _translate = QtCore.QCoreApplication.translate
        settingsWindow.setWindowTitle(_translate("settingsWindow", "Beállítások"))
        self.label.setText(_translate("settingsWindow", "Gesztusvezérlés beállításai"))

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
        for gesture, description in self.selected_prefs.items():
            gestureLabel = QtWidgets.QLabel(parent=self.leftWidget)
            gestureLabel.setObjectName(f"{gesture}RadioButton")
            gestureLabel.setText(description)
            gestureLabel.setStyleSheet(style.mainContentLabel())
            self.leftGrid.addWidget(gestureLabel, row, 0, 1, 1)
            
            optionsComboBox = QtWidgets.QComboBox(parent=self.rightWidget)
            optionsComboBox.setObjectName(f"{gesture}ComboBox")
            optionsComboBox.addItems(main.possible_commands)
            optionsComboBox.setStyleSheet(style.dropDownMenu())
            self.rightGrid.addWidget(optionsComboBox, row, 0, 1, 1)
            
            # Connect the signal to a slot to handle option selection
            optionsComboBox.currentIndexChanged.connect(self.updateComboBoxes)
            
            self.comboBoxes.append(optionsComboBox)
            row += 1
        
        # Add sensitivity label and input
        self.sensitivityLabel = QtWidgets.QLabel(parent=self.leftWidget) 
        self.sensitivityLabel.setObjectName("sensitivityLabel")
        self.sensitivityLabel.setText("Érzékenység")
        self.leftGrid.addWidget(self.sensitivityLabel, row, 0, 1, 1)
        self.sensitivityLabel.setStyleSheet(style.mainContentLabel())
        
        self.sensitivityInput = QtWidgets.QLineEdit(parent=self.rightWidget)
        self.sensitivityInput.setObjectName("sensitivityInput")
        self.sensitivityInput.setStyleSheet(style.dropDownMenu())
        self.sensitivityInput.setPlaceholderText("1-25")
        self.sensitivityInput.setText("5")
        self.sensitivityInput.setSizeIncrement(1, 1)

        # Set the validator to only allow integers between 1 and 25
        int_validator = QIntValidator(1, 25)
        self.sensitivityInput.setValidator(int_validator)

        self.rightGrid.addWidget(self.sensitivityInput, row, 0, 1, 1)
        row += 1

        # Add IP label and input
        self.IPlabel = QtWidgets.QLabel(parent=self.leftWidget)
        self.IPlabel.setObjectName("IPlabel")
        self.IPlabel.setStyleSheet(style.mainContentLabel())
        self.IPlabel.setText("IP cím (ha üres, alapértelmezett kamerát használja)")
        self.leftGrid.addWidget(self.IPlabel, row, 0, 1, 1) 
        
        self.ipInput = QtWidgets.QLineEdit(parent=self.rightWidget)
        self.ipInput.setObjectName("ipInput")
        self.ipInput.setStyleSheet(style.dropDownMenu())
        self.ipInput.setPlaceholderText("255.255.255.255")
        # Use QRegularExpressionValidator with a more precise regular expression for IP addresses
        ip_validator = QtGui.QRegularExpressionValidator(QtCore.QRegularExpression(
            r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
        ))
        self.ipInput.setValidator(ip_validator)

        self.rightGrid.addWidget(self.ipInput, row, 0, 1, 1)
        row += 1

        # Add camera feed label and radio button
        self.camFeedLabel = QtWidgets.QLabel(parent=self.leftWidget)
        self.camFeedLabel.setObjectName("camFeedLabel") 
        self.camFeedLabel.setText("Kamerakép?")
        self.camFeedLabel.setStyleSheet(style.mainContentLabel())
        self.leftGrid.addWidget(self.camFeedLabel, row, 0, 1, 1)

        self.camFeedCheckBox = QtWidgets.QCheckBox(parent=self.rightWidget) 
        self.camFeedCheckBox.setObjectName("camFeedCheckBox")
        self.camFeedCheckBox.setStyleSheet(style.dropDownMenu())
        self.camFeedCheckBox.setChecked(True)
        self.rightGrid.addWidget(self.camFeedCheckBox, row, 0, 1, 1)
        row += 1
    
    def savePreferences(self):
        selected_choices = self.getComboBoxChoices()
        ipAddress = self.ipInput.text()
        sensitivity = self.sensitivityInput.text()
        radioButton = self.camFeedCheckBox.isChecked()  # Correctly get the state of the radio button
        settings = {}
        settings.update(selected_choices)
        settings['ip_address'] = ipAddress if ipAddress != "" else 0
        settings['sensitivity'] = sensitivity
        settings['camFeed'] = radioButton
        with open('preferences.json', 'w', encoding='utf-8') as file:
            json.dump(settings, file, indent=4)
        message = QtWidgets.QMessageBox()
        message.setWindowTitle("Sikeres mentés")
        message.setText("A beállítások sikeresen elmentve!")
        message.setIcon(QtWidgets.QMessageBox.Icon.Information)
        message.exec()
        
    def getComboBoxChoices(self):
        choices = {}
        for comboBox in self.comboBoxes:
            gesture = comboBox.objectName().replace("ComboBox", "")
            choices[gesture] = comboBox.currentText()
        return choices
    
    def updateComboBoxes(self):
        selected_items = set()
        for comboBox in self.comboBoxes:
            selected_items.add(comboBox.currentText())
        
        for comboBox in self.comboBoxes:
            for index in range(comboBox.count()):
                item_text = comboBox.itemText(index)
                if item_text in selected_items and item_text != comboBox.currentText() and item_text != "":
                    comboBox.model().item(index).setEnabled(False)
                else:
                    comboBox.model().item(index).setEnabled(True)