import json

def createGestures(labels, taskFile):
    readable = {
        "None": "",
        "2up": "mutatás felfelé két ujjal",
        "2down": "mutatás lefelé két ujjal",
        "2left": "mutatás balra két ujjal",
        "2right": "mutatás jobbra két ujjal",
        "drei_glaser": "három",
        "peace": "csao",
        "2Metal": "metálvilla",
        "long_life": "hosszú élet",
        "fist": "ökölpacsi",
        "like": "tetszik",
        "perfect": "tökéletes",
        "middle_finger": "középső ujj",
        "fityisz": "fityisz",
        "F": "F",
    }

    gest_dict = {}
    for label in labels:
        if label in readable:
            gest_dict[label] = readable[label]
        else:
            gest_dict[label] = "Unknown"

    gest_dict['task'] = taskFile
    print(gest_dict)
    try:
        with open('GUI/gestures.json', 'w', encoding='utf-8') as file:
            json.dump(gest_dict, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing to gestures.json: {e}")
