def  button():
   return "height: 45px;border-radius: 10px; border: none; background-color: #385b7d;"

def  mainWindowStyle():
   return "background-color: #151b23; color: white; font: 20pt \"Bahnschrift\";"

def projectDescription():
   return "Az alkalmazás lehetővé teszi a<br>számítógép kézmozdulatokkal<br>történő irányítását"

def descLabelStyle():
    return "font: 20px \"Bahnschrift\"; text-align: justify; width: 400px; max-width: 350px;"

def mainContentLabel():
   return "text-align: center; max-height:100px;font-size: 20pt; height:30px"

def hasbara():
    return "hasbara"

def dropDownMenu():
    return """
    QLineEdit {
        font-size: 12pt;
        background-color: #385b7d;
        border-radius: 5px;
        height: 30px;
    }
    QCheckBox {
        color: #385b7d;
        margin: 12px;
    }
    QComboBox {
        font-size: 12pt;
        background-color: #385b7d;
        border-radius: 5px;
        height: 30px;
    }
    QComboBox QAbstractItemView::item:first {
        color: gray;
        
    }
    QSpinBox {
        border-radius: 5px;
        height: 30px;
        background-color: #385b7d;
        font-size: 12pt;
    }
    """

def contacts(): 
    return """
        <p>
            <ul>
                <li>Email:<br>barszcz.daniel@hallgato.sze.hu</li>
                <li> 
                    GitHub:<br>github.com/Excal21/Projektmunka
                </li>            
            </ul>
        </p>
    """
