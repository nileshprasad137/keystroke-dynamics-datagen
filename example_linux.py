"""
Example of hooking the keyboard on Linux using pyxhook

Generates JSON for keystroke timings. Refer paper for format.
"""
from __future__ import print_function

# Libraries we need
import pyxhook
import time
import json

password = ".tie5Roanl"
frequency_password_entry = 5
key_timings = dict()

user_keystroke_timings_list = list()
user_keystroke_timings_json = dict()

for char in list(password):
    if char.isupper():
        # if character is uppercase, have an additional dict key for corresponding lowercase letter!
        key_timings[char.lower()] = {"keyUp": None, "keyDown": None}

    if char == ".":
        key_timings["period"] = {"keyUp": None, "keyDown": None}
    else:
        key_timings[char] = {"keyUp": None, "keyDown": None}

key_timings["Return"] = {"keyUp": None, "keyDown": None}


# This function is called every time a key is pressed down
def kb_down_event(event):
    try:
        key_timings[event.Key]["keyUp"] = time.time()
    except KeyError:
        print("This key is not to be recorded : ", event.Key)


# This function is called every time a keypress is released
def kb_up_event(event):
    try:
        key_timings[event.Key]["keyDown"] = time.time()
    except KeyError:
        print("This key is not to be recorded : ", event.Key)

user_name = input("Enter your name: ")

# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kb_down_event
# Define our callback to fire when a key is pressed down
hookman.KeyUp = kb_up_event
# Hook the keyboard
hookman.HookKeyboard()
# Start our listener. Threads can only be started once.
hookman.start()

password_entry_count = 1

while password_entry_count <= 5:

    input_pwd = input("Enter \'{}\' : ".format(password))
    key_timings["Return"]["keyDown"] = time.time()
    is_pwd_correct = False
    if input_pwd == password:
        print("pwd correct!")
        is_pwd_correct = True

    dataset_based_timings = dict()
    dataset_based_timings["hold_time"] = dict()
    dataset_based_timings["ud_key1_key2"] = dict()
    dataset_based_timings["dd_key1_key2"] = dict()
    dataset_based_timings["password_entry_count"] = password_entry_count

    # print(json.dumps(key_timings))
    if is_pwd_correct:
        password_entry_count += 1
        # Calculate hold time of keys!
        for key in list(password):
            if key == ".":
                dataset_based_timings["hold_time"]["period"] = \
                    key_timings["period"]["keyDown"] - key_timings["period"]["keyUp"]
            elif key.isupper():
                try:
                    dataset_based_timings["hold_time"][key] = \
                        key_timings[key.lower()]["keyDown"] - key_timings[key]["keyUp"]
                except Exception:
                    dataset_based_timings["hold_time"][key] = \
                        key_timings[key]["keyDown"] - key_timings[key]["keyUp"]
            else:
                dataset_based_timings["hold_time"][key] = \
                    key_timings[key]["keyDown"]-key_timings[key]["keyUp"]

        for key1, key2 in zip(password, password[1:]):
            # Calculate ud_k1_k2 and dd_k1_k2
            if key1 == "." or key2 == ".":
                if key1 == ".":
                    key1 = "period"
                else:
                    key2 = "period"
                dataset_based_timings["dd_key1_key2"]["DD."+key1+"."+key2] = key_timings[key2]["keyDown"] - \
                                                                             key_timings[key1]["keyDown"]
                dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = key_timings[key2]["keyDown"] - \
                                                                                   key_timings[key1]["keyUp"]
            elif key1.isupper() or key2.isupper():
                try:
                    dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = \
                        key_timings[key2.lower()]["keyDown"] - key_timings[key1.lower()]["keyDown"]
                    dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = \
                        key_timings[key2.lower()]["keyDown"] - key_timings[key1]["keyUp"]
                except Exception:
                    dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = \
                        key_timings[key2]["keyDown"] - key_timings[key1]["keyDown"]
                    dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = \
                        key_timings[key2]["keyDown"] - key_timings[key1]["keyUp"]
            else:
                dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = \
                    key_timings[key2]["keyDown"] - key_timings[key1]["keyDown"]
                dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = \
                    key_timings[key2]["keyDown"] - key_timings[key1]["keyUp"]

        dataset_based_timings["hold_time"]["Return"] = key_timings["Return"]["keyDown"] - key_timings["Return"]["keyUp"]
        dataset_based_timings["ud_key1_key2"]["UD." + list(password)[-1] + ".Return"] = \
            key_timings["Return"]["keyDown"] - key_timings[list(password)[-1]]["keyUp"]
        dataset_based_timings["dd_key1_key2"]["DD." + list(password)[-1] + ".Return"] = \
            key_timings["Return"]["keyDown"] - key_timings[list(password)[-1]]["keyDown"]

    else:
        print("Password entered was not correct! Please type \'{}\' again !".format(password))

    user_keystroke_timings_list.append(dataset_based_timings)

user_keystroke_timings_json["timings"] = user_keystroke_timings_list
user_keystroke_timings_json["user"] = user_name
print(json.dumps(user_keystroke_timings_json))

with open('output/{}_timings.json'.format(user_name), 'w') as outfile:
    json.dump(user_keystroke_timings_json, outfile)

# Close the listener when recording is done!
hookman.cancel()
