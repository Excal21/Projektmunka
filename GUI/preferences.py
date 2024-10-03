import json

def createPreferences(gestures, preferences,ipAddress):
    gest_dict = gestures[0].keys()
    
    # Merge gest_dict keys and preferences values into settings dictionary
    settings = {key: preferences[i] for i, key in enumerate(gest_dict)}
    if ipAddress!="":
        settings.update({'ip_address': ipAddress})
    print(settings)
    
    # Write the settings dictionary to preferences.json
    with open('preferences.json', 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)
