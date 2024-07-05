from moduls import *

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

        # 팝업 확인후 닫기
        if '닫기' in wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text:
            wait.until(EC.presence_of_element_located((By.XPATH, "//button[text()='닫기']"))).click()

        # 로그인 성공여부 체크
        login_check = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).text
        if '로그아웃' in login_check:
            print('- 로그인 성공')
            return "로그인 성공1"
        elif '로그인' in login_check:
            print("- 로그인 실패")


def driver_close(driver):
    # 현재 열려 있는 모든 창의 핸들을 가져옵니다.
    window_handles = driver.window_handles
    # 각 창을 하나씩 닫습니다.
    for handle in window_handles:
        driver.switch_to.window(handle)
        driver.close()
    driver.quit()


# 토지대장 발금 페이지로 이동
def issued_go_page(wait):
    print('토지임야 체크')
    for c in wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "swiper-slide"))):
        if '토지(임야)' in c.text:
            c.click()
            print('토지(임야) 클릭')
            break
    wait.until(EC.presence_of_element_located((By.XPATH, """//a[text()='발급하기']"""))).click()
    print("발급하기 클릭")


# 펼쳐보기
def see_more(driver, wait, san, dong):
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn_tab_arrow")))
    time.sleep(10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn_tab_arrow"))).click()
    print("펼쳐보기 클릭")

    # 토지(임야)대장열람 클릭(라디오버튼)
    wait.until(EC.presence_of_element_located(
        (By.XPATH, """//a[@onclick="javascript:refreshFormRadio('03');"]""")))
    print("토지(임야)대장열람 클릭(라디오버튼) 체크")
    time.sleep(1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, """//a[@onclick="javascript:refreshFormRadio('03');"]"""))).click()
    print("토지(임야)대장열람 클릭(라디오버튼) 클릭")

    if san == '산':
        wait.until(EC.presence_of_element_located((By.XPATH, """//label[text()='임야 대장']"""))).click()
        print("임야대장 클릭(산)")

    driver.find_element(By.ID, "btnAddress").click()  # 대상토지 소재지 검색
    print('대상 토지 소재지 주소검색 클릭')
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[-1])  # 새창 변환
    print("새창변환")
    time.sleep(1)
    driver.find_element(By.NAME, "txtAddr").send_keys(dong)  # 동읍면 입력
    print("동읍면 입력")
    driver.execute_script("isValid();return false;")  # 검색버튼
    print("검색버튼 클릭")


# 동으로 검색한 결과에서 해당 주소 선택
def search_result_list_select(driver, si, dong, ri):
    aa = driver.find_elements(By.CSS_SELECTOR, "#resultList > a")
    ### 주소선택창에서 해당주소가 있을때까지 비교후 클릭
    print('주소선택창에서 해당주소가 있을때까지 비교후 클릭')
    for i in aa:
        if ri == '':
            if f'{si}' in i.text and f'({dong})' in i.text:
                i.send_keys(Keys.ENTER)
                break
        elif dong == "":
            if f'{si}' in i.text and f'({ri})' in i.text:
                i.send_keys(Keys.ENTER)
                break
        else:
            if f'{si}' in i.text and f'({ri})' in i.text:
                i.send_keys(Keys.ENTER)
                break
    print("클릭 완료")

    try:
        ### 주소 검색했을때 행정기관 선택하라는 팝업창이 나온다면
        driver.switch_to.window(driver.window_handles[-1])
        source = driver.page_source
        html = BeautifulSoup(source, 'lxml')
        if '검색결과' in str(html):
            driver.find_elements(By.TAG_NAME, "a")[1].click()
    except:
        pass


# 나머지 정보 입력
def info_input(driver, wait, jibun, boobun):
    ### 지번및 부번 입력
    driver.switch_to.window(driver.window_handles[-1])
    wait.until(
        EC.presence_of_element_located((By.NAME, "토지임야대장신청서/IN-토지임야대장신청서/신청토지소재지/주소정보/상세주소/번지"))).send_keys(
        jibun)
    print('지번 입력 완료')
    wait.until(
        EC.presence_of_element_located((By.NAME, "토지임야대장신청서/IN-토지임야대장신청서/신청토지소재지/주소정보/상세주소/호"))).send_keys(
        boobun)
    print('부번 입력 완료')
    ### 연혁 인쇄 유무(히스토리)
    wait.until(EC.presence_of_element_located((By.XPATH, """//label[text()='인쇄함']"""))).click()
    print('연혁 인쇄 유무 -> 인쇄함 클릭 ')
    ### 민원신청하기
    wait.until(EC.presence_of_element_located((By.ID, "btn_end"))).click()
    print("민원신청하기 클릭")


# input파일 지번과 열람문서 지번이 일치하는지 체크
def jinbun_match_chekced(driver, wait, num, do, si, dong, ri, san, jibun, boobun, fail_file_name, logger):
    ### 문서 열람후 새창
    time.sleep(5)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ibtn.small.dark"))).click()  # 열람문서 클릭
    print("열람문서 클릭")
    driver.switch_to.window(driver.window_handles[-1])  # 새창 변환

    # input 지번 편집
    if boobun == "":
        total_jibun = str(jibun)
    else:
        total_jibun = str(f"{jibun}-{boobun}")

    print("input 파일의 지번-부번과 열람문서 지번-부번이 같은지 체크..")
    ### 지번-부번 과 열람문서의 지번과 일치하면 진행, 일치하지 않으면 새로고침후 다시 확인
    ### (5번 반복후 그래도 일치하지 않으면 예외처리하고 실패 목록에 넣기
    for check_cnt in range(1, 6):
        match_checked = False
        document_jibun = driver.find_elements(By.CLASS_NAME, "BR1")[3].text
        document_jibun = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "BR1")))[3].text
        document_jibun = document_jibun.replace("산 ", "")

        if total_jibun == document_jibun:
            print("   지번 일치")
            match_checked = True
            break
        else:
            print("   지번 불일치")
            driver.close()
            driver.switch_to.window(driver.window_handles[-1])
            time.sleep(10)
            driver.refresh()

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ibtn.small.dark"))).click()  # 열람문서 클릭
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])  # 새창 변환
            match_checked = False

    return match_checked, total_jibun