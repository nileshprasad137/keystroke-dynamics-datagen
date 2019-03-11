"""
A simple example of hooking the keyboard on Linux using pyxhook

Any key pressed prints out the keys values, program terminates when spacebar
is pressed.
"""
from __future__ import print_function

# Libraries we need
import pyxhook
import time
import json

password = ".tie5Roanl"
key_timings = dict()

for char in list(password):
    if char.isupper():
        # if character is uppercase, have an additional dict key for corresponding lowercase letter!
        key_timings[char.lower()] = {"keyUp": None, "keyDown": None}

    if char == ".":
        key_timings["period"] = {"keyUp": None, "keyDown": None}
    else:
        key_timings[char] = {"keyUp": None, "keyDown": None}

key_timings["Return"] = {"keyUp": None, "keyDown": None}
# key_timings["Shift_L"] = {"keyUp": None, "keyDown": None}


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


# Create hookmanager
hookman = pyxhook.HookManager()
# Define our callback to fire when a key is pressed down
hookman.KeyDown = kb_down_event
# Define our callback to fire when a key is pressed down
hookman.KeyUp = kb_up_event

# Hook the keyboard
hookman.HookKeyboard()

# Start our listener
hookman.start()

# Create a loop to keep the application running
# running = True
# while running:
#     time.sleep(0.1)

input_pwd = input("Enter the password : ")
key_timings["Return"]["keyDown"] = time.time()
is_pwd_correct = False
if input_pwd == password:
    print("pwd correct!")
    is_pwd_correct = True

dataset_based_timings = dict()
dataset_based_timings["hold_time"] = dict()
dataset_based_timings["ud_key1_key2"] = dict()
dataset_based_timings["dd_key1_key2"] = dict()

print(json.dumps(key_timings))
if is_pwd_correct:
    # Calculate hold time of keys!
    for key in list(password):
        if key == ".":
            dataset_based_timings["hold_time"]["period"] = key_timings["period"]["keyDown"]-key_timings["period"]["keyUp"]
        elif key.isupper():
            try:
                dataset_based_timings["hold_time"][key] = key_timings[key.lower()]["keyDown"] - key_timings[key]["keyUp"]
            except Exception:
                dataset_based_timings["hold_time"][key] = key_timings[key]["keyDown"] - key_timings[key]["keyUp"]
        else:
            dataset_based_timings["hold_time"][key] = key_timings[key]["keyDown"]-key_timings[key]["keyUp"]

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
                dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = key_timings[key2.lower()]["keyDown"] - \
                                                                             key_timings[key1.lower()]["keyDown"]
                dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = key_timings[key2.lower()]["keyDown"] - \
                                                                                   key_timings[key1]["keyUp"]
            except Exception:
                dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = key_timings[key2]["keyDown"] - \
                                                                                   key_timings[key1]["keyDown"]
                dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = key_timings[key2]["keyDown"] - \
                                                                                   key_timings[key1]["keyUp"]
        else:
            dataset_based_timings["dd_key1_key2"]["DD." + key1 + "." + key2] = key_timings[key2]["keyDown"] - \
                                                                         key_timings[key1]["keyDown"]
            dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = key_timings[key2]["keyDown"] - \
                                                                               key_timings[key1]["keyUp"]

    dataset_based_timings["hold_time"]["Return"] = key_timings["Return"]["keyDown"] - key_timings["Return"]["keyUp"]
    dataset_based_timings["ud_key1_key2"]["UD." + list(password)[-1] + ".Return"] = key_timings["Return"]["keyDown"] - \
                                                                            key_timings[list(password)[-1]]["keyUp"]
    dataset_based_timings["dd_key1_key2"]["DD." + list(password)[-1] + ".Return"] = key_timings["Return"]["keyDown"] - \
                                                                            key_timings[list(password)[-1]]["keyDown"]


print(json.dumps(dataset_based_timings))


# Close the listener when we are done
hookman.cancel()

