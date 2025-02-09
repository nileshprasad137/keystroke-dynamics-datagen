"""
Keystroke Dynamics Recorder 
- Uses object-oriented programming (OOP)
- Compatible with MacOS/Linux (pynput)
- Stores data in JSON format for ML training
"""

import time
import json
import logging
from pathlib import Path
from pynput import keyboard

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class KeystrokeRecorder:
    """
    A class to record keystroke dynamics for user authentication.
    """
    
    DEFAULT_PASSWORD = ".tie5Roanl"
    FREQUENCY_PASSWORD_ENTRY = 10  # Number of times password needs to be typed
    
    def __init__(self):
        """
        Initializes key timing data structures and sets up the listener.
        """
        self.user_name = ""
        self.password_entry_count = 1
        self.key_timings = {}
        self.user_keystroke_timings_list = []
        self.user_keystroke_timings_json = {}
        
        # Ensure proper key storage format
        for char in list(self.DEFAULT_PASSWORD):
            normalized_char = char.lower() if char.isalpha() else char
            self.key_timings[normalized_char] = {"keyUp": None, "keyDown": None}

        self.key_timings["return"] = {"keyUp": None, "keyDown": None}  # Handling Return key
        
        logging.info("Keystroke recorder initialized.")

    def start_recording(self):
        """
        Starts the recording process for the user.
        """
        self.user_name = input("Enter your name: ").strip()
        logging.info(f"User '{self.user_name}' started recording.")

        with keyboard.Listener(on_press=self.kb_down_event, on_release=self.kb_up_event) as listener:
            while self.password_entry_count <= self.FREQUENCY_PASSWORD_ENTRY:
                print(f"Enter {1 + self.FREQUENCY_PASSWORD_ENTRY - self.password_entry_count} times more!")
                input_pwd = input(f"Enter '{self.DEFAULT_PASSWORD}': ").strip()

                if input_pwd == self.DEFAULT_PASSWORD:
                    logging.info(f"Password correctly entered for attempt {self.password_entry_count}.")
                    self.process_keystroke_data()
                    self.password_entry_count += 1
                else:
                    logging.warning("Incorrect password entered. Retrying...")

            listener.stop()  # Stop the keyboard listener when done

        self.save_data()
        print("Keystroke data saved successfully!")
        logging.info("Keystroke recording session completed.")

    def kb_down_event(self, key):
        """
        Handles key press events.
        """
        try:
            key_str = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
            if key_str in self.key_timings:
                self.key_timings[key_str]["keyDown"] = time.time()
        except AttributeError:
            pass  # Ignore special function keys

    def kb_up_event(self, key):
        """
        Handles key release events.
        """
        try:
            key_str = key.char.lower() if hasattr(key, 'char') and key.char else key.name.lower()
            if key_str in self.key_timings:
                self.key_timings[key_str]["keyUp"] = time.time()
        except AttributeError:
            pass

    def process_keystroke_data(self):
        """
        Processes keystroke timing data for ML use.
        """
        dataset_based_timings = {
            "hold_time": {},
            "ud_key1_key2": {},
            "dd_key1_key2": {},
            "password_entry_count": self.password_entry_count
        }

        # Compute Hold Time
        for key in self.DEFAULT_PASSWORD:
            normalized_key = key.lower()
            if self.key_timings[normalized_key]["keyUp"] and self.key_timings[normalized_key]["keyDown"]:
                dataset_based_timings["hold_time"][normalized_key] = (
                    self.key_timings[normalized_key]["keyUp"] - self.key_timings[normalized_key]["keyDown"]
                )

        # Compute Keydown-Keydown & Keyup-Keydown Intervals
        for key1, key2 in zip(self.DEFAULT_PASSWORD, self.DEFAULT_PASSWORD[1:]):
            key1_norm, key2_norm = key1.lower(), key2.lower()

            if self.key_timings[key2_norm]["keyDown"] and self.key_timings[key1_norm]["keyDown"]:
                dataset_based_timings["dd_key1_key2"][f"DD.{key1_norm}.{key2_norm}"] = (
                    self.key_timings[key2_norm]["keyDown"] - self.key_timings[key1_norm]["keyDown"]
                )

            if self.key_timings[key2_norm]["keyDown"] and self.key_timings[key1_norm]["keyUp"]:
                dataset_based_timings["ud_key1_key2"][f"UD.{key1_norm}.{key2_norm}"] = (
                    self.key_timings[key2_norm]["keyDown"] - self.key_timings[key1_norm]["keyUp"]
                )

        # Compute Return Key Intervals
        dataset_based_timings["hold_time"]["return"] = (
            self.key_timings["return"]["keyUp"] - self.key_timings["return"]["keyDown"]
        ) if self.key_timings["return"]["keyUp"] and self.key_timings["return"]["keyDown"] else None

        dataset_based_timings["ud_key1_key2"][f"UD.{self.DEFAULT_PASSWORD[-1]}.return"] = (
            self.key_timings["return"]["keyDown"] - self.key_timings[self.DEFAULT_PASSWORD[-1].lower()]["keyUp"]
        ) if self.key_timings["return"]["keyDown"] and self.key_timings[self.DEFAULT_PASSWORD[-1].lower()]["keyUp"] else None

        dataset_based_timings["dd_key1_key2"][f"DD.{self.DEFAULT_PASSWORD[-1]}.return"] = (
            self.key_timings["return"]["keyDown"] - self.key_timings[self.DEFAULT_PASSWORD[-1].lower()]["keyDown"]
        ) if self.key_timings["return"]["keyDown"] and self.key_timings[self.DEFAULT_PASSWORD[-1].lower()]["keyDown"] else None

        self.user_keystroke_timings_list.append(dataset_based_timings)

    def save_data(self):
        """
        Saves recorded keystroke data to a JSON file.
        """
        self.user_keystroke_timings_json["timings"] = self.user_keystroke_timings_list
        self.user_keystroke_timings_json["user"] = self.user_name

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)  # Ensure output directory exists

        output_file = output_dir / f"{self.user_name}_timings.json"
        with output_file.open('w') as outfile:
            json.dump(self.user_keystroke_timings_json, outfile, indent=4)

        logging.info(f"Keystroke data saved to {output_file}")


if __name__ == "__main__":
    recorder = KeystrokeRecorder()
    recorder.start_recording()
