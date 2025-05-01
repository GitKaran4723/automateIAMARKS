# Automation of Marks Entry

## ✅ Features

- Login manually to bypass CAPTCHA
- Matches student USNs from Excel with those on the portal
- Automatically fills in the corresponding marks
- Logs missing USNs or errors

## 📦 Requirements

- Python 3.8+
- Google Chrome (updated)
- ChromeDriver (managed automatically)
- A valid `.env` file with login credentials (if used)

## 🔧 Setup Instructions

### 1. Install dependencies

```
pip install selenium pandas openpyxl python-dotenv webdriver-manager
```

### 2. Prepare a `.env` file

- Add the following details in the file
- This is to secure the credentials 

```
hodUser=your_username
hodpass=your_password
```

### 3. Prepare `marks.xlsx`

| USN           | Marks |
|---------------|-------|
| U03NK24S0027  | 23    |
| U03NK24S0043  | 25    |

### 4. Run the script

```
python app.py
```

