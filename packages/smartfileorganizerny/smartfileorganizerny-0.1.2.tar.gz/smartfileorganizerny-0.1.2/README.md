# SmartFileOrganizer

SmartFileOrganizer is a flexible Python-based tool that helps you automatically organize files in any folder based on **file type**, **date**, or **both** — keeping your directories clean, efficient, and easy to navigate.

---

## 🔥 Features

- **Organize by File Type**: PDFs, Images, Videos, etc.
- **Organize by Date**: Sort files into year-month folders.
- **Flexible Organization**: Combine both type and date-based sorting.
- **Customizable Folder**: Choose any target folder to organize.
- **Automatic Folder Creation**: Creates subfolders automatically if they don't exist.
- **Detailed Logging**: Provides logs for all operations.
- **Easy Scheduling**: Can be run via Task Scheduler (Windows) or Cron Jobs (Linux/macOS).

---

## 🚀 Getting Started

You can use Smart File Organizer in **two ways**:

---

### 1. Install as a Python Package (Recommended)

- **Install from PyPI**:

  ```bash
  pip install smartfileorganizerny
  ```

- **Use it directly in your code**:

  ```python
  from smartfileorganizerny import organizer

  organizer.start()
  ```

This is the easiest and most flexible way to use the project.

---

### 2. Clone the Repository

- **Clone the GitHub repository**:

  ```bash
  git clone https://github.com/NikhilKKYakkala/SmartFileOrganizer.git
  cd SmartFileOrganizer
  ```

- **Install dependencies**:

  ```bash
  pip install -r requirements.txt
  ```

- **Run the script manually**:

  ```bash
  python src/main.py
  ```

Follow the on-screen prompts to specify the folder and preferred organization method.

---

## 📁 Example Folder Structures

**By Type**:

```
Downloads/
├── PDFs/
├── Images/
├── Videos/
```

**By Date**:

```
Downloads/
├── 2025-04/
├── 2025-05/
```

**By Both Type and Date**:

```
Downloads/
├── PDFs/
│   ├── 2025-04/
│   ├── 2025-05/
├── Images/
│   ├── 2025-04/
│   ├── 2025-05/
```
---

## 🔄 Automation

You can schedule Smart File Organizer to run automatically at specific intervals:

- **Windows**: Use Task Scheduler
- **Linux/macOS**: Use Cron Jobs

Example: Organize your "Downloads" folder every night automatically!

---

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

---

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes.
4. Submit a pull request.

Please follow best coding practices and update documentation as needed.

---

## ✨ Future Improvements

- Duplicate File Detection and Management
- File Encryption Option
- Cloud Storage Integration (Google Drive, Dropbox, etc.)
- Graphical User Interface (GUI)

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).