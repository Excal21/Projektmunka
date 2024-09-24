import json

def create_preferences(settings):
    options = ["thumbs_down", "victory", "pointing_up", "thumbs_up", "input_source"]
    replacements = {
        "eszköz kamerája": "dev_cam",
        "telefon kamerája": "phone_mic",
        "Ctrl+c": "copy",
        "Ctrl+v": "paste",
        "Fényerő növelés": "increase_brightness",
        "Fényerő csökkentés": "decrease_brightness",
        "Böngésző megnyitása": "open_browser"
    }
    def_set = ["Thumbs down", "Victory", "Pointing up", "Thumbs up"]

    # Replace settings with their corresponding values
    for i in range(len(settings)):
        for key, value in replacements.items():
            settings[i] = settings[i].replace(key, value)

    # Create preferences dictionary
    prefs = {options[i]: settings[i] for i in range(len(options))}

    # Ensure unique settings
    seen = set()
    for i in range(len(def_set)):
        if prefs[options[i]] in def_set or prefs[options[i]] in seen:
            prefs[options[i]] = 'not_set'
        else:
            seen.add(prefs[options[i]])

    # Convert prefs dictionary to JSON and save to file
    with open('preferences.json', 'w', encoding='utf-8') as json_file:
        json.dump(prefs, json_file, ensure_ascii=False, indent=4)

    print(prefs)