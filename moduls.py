import sys, types, os
import json, time, random, re, csv
import logging
from datetime import datetime

import requests
import subprocess
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import CaptchaCracker as cc

from pywinauto import findwindows
from pywinauto import application

import selenium
from selenium import webdriver
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
from selenium.webdriver.common.alert import Alert