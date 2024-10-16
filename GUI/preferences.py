import json

def createPreferences(gestures, preferences, ipAddress, radioButton, sensitivity):
    gest_dict = gestures[0].keys()
    
    # Merge gest_dict keys and preferences values into settings dictionary
    settings = {key: preferences[i] for i, key in enumerate(gest_dict)}
    settings.update({'camFeed': radioButton, 'sensitivity': sensitivity})
    if ipAddress != "":
        settings.update({'ip_address': ipAddress})
    print(settings)
    
    # Write the settings dictionary to preferences.json
    with open('preferences.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)