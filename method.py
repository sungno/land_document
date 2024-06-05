from moduls import *


### 셀레니움 스타터 세팅
def starter():
    # user_agent세팅 (사용자가 직접 제어 하는것처럼 하기 위해 세팅)
    user_agent = "Mozilla/5.0 (Linux; Android 9; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.83 Mobile Safari/537.36"

    option = Options()
    subprocess.Popen(
        r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\chrometemp"')  # 디버거 크롬 구동
    option.add_argument('user-agent=' + user_agent)
    option.add_experimental_option('debuggerAddress', '127.0.0.1:9222')  # 디버거 모드 세팅
    option.add_argument('window-size=1920x1080')
    option.add_argument('lang=ko_KR')
    option.add_argument(
        f'user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36')
    option.add_experimental_option("detach", False)
    chromedriver_autoinstaller.install(True)
    driver = webdriver.Chrome(options=option)

    driver.implicitly_wait(20)
    wait = WebDriverWait(driver, 60)
    return driver, wait



### 시간체크 함수
def time_check():
    tms = time.localtime()
    result_time = time.strftime('%Y.%m.%d %I:%M:%S %p', tms)
    return result_time


### input 파일과, 계정파일 데이터프레임으로 합치기
def merge_dataframe(df, account_df):
    df = df.replace(np.nan, '', regex=True)  # 'nan'값 ""(빈문자열)로 치환
    id_box = []
    pw_box = []
    c = 0
    for d in df['일련번호']:
        for x, y in zip(account_df['ID'], account_df['PW']):
            c += 1
            if c > len(df['일련번호']):
                b = 0
                break
            else:
                b = 1
                id_box.append(x)
                pw_box.append(y)
        if b == 0:
            break
    df['ID'] = id_box
    df['PW'] = pw_box

    return df


### 정부24 Login
def gov_login(driver, wait, user_id, user_pw):
    while True:
        driver.get("https://www.gov.kr/nlogin/?Mcode=10003&regType=ctab")
        wait.until(EC.presence_of_element_located((By.ID, '아이디'))).click()
        wait.until(EC.presence_of_element_located((By.ID, 'userId'))).send_keys(user_id)
        wait.until(EC.presence_of_element_located((By.XPATH, """//button[text()='다음']"""))).click()

        wait.until(EC.presence_of_element_located((By.ID, 'pwd'))).send_keys(user_pw)
        wait.until(EC.presence_of_element_located((By.XPATH, """//button[text()='로그인']"""))).click()
        time.sleep(5)

        if "비밀번호 변경" in wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text:
            print("- 비밀번호 나중에 변경하기")
            wait.until(EC.presence_of_element_located((By.XPATH, """//a[text()='나중에 변경하기']"""))).click()
            print('- 나중에 변경하기 클릭')
            time.sleep(5)
        login_check = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text
        if '로그아웃' in login_check:
            print('- 로그인 성공')
            return "로그인 성공1"
        elif '로그인' in login_check:
            print("- 로그인 실패")


# COOL IP 제어
def ip_change_click():
    app = application.Application(backend='win32').connect(title_re="COOL IP - *")
    dlg = app['Dialog']
    # dlg.print_control_identifiers()  #속성값들 확인
    dlg.child_window(title="IP변경", class_name="Button").click()
    time.sleep(1)
    print("● IP변경")

# 모든 문자열 데이터의 탭 공백을 제거하는 함수 정의
def remove_tabs_from_dataframe(df):
    # 데이터프레임 내의 모든 문자열 데이터에서 탭 공백 제거
    return df.applymap(lambda x: x.replace('\t', '') if isinstance(x, str) else x)


def driver_close(driver):
    # 현재 열려 있는 모든 창의 핸들을 가져옵니다.
    window_handles = driver.window_handles
    # 각 창을 하나씩 닫습니다.
    for handle in window_handles:
        driver.switch_to.window(handle)
        driver.close()
    driver.quit()