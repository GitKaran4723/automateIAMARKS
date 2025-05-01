from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from dotenv import load_dotenv
import pandas as pd

import os
load_dotenv()

hodUser = os.getenv("hodUser")
hodPass = os.getenv("hodpass")

# Load Excel
df = pd.read_csv("Internals.csv")  # your file with columns: 'USN', 'Marks'
marks_dict = dict(zip(df['USN'].astype(str).str.strip(), df['OS_Marks']))

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.maximize_window()
# Open the portal
driver.get("https://uucms.karnataka.gov.in/Login/Index")

# Enter login credentials
driver.find_element(By.ID, "txtUserName").send_keys(hodUser)
driver.find_element(By.ID, "txtPassword").send_keys(hodPass)

input("Enter Enter once Done")



# Find all rows in the marks table
rows = driver.find_elements(By.CSS_SELECTOR, "#InternalAssessmentMarksList tr")

for index, row in enumerate(rows, start=1):
    try:
        usn_element = row.find_elements(By.TAG_NAME, "td")[2]  # USN is in 3rd td
        usn = usn_element.text.strip()

        if usn in marks_dict:
            mark_input = row.find_element(By.ID, f"marksScored_{index}")
            mark_input.clear()
            mark_input.send_keys(str(marks_dict[usn]))
            print(f"✅ Entered {marks_dict[usn]} for {usn}")
        else:
            print(f"❌ USN {usn} not found in Excel")

    except Exception as e:
        print(f"⚠️ Error processing row {index}: {e}")

# Keep the browser open for review
input("✅ Attendance entry done. Press Enter to close...")
driver.quit()