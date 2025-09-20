# Heart-Disease-Predictor
Predicting Coronary Heart-Disease using Machine Learning models


# ❤️ Heart Disease Predictor Working and Setup

A machine learning–powered desktop and web application that predicts the likelihood of heart disease using **Logistic Regression**, **Random Forest**, and **SVM** with ~80–85% accuracy.  

Built with **Python, Flask, scikit-learn, pywebview, and PyInstaller**, this project demonstrates both a **Flask backend API** and a **standalone desktop GUI app**.

---

## 📖 Description
The application predicts heart disease risk from clinical features (age, sex, blood pressure, cholesterol, etc.) and provides:
- A **Flask API** (for integration with other systems).  
- A **native desktop GUI** (packaged with PyInstaller using pywebview).  

⚠️ **Note:** This is a decision-support demo project. It is **not a medical diagnosis tool**.

---

## 🛠 Tech Stack
- **Python 3.10+**
- **Flask** — lightweight web framework for API and UI.  
- **pywebview** — desktop-native window wrapper for the Flask app.  
- **scikit-learn, pandas, numpy** — ML models and data processing.  
- **PyInstaller** — for packaging as an `.exe` desktop app.  

---

## 📊 Machine Learning Models
Trained on the classic heart disease dataset, evaluated with ~80–85% accuracy:
- **Logistic Regression** — interpretable, efficient baseline.  
- **Random Forest** — ensemble model for robust predictions.  
- **SVM (Support Vector Machine)** — effective on complex feature spaces.  

---

## 🚀 Setup & Run (Development Mode)

### 1. Clone the repo
```bash
git clone https://github.com/your-username/Heart-Disease-Predictor.git
cd Heart-Disease-Predictor
````

### 2. Create & activate a virtual environment

```powershell
# Windows PowerShell
python -m venv venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
.\venv\Scripts\Activate.ps1
```

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

### 4. Run the app

* **Flask API only**:

  ```bash
  python app.py
  ```

  → Visit [http://127.0.0.1:5000](http://127.0.0.1:5000)

* **Desktop GUI**:

  ```bash
  python run_gui.py
  ```

  → Opens a native window with the app.

---

## 📦 Build as Desktop Application

### 1. Install PyInstaller

```bash
pip install pyinstaller
```

### 2. Build the app (one-folder mode)

```powershell
python -m PyInstaller --onedir --noconsole --icon "icon.ico" `
  --collect-submodules sklearn --collect-submodules numpy `
  --add-data "backend/models;backend/models" `
  --add-data "templates;templates" `
  --add-data "static;static" `
  run_gui.py
```

* Output: `dist/run_gui/run_gui.exe`
* Logs: `dist/run_gui/logs/run_gui.log` (for debugging crashes).

### 3. Create a Desktop shortcut

Manually: right-click `dist/run_gui/run_gui.exe` → *Send to* → Desktop (shortcut).
Or use this PowerShell snippet:

```powershell
$exePath = (Resolve-Path ".\dist\run_gui\run_gui.exe").Path
$desktop = [Environment]::GetFolderPath("Desktop")
$shell = New-Object -ComObject WScript.Shell
$lnk = $shell.CreateShortcut("$desktop\Heart Disease Predictor.lnk")
$lnk.TargetPath = $exePath
$lnk.WorkingDirectory = Split-Path $exePath
$lnk.IconLocation = "$exePath,0"
$lnk.Save()
```

---

## 🐛 Troubleshooting

* **`python not found`** → Install Python from [python.org](https://www.python.org/downloads/) and re-open PowerShell.
* **`Activate.ps1 cannot be loaded`** → Run:

  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
  ```
* **Pywebview window doesn’t open** → Ensure [WebView2 Runtime](https://developer.microsoft.com/en-us/microsoft-edge/webview2/) is installed (Evergreen Bootstrapper x64).
* **`TypeError: create_window() got an unexpected keyword argument 'icon'`** → Fixed (pywebview v6.0 does not support `icon=`; exe icon is set by PyInstaller).
* **Missing module errors in exe** → Rebuild with `--collect-submodules sklearn --collect-submodules numpy`.

---

## 🖼 Screenshots

* **Positive Prediction (Heart Disease Detected)**
    <img width="2519" height="1544" alt="Screenshot 2025-09-20 143309" src="https://github.com/user-attachments/assets/919c1fec-fbb0-4577-a699-0301b1155ddb" />
    
    <img width="2517" height="1412" alt="Screenshot 2025-09-20 143323" src="https://github.com/user-attachments/assets/5d9059de-8c68-458a-9de9-0fc577500d94" />

 
* **Negative Prediction (No Heart Disease)**
   <img width="2537" height="1526" alt="Screenshot 2025-09-20 143418" src="https://github.com/user-attachments/assets/31a4636c-a7aa-46d5-a6b5-30c922fc7789" />

   <img width="2522" height="1479" alt="Screenshot 2025-09-20 143433" src="https://github.com/user-attachments/assets/ba21d15c-0fb9-4ea8-a3d3-82f62a154631" />


Conclusion

A compact, accurate (80–85%), and user-friendly system demonstrating **ML-powered health risk prediction**, delivered as both a **Flask API** and a **desktop GUI app**.


