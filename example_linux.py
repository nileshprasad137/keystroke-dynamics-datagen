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

password = "Abc."
keyTimings = dict()

for char in list(password):
    if char.isupper():
        # if character is uppercase, have an additional dict key for corresponding lowercase letter!
        keyTimings[char.lower()] = {"keyUp": None, "keyDown": None}

    if char == ".":
        keyTimings["period"] = {"keyUp": None, "keyDown": None}
    else:
        keyTimings[char] = {"keyUp": None, "keyDown": None}

keyTimings["Return"] = {"keyUp": None, "keyDown": None}
# keyTimings["Shift_L"] = {"keyUp": None, "keyDown": None}
print(keyTimings)


# This function is called every time a key is pressed down
def kb_down_event(event):
    global running

    try:
        keyTimings[event.Key]["keyUp"] = time.time()
    except KeyError:
        print("This key is not to be recorded : ", event.Key)
    print("Time currently:", time.time())
    # If the ascii value matches spacebnvear, terminate the while loop
    if event.Ascii == 13:
        running = False


# This function is called every time a keypress is released
def kb_up_event(event):
    global running
    # print key info
    # print(event.Key, " ", event.MessageName)
    try:
        keyTimings[event.Key]["keyDown"] = time.time()
    except KeyError:
        print("This key is not to be recorded : ", event.Key)
    print("Time currently:", time.time())
    # If the ascii value matches spacebar, terminate the while loop
    if event.Ascii == 13:
        running = False


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
keyTimings["Return"]["keyDown"] = time.time()
is_pwd_correct = False
if input_pwd == password:
    print("pwd correct!")
    is_pwd_correct = True

dataset_based_timings = dict()
dataset_based_timings["hold_time"] = dict()
dataset_based_timings["ud_key1_key2"] = dict()
dataset_based_timings["dd_key1_key2"] = dict()

if is_pwd_correct:
    # Calculate hold time of keys!
    print("in bool")
    for key in list(password):
        if key == ".":
            dataset_based_timings["hold_time"]["period"] = keyTimings["period"]["keyDown"]-keyTimings["period"]["keyUp"]
        elif key.isupper():
            dataset_based_timings["hold_time"][key] = keyTimings[key.lower()]["keyDown"] - keyTimings[key]["keyUp"]
        else:
            dataset_based_timings["hold_time"][key] = keyTimings[key]["keyDown"]-keyTimings[key]["keyUp"]

    for key1, key2 in zip(password, password[1:]):
        print(key1, " ", key2)
        # Calculate ud_k1_k2 and dd_k1_k2
        if key1 == "." or key2 == ".":
            if key1==".":
                key1 = "period"
            else:
                key2 = "period"
            dataset_based_timings["dd_key1_key2"]["DD."+key1+"."+key2] = keyTimings[key2]["keyDown"]-keyTimings[key1]["keyDown"]
            dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = keyTimings[key2]["keyDown"] - \
                                                                               keyTimings[key1]["keyUp"]
        elif key1.isupper() or key2.isupper():
            dataset_based_timings["dd_key1_key2"]["DD."+key1+"."+key2] = keyTimings[key2.lower()]["keyDown"] - keyTimings[key1.lower()]["keyDown"]
            dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = keyTimings[key2.lower()]["keyDown"] - \
                                                                               keyTimings[key1]["keyUp"]
        else:
            dataset_based_timings["dd_key1_key2"]["DD."+key1+"."+key2] = keyTimings[key2]["keyDown"]-keyTimings[key1]["keyDown"]
            dataset_based_timings["ud_key1_key2"]["UD." + key1 + "." + key2] = keyTimings[key2]["keyDown"] - \
                                                                               keyTimings[key1]["keyUp"]


print(json.dumps(dataset_based_timings))
print(json.dumps(keyTimings))

# Close the listener when we are done
hookman.cancel()

