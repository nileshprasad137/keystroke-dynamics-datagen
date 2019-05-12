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
frequency_password_entry = 10
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
        # if event.Key == "Return":
        #     print("key_timings[{}][\"keyUp\"]::{}".format(event.Key, key_timings[event.Key]["keyUp"]))
        # print("key_timings[{}][\"keyUp\"]::{}".format(event.Key,key_timings[event.Key]["keyUp"]))
    except KeyError:
        # print("This key is not to be recorded : ", event.Key)
        pass


# This function is called every time a keypress is released
def kb_up_event(event):
    try:
        key_timings[event.Key]["keyDown"] = time.time()
        # if event.Key == "Return":
        #     print("key_timings[{}][\"keyDown\"]::{}".format(event.Key, key_timings[event.Key]["keyDown"]))
    except KeyError:
        # print("This key is not to be recorded : ", event.Key)
        pass

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

while password_entry_count <= frequency_password_entry:
    print("enter {} times more!".format(1+frequency_password_entry-password_entry_count))
    input_pwd = input("Enter \'{}\' : ".format(password))
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

        # print(json.dumps(key_timings))

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

        time.sleep(1)
        # print(json.dumps(key_timings))
        # print("Ret KD :: ",key_timings["Return"]["keyDown"])
        # print("Ret KU :: ", key_timings["Return"]["keyUp"])
        # print(key_timings["Return"]["keyDown"] - key_timings["Return"]["keyUp"])
        dataset_based_timings["hold_time"]["Return"] = key_timings["Return"]["keyDown"] - key_timings["Return"]["keyUp"]
        dataset_based_timings["ud_key1_key2"]["UD." + list(password)[-1] + ".Return"] = \
            key_timings["Return"]["keyDown"] - key_timings[list(password)[-1]]["keyUp"]
        dataset_based_timings["dd_key1_key2"]["DD." + list(password)[-1] + ".Return"] = \
            key_timings["Return"]["keyDown"] - key_timings[list(password)[-1]]["keyDown"]

        user_keystroke_timings_list.append(dataset_based_timings)

    else:
        print("Password entered was not correct! Please type \'{}\' again !".format(password))

user_keystroke_timings_json["timings"] = user_keystroke_timings_list
user_keystroke_timings_json["user"] = user_name
print(json.dumps(user_keystroke_timings_json))


rows = []

hold_time_user = []
dd_key1_key2_user = []
ud_key1_key2_user = []
cnt = 1
data = user_keystroke_timings_json
for timing in data['timings']:
    hold_time_user.append(timing["hold_time"])
    dd_key1_key2_user.append(timing["dd_key1_key2"])
    ud_key1_key2_user.append(timing["ud_key1_key2"])
    row = dict()
    for key in timing["hold_time"].keys():
        if key == "5":
            new_key = "H.five"
        elif key == "R":
            new_key = "H.Shift.r"
        else:
            new_key = "H."+key
        row[new_key] = timing["hold_time"][key]
    for key in timing["dd_key1_key2"].keys():
        if key == "DD.5.R":
            new_key = "DD.five.Shift.r"
        elif key == "DD.R.o":
            new_key = "DD.Shift.r.o"
        elif key == "DD.e.5":
            new_key = "DD.e.five"
        else:
            new_key = key
        row[new_key] = timing["dd_key1_key2"][key]
    for key in timing["ud_key1_key2"].keys():
        if key == "UD.5.R":
            new_key = "UD.five.Shift.r"
        elif key == "UD.R.o":
            new_key = "UD.Shift.r.o"
        elif key == "UD.e.5":
            new_key = "UD.e.five"
        else:
            new_key = key
        row[new_key] = timing["ud_key1_key2"][key]
        # print(key)
    row["subject"] = "nilesh"
    row["rep"] = cnt
    row["sessionIndex"] = 1
    rows.append(row)
    cnt += 1

print(rows)
column_names = ["H.period", "DD.period.t", "UD.period.t", "H.t", "DD.t.i", "UD.t.i", "H.i",	"DD.i.e", "UD.i.e", "H.e",
                "DD.e.five", "UD.e.five", "H.five", "DD.five.Shift.r", "UD.five.Shift.r", "H.Shift.r", "DD.Shift.r.o",
                "UD.Shift.r.o", "H.o", "DD.o.a", "UD.o.a", "H.a", "DD.a.n", "UD.a.n",	"H.n", "DD.n.l", "UD.n.l",
                "H.l", "DD.l.Return", "UD.l.Return", "H.Return"]

row_value_list = list()
for column_name in column_names:
    row_value_list.append(rows[0][column_name])
# row_value_list.append(rows[0]['DD.period.t'])
print(row_value_list)

with open('output/{}_timings.json'.format(user_name), 'w') as outfile:
    json.dump(user_keystroke_timings_json, outfile)

# Close the listener when recording is done!
hookman.cancel()
