# SmartFileOrganizer

SmartFileOrganizer is a flexible Python-based tool that helps you automatically organize files in any folder based on **file type**, **date**, or **both** — keeping your directories clean, efficient, and easy to navigate.

## 🚀 Features
- Organize files by:
  - File Type (e.g., PDFs, Images, Executables)
  - Date (e.g., organized into Year-Month folders)
  - Combination of File Type and Date
- Customizable target folder (choose any folder you want)
- Automatically creates necessary subfolders if they don't exist
- Detailed logging of all operations
- Easy to schedule (with Task Scheduler, cron jobs, etc.)

## 📂 Example Folder Structures
**By Type:**
```
Downloads/
├── PDFs/
├── Images/
├── Videos/
```

**By Date:**
```
Downloads/
├── 2025-04/
├── 2025-05/
```

**By Both:**
```
Downloads/
├── PDFs/
│   ├── 2025-04/
│   ├── 2025-05/
├── Images/
│   ├── 2025-04/
│   ├── 2025-05/
```

## 🛠️ Requirements
- Python 3.7+
- Libraries:
  - os
  - shutil
  - datetime
  - logging
  - (Optional: watchdog for real-time monitoring)

Install any additional dependencies with:
```
pip install -r requirements.txt
```

## ⚙️ How to Use
1. Clone this repository:
```
git clone https://github.com/yourusername/SmartFileOrganizer.git
```
2. Navigate to the project directory:
```
cd SmartFileOrganizer
```
3. Run the script:
```
python main.py
```
4. Follow the prompts to:
   - Enter the folder path you want to organize
   - Choose your preferred organization method (type, date, or both)

## 📅 Automation
- **Windows:** Set up a Task Scheduler job to run `main.py` periodically
- **Linux/macOS:** Set up a cron job (e.g., daily organization)

## 🚀 Project Badges

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue?logo=python&style=for-the-badge" alt="Python Version">
  <a href="https://github.com/NikhilKKYakkala/SmartFileOrganizer/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/NikhilKKYakkala/SmartFileOrganizer?style=for-the-badge" alt="License">
  </a>
  <a href="https://github.com/NikhilKKYakkala/SmartFileOrganizer/actions">
    <img src="https://img.shields.io/github/actions/workflow/status/NikhilKKYakkala/SmartFileOrganizer/python-app.yml?branch=main&style=for-the-badge" alt="Build Status">
  </a>
  <a href="https://github.com/NikhilKKYakkala/SmartFileOrganizer">
    <img src="https://img.shields.io/github/last-commit/NikhilKKYakkala/SmartFileOrganizer?style=for-the-badge" alt="Last Commit">
  </a>
</p>

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.