from tkinter import *

from tkinter import messagebox

import tkinter as tk
from tkinter import ttk

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
from datetime import datetime
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.print_page_options import PrintOptions
import base64
import math

currentScriptDirectoryPath = os.path.dirname(os.path.abspath(__file__))
currentScriptDirectoryPathFiles = os.listdir(currentScriptDirectoryPath)

sys.path.append(currentScriptDirectoryPath)

downloadDefaultDirectory = '.'
headlessmode = False
options = webdriver.ChromeOptions()
options_test = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox");
options.add_argument("--disable-dev-shm-usage");
options.add_argument("--disable-renderer-backgrounding");
options.add_argument("--disable-background-timer-throttling");
options.add_argument("--disable-backgrounding-occluded-windows");
options.add_argument("--disable-client-side-phishing-detection");
options.add_argument("--disable-crash-reporter");
options.add_argument("--disable-oopr-debug-crash-dump");
options.add_argument("--no-crash-upload");
options.add_argument("--disable-gpu");
options.add_argument("--disable-extensions");
options.add_argument("--disable-low-res-tiling");
options.add_argument("--log-level=3");
options.add_argument("--silent");
options.add_argument("--disable-search-engine-choice-screen")
options.add_argument("--headless=new")
options.add_argument("--window-position=-2400,-2400")
def_dir=os.path.join(currentScriptDirectoryPath, 'user_data')
print(def_dir)
options.add_argument("--user-data-dir="+def_dir)
options.add_argument("--profile-directory=Profile 1")
options_test.add_argument("--user-data-dir="+def_dir)
options_test.add_argument("--profile-directory=Profile 1")
options_test.add_argument("--disable-search-engine-choice-screen")
prefs = {
    'download.default_directory': downloadDefaultDirectory,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing_for_trusted_sources_enabled": False,
    "safebrowsing.enabled": False
}
options.add_experimental_option('prefs', prefs)
options_test.add_experimental_option('prefs', prefs)
if not headlessmode:
   selected_options = options_test
else:
   selected_options = options
driver = webdriver.Chrome(options=selected_options)

# main window
root = tk.Tk()
root.geometry("400x300")
root.title('Login')

# Frame hinzufügen
frame = ttk.Frame(root, padding=10)
frame.rowconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(2, weight=1)
frame.rowconfigure(3, weight=1)
frame.rowconfigure(4, weight=1)
frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=3)
frame.grid()

# username
username_label = ttk.Label(frame, text="Email:")
username_label.grid(column=0, row=0, sticky=tk.EW, padx=5, pady=5)

username_entry = ttk.Entry(frame)
username_entry.grid(column=1, row=0, sticky=tk.EW, padx=5, pady=5)

# password
password_label = ttk.Label(frame, text="Password:")
password_label.grid(column=0, row=1, sticky=tk.EW, padx=5, pady=5)

password_entry = ttk.Entry(frame,  show="*")
password_entry.grid(column=1, row=1, sticky=tk.EW, padx=5, pady=5)

# auth_code
auth_code_label = ttk.Label(frame, text="Auth code:")
auth_code_label.grid(column=0, row=2, sticky=tk.EW, padx=5, pady=5)

auth_code_entry = ttk.Entry(frame, text="0123456")
auth_code_entry.grid(column=1, row=2, sticky=tk.EW, padx=5, pady=5)

# btc
btc_label = ttk.Label(frame, text="bitcoin value:")
btc_label.grid(column=0, row=3, sticky=tk.EW, padx=5, pady=5)

btc_value = ttk.Entry(frame, text="5.0")
btc_value.grid(column=1, row=3, sticky=tk.EW, padx=5, pady=5)

def add_ex_to_chrome(extension_url='https://chromewebstore.google.com/detail/todoist-for-chrome-planne/jldhpllghnbhlbpcmnajkpdmadaolakh'):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.common.keys import Keys
    import time
    import pyautogui

    # Set up Chrome options
    #chrome_options = Options()

    # Path to your ChromeDriver
    #chrome_driver_path = 'chromedriverPath'

    # Initialize ChromeDriver with the specified options
    #service = Service(chrome_driver_path)
    #driver = webdriver.Chrome(service=service, options=chrome_options)

    # Go to the Chrome Web Store URL of the desired extension
    driver.get(extension_url)
    driver.maximize_window();

    # Wait for the page to load
    time.sleep(5)  # Adjust time as needed

    actions = ActionChains(driver)
    try:
       # Find the "Add to Chrome" button
       try:
           add_to_chrome_button = driver.find_element(By.XPATH, '//button[span[contains(text(),"Add to Chrome")]]')
       except:
           add_to_chrome_button = driver.find_element(By.XPATH, '//button[span[contains(text(),"Hinzufügen")]]')

       # Click the "Add to Chrome" button
       add_to_chrome_button.click()
    
       time.sleep(8)
       pyautogui.press('tab', presses=1)
       time.sleep(3)
    
       # Use PyAutoGUI to press Enter to confirm "Add to Extension"
       pyautogui.press('enter')
    
       # Wait for the "Add Extension" confirmation dialog
       time.sleep(2)
    except Exception as e:
       print(f"An error occurred: {e}")

    # Wait to observe the added extension
    time.sleep(5)
    # Close the browser
    #driver.quit()

threads=[]
def poll_emails(email):
    import os
    os.system('@poll_byom_emails_for_switchere.exe ' + email)
    
def write_auth_code():
    import pyperclip
    while True:
        old_text=auth_code_entry.get()
        text=pyperclip.paste()
        if text.isdigit() and not old_text == text:
           auth_code_entry.delete(0,END)
           auth_code_entry.insert(0,text)

def login_action_part_one():
    user = username_entry.get()
    import re
    # Execute a shell command
    if len(user) > 0:
       email = re.findall(r'([\w\.-]+@[\w\.-]+(?:\.[\w]+)+)',user)
       print(email)
       if len(email) > 0 and email[0].endswith("@byom.de"):
          import threading
          emailt=email[0]
          print(emailt)
          t = threading.Thread(target=poll_emails, args=[emailt])
          t.start()
          t2 = threading.Thread(target=write_auth_code, args=[])
          t2.start()

def login_action_part_second():    
    #add_ex_to_chrome("https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo")
    user = username_entry.get()
    passw = password_entry.get()
    btcv = btc_value.get()
    haveLogin = False
    closeDriver = False
    
    driver.get("https://switchere.com/sign-up")
    user = "werr@byom.de"
    email_input = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#email-input")))
    if len(user) > 0:
       email = re.findall(r'([\w\.-]+@[\w\.-]+(?:\.[\w]+)+)',user)
       if len(email) > 0 and email[0].endswith("@byom.de"):
          emailt=email[0]
          email_input.send_keys(" and some", Keys.ENTER)
def login_action():
    login_action_part_one()
    login_action_part_second()
    
# login button
login_button = ttk.Button(frame, text="Login", command=login_action)
login_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

# get_auth_code
get_auth_code = ttk.Button(frame, text="Get auth code", command=root.destroy)
get_auth_code.grid(column=2, row=4, sticky=tk.EW, padx=5, pady=5)

root.mainloop()