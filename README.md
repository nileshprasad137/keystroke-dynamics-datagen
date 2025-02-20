# Keystroke-Dynamics-DataGen

A dataset generator for **keystroke dynamics research**—a biometric technique to **distinguish users based on their typing patterns**.

This tool records **keystroke timing features** and generates **JSON-formatted datasets**, which can be used for **user authentication, security applications, and behavioral biometrics research**.

---

## **📌 Features Recorded**
This script captures three **key typing characteristics**:

✔ **Hold Time** – Duration between key press (`keydown`) and key release (`keyup`).  
✔ **Keydown-Keydown Time** – Time between pressing two consecutive keys (`keydown` → `keydown`).  
✔ **Keyup-Keydown Time** – Time between releasing one key and pressing the next (`keyup` → `keydown`).  

👉 **Refer to this research paper** 📄 [Keystroke Dynamics by CMU](http://www.cs.cmu.edu/~keystroke/) for dataset format.

---

## **🚀 Getting Started**
### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/nileshprasad137/keystroke-dynamics-datagen.git
cd keystroke-dynamics-datagen
```

### **2️⃣ Set Up the Environment**
Create a virtual environment and install dependencies.
```bash
python3 -m venv .venv
source .venv/bin/activate  # For Linux & macOS
# On Windows, use: .venv\Scriptsctivate
pip install -r requirements.txt
```

### **3️⃣ Prepare the Dataset**
- Place the **original dataset** (`DSL-StrongPasswordData.csv`) in the **root folder**.
- Copy the dataset into the `edited_dataset/` folder for **appending new data** without modifying the original file.

---

## **🎬 Running the Keystroke Recorder**
**To record keystrokes, run the script:**
```bash
python record_keystroke.py
```
🔹 The script will prompt you to **enter a name** for the user recording the keystrokes, e.g., **"Nilesh_rep1"**.  
🔹 Modify `frequency_password_entry` inside `record_keystroke.py` to set how many times the user needs to enter the password.  
🔹 The script will generate **keystroke timing data in JSON format** inside the `output/` folder.  

### **Example**
```bash
Enter your name: Nilesh_rep1
Enter '.tie5Roanl': .tie5Roanl
Password correct!
Keystroke data saved successfully!
```
✅ Output will be stored as:  
```
output/Nilesh_rep1_timings.json
```

---

## **📌 Appending New Keystroke Data to Dataset**
Once recordings are complete, run the script below to append the new data to `edited_dataset/`:
```bash
python append_in_dataset.py
```
✔ If you entered the username **"Nilesh_rep1"**, provide `"Nilesh"` as input when prompted.  
✔ Your recorded keystrokes will be **added to the dataset** in the `edited_dataset/` folder.  
✔ **Original dataset remains unaffected**.  

---

## **🔹 Supported Platforms**
✅ **Linux & macOS** (Uses `pynput` instead of `pyxhook`).  
✅ **Windows Compatibility** → Future support using `keyboard` module.  

---

## **🛠️ Modifications & Customizations**
**You can modify the following parameters:**
| Parameter  | Description |
|------------|-------------|
| `frequency_password_entry` | Number of times the user must enter the password. |
| `DEFAULT_PASSWORD` | Change the predefined password to match your study. |
| `record_keystroke.py` | Modify the script to capture additional typing features. |

---

## **📢 Contributions & Improvements**
🚀 **Looking for contributors!**  
We welcome contributions to:  
✔ Improve **cross-platform compatibility** (Windows support).  
✔ Enhance **data visualization tools** for keystroke analysis.  
✔ Add **ML models** for authentication & anomaly detection.  

**To contribute:**  
1. Fork the repository.  
2. Create a feature branch (`git checkout -b feature-new`).  
3. Commit changes (`git commit -m "Added Windows support"`).  
4. Push the branch (`git push origin feature-new`).  
5. Submit a pull request.  

🙌 **Contributions are highly appreciated!**  

---

## **📜 License**
This project is licensed under the **MIT License**. Feel free to use, modify, and distribute.

---

## **🔗 Related Work**
- 📄 **Research Paper on Keystroke Dynamics** → [CMU Keystroke Study](http://www.cs.cmu.edu/~keystroke/)  
- 🔍 **Example Use Cases** → Behavioral biometrics, continuous authentication, fraud detection.  
- 🏆 **Potential Applications** → Banking security, anti-bot verification, identity protection.  

---

💡 **Need Help?**
📧 Contact: **nileshprasad137@gmail.com**  
🚀 **Star this repo if you found it useful!** ⭐
