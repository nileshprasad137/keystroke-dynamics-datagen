"""
Keystroke Dynamics Recorder 
"""

from __future__ import print_function
import time
import json
from pynput import keyboard

password = ".tie5Roanl"
frequency_password_entry = 10
key_timings = {}

user_keystroke_timings_list = []
user_keystroke_timings_json = {}

# Ensure keys are stored in lowercase & with correct names
for char in password:
    normalized_char = char.lower() if char.isalpha() else char
    key_timings[normalized_char] = {"keyUp": None, "keyDown": None}

key_timings["return"] = {"keyUp": None, "keyDown": None}  # Fixing Return key handling

# Capture key press (keydown) event
def kb_down_event(key):
    try:
        key_str = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
        if key_str in key_timings:
            key_timings[key_str]["keyDown"] = time.time()
    except AttributeError:
        pass  # Ignore unknown keys

# Capture key release (keyup) event
def kb_up_event(key):
    try:
        key_str = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
        if key_str in key_timings:
            key_timings[key_str]["keyUp"] = time.time()
    except AttributeError:
        pass

user_name = input("Enter your name: ")

password_entry_count = 1

# Create keyboard listener
with keyboard.Listener(on_press=kb_down_event, on_release=kb_up_event) as listener:
    while password_entry_count <= frequency_password_entry:
        print(f"Enter {1 + frequency_password_entry - password_entry_count} times more!")
        input_pwd = input(f"Enter '{password}': ")

        if input_pwd == password:
            print("Password correct!")
            dataset_based_timings = {
                "hold_time": {},
                "ud_key1_key2": {},
                "dd_key1_key2": {},
                "password_entry_count": password_entry_count
            }

            # Calculate hold time of keys
            for key in password:
                normalized_key = key.lower()
                dataset_based_timings["hold_time"][normalized_key] = (
                    key_timings[normalized_key]["keyUp"] - key_timings[normalized_key]["keyDown"]
                ) if key_timings[normalized_key]["keyUp"] and key_timings[normalized_key]["keyDown"] else None

            for key1, key2 in zip(password, password[1:]):
                key1_norm, key2_norm = key1.lower(), key2.lower()
                dataset_based_timings["dd_key1_key2"]["DD." + key1_norm + "." + key2_norm] = (
                    key_timings[key2_norm]["keyDown"] - key_timings[key1_norm]["keyDown"]
                ) if key_timings[key2_norm]["keyDown"] and key_timings[key1_norm]["keyDown"] else None
                
                dataset_based_timings["ud_key1_key2"]["UD." + key1_norm + "." + key2_norm] = (
                    key_timings[key2_norm]["keyDown"] - key_timings[key1_norm]["keyUp"]
                ) if key_timings[key2_norm]["keyDown"] and key_timings[key1_norm]["keyUp"] else None

            time.sleep(1)

            dataset_based_timings["hold_time"]["return"] = (
                key_timings["return"]["keyUp"] - key_timings["return"]["keyDown"]
            ) if key_timings["return"]["keyUp"] and key_timings["return"]["keyDown"] else None

            dataset_based_timings["ud_key1_key2"]["UD." + password[-1] + ".return"] = (
                key_timings["return"]["keyDown"] - key_timings[password[-1].lower()]["keyUp"]
            ) if key_timings["return"]["keyDown"] and key_timings[password[-1].lower()]["keyUp"] else None

            dataset_based_timings["dd_key1_key2"]["DD." + password[-1] + ".return"] = (
                key_timings["return"]["keyDown"] - key_timings[password[-1].lower()]["keyDown"]
            ) if key_timings["return"]["keyDown"] and key_timings[password[-1].lower()]["keyDown"] else None

            user_keystroke_timings_list.append(dataset_based_timings)
            password_entry_count += 1
        else:
            print(f"Incorrect password! Please type '{password}' again.")

    user_keystroke_timings_json["timings"] = user_keystroke_timings_list
    user_keystroke_timings_json["user"] = user_name
    print(json.dumps(user_keystroke_timings_json, indent=4))

    with open(f'output/{user_name}_timings.json', 'w') as outfile:
        json.dump(user_keystroke_timings_json, outfile)

print("Keystroke data saved successfully!")
