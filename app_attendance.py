from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import pandas as pd
import os

# Load environment variables
load_dotenv()
hodUser = os.getenv("hodUser")
hodPass = os.getenv("hodpass")

# Hardcoded value for classes held (same for everyone)
CLASSES_HELD = 45

# Load CSV attendance data (Columns: USN, Attended)
df = pd.read_csv("attendance.csv")
attendance_dict = {
    row['USN'].strip(): int(row['OS_att'])
    for _, row in df.iterrows()
}


# Start browser
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
driver.maximize_window()
driver.get("https://uucms.karnataka.gov.in/Login/Index")

# Login
driver.find_element(By.ID, "txtUserName").send_keys(hodUser)
driver.find_element(By.ID, "txtPassword").send_keys(hodPass)

# Wait for manual login (CAPTCHA etc.)
input("🛑 Login manually and navigate to the Attendance Entry page. Then press Enter...")

time.sleep(3)

# Locate attendance table rows
rows = driver.find_elements(By.CSS_SELECTOR, "#tblStudentDetails tbody tr")

for i, row in enumerate(rows, start=1):
    try:
        columns = row.find_elements(By.TAG_NAME, "td")
        usn = columns[3].text.strip()

        if usn in attendance_dict:
            attended = attendance_dict[usn]

            # Locate input fields
            held_input = row.find_element(By.XPATH, ".//input[@name='item.noClassConducted']")
            attended_input = row.find_element(By.XPATH, ".//input[@name='item.noClassAttended']")

            # Enter values
            held_input.clear()
            held_input.send_keys(str(CLASSES_HELD))

            attended_input.clear()
            attended_input.send_keys(str(attended))

            print(f"✅ {usn}: Held={CLASSES_HELD}, Attended={attended}")
        else:
            print(f"❌ USN not in CSV: {usn}")

    except Exception as e:
        print(f"⚠️ Error on row {i}: {e}")

# Wait for review
input("✅ Done entering attendance. Press Enter to close browser...")
driver.quit()
