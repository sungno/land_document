import time
import pandas as pd
from bs4 import BeautifulSoup
import subprocess
import re
import os
import pyperclip
import numpy as np
import urllib.request
import threading
import random
import pyautogui as pg
from pywinauto import findwindows
from pywinauto import application


import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.Qt import *


# from selenium import webdriver
# import chromedriver_autoinstaller
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver import ActionChains
# from selenium.webdriver.common.alert import Alert
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.chrome.service import Service


import selenium
from user_agents import parse
import undetected_chromedriver as uc
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager