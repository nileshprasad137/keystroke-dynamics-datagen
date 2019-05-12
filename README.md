# keystroke-dynamics-datagen

Generates dataset for the study of typing patterns of people to distinguish 
them from one another.

---------------------------------------------

Records three features:

##### Hold time – time between press and release of a key.
##### Keydown-Keydown time – time between the pressing of consecutive keys.
##### Keyup-Keydown time – time between the release of one key and the press of next key.

Generates JSON for the timings.

----------------------------------------------------------------------------------------

Refer [this paper](http://www.cs.cmu.edu/~keystroke/) for dataset format!

---------------------------------------------------------------------------------


Run `record_keystroke.py`  to see it in action.

#### Detailed Instructions 
* Clone the repository.
* Keep a copy of `DSL-StrongPasswordData.csv` in `edited_dataset` folder. Note- **Let the original dataset stay in root folder.**
* Run `record_keystroke.py` and provide name for user who is recording the keystrokes in the format `[username]_rep[count_of_recording]`. EX. Nilesh_rep1
* You can modify the number of recordings in one execution by modifying `frequency_password_entry` inside `record_keystroke.py`. This will generate JSON of keystroke timings in `output/` folder for any future use. 
* Run `append_in_dataset.py` by providing the username you had provided during running record script.
EX. if you had given username as "xyz_rep1". Give "xyz" as the input here.
* Your keystrokes will be appended in the dataset in `edited_dataset` folder. Original dataset is not affected.


#### Note

This script works only for Linux Based Systems as `pyxhook` is for Linux. `PyHook` or `keyboard` modules can be used for developing relevant scripts for Windows. 

Contributions highly appreciated!

