import json

def createGestures(labels):
    gest_dict = labels[0].keys()
    #itt lenne még valami, de majd hétfőn
    with open('GUI/gestures.json', 'w', encoding='utf-8') as file:
        json.dump(gest_dict, file, ensure_ascii=False, indent=4)
    