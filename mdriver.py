from moduls import *


def make_user_agent(ua, is_mobile):
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture = ""
    else:  # Window
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion": ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform": f"{platform_info}",
        "acceptLanguage": "ko-KR, kr, en-US, en",
        "userAgentMetadata": {
            "brands": [
                {"brand": " Not A;Brand", "version": "99"},
                {"brand": "Google Chrome", "version": f"{version}"},
                {"brand": "Chromium", "version": f"{version}"}
            ],
            "fullVersion": f"{ua_full_version}",
            "platform": platform,
            "platformVersion": platform_version,
            "architecture": architecture,
            "model": model,
            "mobile": is_mobile  # True, False
        }
    }
    return RET_USER_AGENT


def read_agents():
    agents = []
    f = open("./useragents.txt", "r", encoding="utf8")
    while True:
        line = f.readline()
        if not line:
            break
        agents.append(line.rstrip())
    return agents


def make_driver():
    UA_list = read_agents()
    UA = random.choice(UA_list)  # seed = time.time()
    options = Options()
    # User Agent 속이기
    options.add_argument(f'--user-agent={UA}')
    # options.add_argument("--start-fullscreen")  # pc용 사이즈
    options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    options.add_argument('--disable-logging')
    # origin 허용(동적데이터 불러오기)
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-site-isolation-trials")
    options.headless = False

    chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
    # driver = uc.Chrome(options=options)

    driver = webdriver.Chrome(options=options)
    print("Driver Open")

    driver.maximize_window()
    print("Maximize Window")

    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 60)
    print("Wait Driver ")

    UA_Data = make_user_agent(UA, False)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", UA_Data)
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", UA_Data)
    print("Driver Setting Final")
    return driver, wait


### 셀레니움 스타터 세팅
def starter():
    # user_agent세팅 (사용자가 직접 제어 하는것처럼 하기 위해 세팅)
    UA_list = read_agents()
    UA = random.choice(UA_list)  # seed = time.time()
    option = Options()
    option.add_argument('user-agent=' + UA)
    option.add_argument("--no-first-run --no-service-autorun --password-store=basic")
    # option.add_argument('--disable-logging')
    # origin 허용(동적데이터 불러오기)
    # option.add_argument("--disable-web-security")
    # option.add_argument("--disable-site-isolation-trials")
    option.headless = False
    option.add_argument('window-size=1920x1080')
    option.add_argument('lang=ko_KR')
    option.add_argument("disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
    option.add_experimental_option("excludeSwitches", ["enable-automation"])  # 자동화 표시 제거
    option.add_experimental_option('useAutomationExtension', False)  # 자동화 확장 기능 사용 안 함
    print("Driver Waiting")

    driver = webdriver.Chrome(options=option)
    print("Driver Open")

    driver.maximize_window()
    print("Maximize Window")


    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 60)
    print("Wait Driver ")

    UA_Data = make_user_agent(UA, False)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", UA_Data)
    driver.execute_cdp_cmd("Emulation.setUserAgentOverride", UA_Data)
    print("Driver Setting Final")

    return driver, wait