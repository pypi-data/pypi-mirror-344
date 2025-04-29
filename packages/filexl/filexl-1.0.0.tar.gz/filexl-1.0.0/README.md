# 📂 filexl

A simple Python CLI tool to list all files in a given directory and export them to an Excel file. Supports filtering by file extension, optional path naming, and detection of duplicate file names.

---

## 🚀 Features

- 🔍 Recursively lists all files in a directory (including hidden files)
- 📝 Outputs to Excel with columns:
  - File Name
  - Extension
  - Full Path
  - Path Name (optional)
- 🔁 Appends to existing Excel files
- 🎯 Filter by file extension (`--ext`)
- 🔎 Export only duplicate file names with `--only-duplicates`
- 🔠 Optional case-insensitive extension filtering
- ✅ Simple CLI interface with `--help` support

---

## 🧰 Installation

```bash
git clone https://github.com/kiarash-gh/filexl
cd filexl
pip install .
```

## 📦 Usage

Basic usage
```
filexl --path D:\data

```

With optional path name and Excel file name
```
filexl --path D:\data --name "MyData" --filename myfiles.xlsx

```

Filter by extensions (space or comma-separated)
```
filexl --path D:\images --ext .jpg .png --ignore-case

```

Export only duplicate file names
```
# With default output name (duplicates.xlsx)
filexl --path D:\data --only-duplicates

# Or with a custom output file
filexl --path D:\data --only-duplicates mydups.xlsx

```

## 🧪 Example Output

| File Name | Extension | Path                              | Path Name |
|-----------|-----------|-----------------------------------|-----------|
| report    | pdf       | D:\docs\2023\report.pdf           | Documents |
| report    | pdf       | D:\docs\2022\report.pdf           | Documents |
| image     | jpg       | D:\media\photos\image.jpg         | Media     |
| notes     | txt       | D:\projects\docs\notes.txt        | Projects  |

## 🧱 Development
To build a standalone executable:
```
pip install pyinstaller
pyinstaller --onefile filexl/cli.py

```

## 📜 License
MIT License. Use it freely in your own projects!

## 👨‍💻 Author
Developed by Kiarash Gharahgozloo
GitHub: @kiarash-gh