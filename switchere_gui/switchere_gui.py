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

def login_action():
    user = username_entry.get()
    passw = password_entry.get()
    btcv = btc_value.get()
    import subprocess
    FNULL = open(os.devnull, 'w')    #use this if you want to suppress output to stdout from the subprocess
    filename = "my_file.dat"
    args = "poll_byom_emails_for_switchere.exe " + user
    subprocess.call(args, stdout=FNULL, stderr=FNULL, shell=False)
    haveLogin = False
    closeDriver = False



# login button
login_button = ttk.Button(frame, text="Login", command=login_action)
login_button.grid(column=1, row=4, sticky=tk.E, padx=5, pady=5)

# get_auth_code
get_auth_code = ttk.Button(frame, text="Get auth code", command=root.destroy)
get_auth_code.grid(column=2, row=4, sticky=tk.EW, padx=5, pady=5)

root.mainloop()