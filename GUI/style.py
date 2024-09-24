def  button():
   return "height: 45px;border-radius: 10px; border: none; background-color: #872341;"

def  mainWindowStyle():
   return "background-color: #22092C; color: white; font: 20pt \"Bahnschrift\";"

def projectDescription():
   return "picsa"

def contacts(): 
   return "fasz"
def dropDownMenu():
    return """
    QComboBox {
        font-size: 12pt;
        background-color: #872341;
        border-radius: 5px;
        height: 30px;
    }
    QComboBox::down-arrow {
        height: 10px;
        border-radius: 3px;

    }
    QComboBox QAbstractItemView::item:first {
        color: gray;
    }
    """
def hasbara():
    return "hasbara"
def thumbsUp():
    return '<html><head/><body><p>Thumbs Up<br/><img src="thumbsup.png"/></p></body></html>'
def thumbsDown():
   return '<html><head/><body><p>Thumbs Down<br/><img src="thumbsdonw.png"/></p></body></html>'
def pointingUp():
    return '<html><head/><body><p>Pointing Up<br/><img src=""/></p></body></html>'
def victory():
   return '<html><head/><body><p>Victory<br/><img src=""/></p></body></html>'