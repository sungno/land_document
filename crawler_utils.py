from moduls import *


def result_img():
    """
    가중치로 결과 도출
    :return:
    """
#     target_img_path = r'C:\Users\ysn39\파이썬 주피터\장앤장\캡챠\target_captcha.png'    #타켓 이미지 경로
    target_img_path = r'target_captcha.png'    #타켓 이미지 경로
    img_width = 200 #타켓 이미지 넓이
    img_height = 72 #타켓 이미지 높이
    img_length = 6  #타켓 이미지가 포함한 문자 수
    img_char = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}   #타켓 이미지안에 포함된 문자들
#     weights_path = r'C:\Users\ysn39\파이썬 주피터\장앤장\캡챠\gove24_weights.h5' #학습 결과 가중치 경로
    weights_path = r'gove24_20250708.h5' #학습 결과 가중치 경로
    AM = cc.ApplyModel(weights_path, img_width, img_height, img_length, img_char)   #결과 가중치를 가지는 모델 생성
    pred = AM.predict(target_img_path)  #결과 도출
    return pred


### 정부24 Login
def gov_login(driver, wait, user_id, user_pw):
    while True:
        while True:
            print('- 로그인 시도')
            driver.get("https://plus.gov.kr/login/loginIdPwd")
            # 아이디 입력후 다음버튼 클릭
            wait.until(EC.presence_of_element_located((By.ID, """input_id""")))
            wait.until(EC.element_to_be_clickable((By.ID, """input_id"""))).send_keys(user_id)
            time.sleep(random.uniform(1, 2))
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, """btn.lg.btn-login"""))).click()

            # 비밀번호 입력
            wait.until(EC.presence_of_element_located((By.ID, """input_pwd""")))
            wait.until(EC.element_to_be_clickable((By.ID, """input_pwd"""))).send_keys(user_pw)

            # 캡차(보안문자) 이미지 캡쳐후 저장
            element1 = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'img-captcha')))
            element_png = element1.screenshot_as_png
            with open("target_captcha.png", "wb") as file:
                file.write(element_png)

            # 저장된 캡차(보안문자) 이미지 해독
            capcha_number = result_img()
            if len(capcha_number) == 6:
                break
            time.sleep(3)

        # 보안문자 입력
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "input.lg"))).send_keys(capcha_number)
        time.sleep(1)
        # 로그인 버튼 클릭
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, """btn.lg.btn-login"""))).click()

        time.sleep(3)
        if "비밀번호 변경" in wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text:
            print("- 비밀번호 나중에 변경하기")
            wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body'))).send_keys(Keys.END)
            time.sleep(1)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, """btn.xlg.tertiary"""))).click()
            print('- 다음에 변경하기 클릭')
        time.sleep(3)

        # '비밀번호 변경없이 진행합니다.' modal 처리
        time.sleep(1)
        body_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
        if '변경 없이 진행합니다.' in body_text:
            top_modal = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "iw-modal-alert.on")))
            top_modal.find_element(By.CLASS_NAME, "btn.tertiary.close-modal").click()

        # '정부24 개편 기념 이벤트' 모달 처리
        time.sleep(1)
        if 'iw-modal-auto main-popup on' in driver.page_source:
            print("'정부24 개편 기념 이벤트' 모달 처리 완료")
            popup_modal = wait.until(EC.presence_of_element_located((By.ID, "layerModal_main_popup")))
            popup_modal.find_element(By.TAG_NAME, 'button').click()

        # 로그인 성공여부 체크
        body_text = wait.until(EC.presence_of_element_located((By.TAG_NAME, "body"))).text
        if '아이디 또는 비밀번호가 일치하지 않습니다.' in body_text:
            print("- 로그인 실패")
        else:
            print("로그인 성공")
            return "- 로그인 성공"
        time.sleep(1)


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
    for c in wait.until(EC.presence_of_all_elements_located((By.XPATH, """//span[text()='토지(임야)대장']"""))):
        if '토지(임야)대장' in c.text:
            c.click()
            print("'토지(임야)대장' 클릭")
            break
    wait.until(EC.presence_of_element_located((By.XPATH, """//a[text()='발급하기']"""))).click()
    print("발급하기 클릭")


# 토지대장 발금 페이지로 이동
def issued_go_page_2(wait):
    """
     자주 찾는 서비스에 없는 경우
    :param wait:
    :return:
    """
    print('토지임야 체크')
    land_issued_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, """btn-txt.ico-arr-right-white""")))
    if land_issued_element:
        land_issued_element.click()
        print("'토지(임야)대장' 클릭")
        wait.until(EC.presence_of_element_located((By.XPATH, """//button[text()='발급하기']"""))).click()
        print("발급하기 클릭")


# 펼쳐보기
def see_more(driver, wait, san, dong):
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn_tab_arrow")))
    # time.sleep(1)
    # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "btn_tab_arrow"))).click()
    # print("펼쳐보기 클릭")
    #
    # # 토지(임야)대장열람 클릭(라디오버튼)
    # time.sleep(1)
    # wait.until(EC.presence_of_element_located(
    #     (By.XPATH, """//a[@onclick="javascript:refreshFormRadio('03');"]""")))
    # print("토지(임야)대장열람 클릭(라디오버튼) 체크")
    # time.sleep(1)
    # wait.until(EC.element_to_be_clickable(
    #     (By.XPATH, """//a[@onclick="javascript:refreshFormRadio('03');"]"""))).click()
    # print("토지(임야)대장열람 클릭(라디오버튼) 클릭")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='토지(임야)대장열람']"))).click()
    time.sleep(3)
    if san == '산':
        wait.until(EC.presence_of_element_located((By.XPATH, """//label[text()='임야 대장']"""))).click()
        elem = wait.until(EC.visibility_of_element_located((By.XPATH, "//label[text()='임야 대장']")))
        actions = ActionChains(driver)
        actions.move_to_element(elem).click().perform()
        print("임야대장 클릭(산)")

    time.sleep(1)
    elem = driver.find_element(By.ID, "btnAddress")  # 대상토지 소재지 검색
    actions = ActionChains(driver)
    actions.move_to_element(elem).click().perform()

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

    ### 토지이동연혁 인쇄 유무(히스토리)
    land_history_division = '토지임야대장신청서_IN-토지임야대장신청서_토지연혁구분_.라디오코드_1'
    elem = wait.until(EC.presence_of_element_located((By.XPATH, f"""//label[@for='{land_history_division}']""")))
    actions = ActionChains(driver)
    actions.move_to_element(elem).click().perform()
    print('토지이동연혁 인쇄 유무 -> 인쇄함 클릭 ')

    ### 소유권연혁 인쇄 유무(히스토리)
    ownership_division = "토지임야대장신청서_IN-토지임야대장신청서_소유권연혁구분_.라디오코드_1"
    elem = wait.until(EC.presence_of_element_located((By.XPATH, f"""//label[@for='{ownership_division}']""")))
    actions = ActionChains(driver)
    actions.move_to_element(elem).click().perform()
    print('소유권연혁 인쇄 유무 -> 인쇄함 클릭 ')

    ### 민원신청하기
    elem = wait.until(EC.presence_of_element_located((By.ID, "btn_end")))
    actions = ActionChains(driver)
    actions.move_to_element(elem).click().perform()
    print("민원신청하기 클릭")


# input파일 지번과 열람문서 지번이 일치하는지 체크
def jinbun_match_chekced(driver, wait, jibun, boobun):
    ### 문서 열람후 새창
    WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "btn.secondary.xsm"))).click()  # 열람문서 클릭
    print("열람문서 클릭")

    ### 열람된 문서로 새창 변환
    while True:
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[-1])
            break

    # input 지번 편집
    if boobun == "":
        total_jibun = str(jibun)
    else:
        total_jibun = str(f"{jibun}-{boobun}")

    print("input 파일의 지번-부번과 열람문서 지번-부번이 같은지 체크..")
    ### 지번-부번 과 열람문서의 지번과 일치하면 진행, 일치하지 않으면 새로고침후 다시 확인
    ### (5번 반복후 그래도 일치하지 않으면 예외처리하고 실패 목록에 넣기
    match_checked = False
    for check_cnt in range(1, 6):
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
            time.sleep(5)
            wait.until(EC.presence_of_element_located((By.ID, "srch"))).click()
            time.sleep(1)

            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ibtn.small.dark"))).click()  # 열람문서 클릭
            time.sleep(1)
            driver.switch_to.window(driver.window_handles[-1])  # 새창 변환
            match_checked = False

    if not match_checked:
        driver.close()
        driver.switch_to.window(driver.window_handles[-1])
        for cnt_check_2 in range(1, 6):
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ibtn.small.dark")))[cnt_check_2].click()
            document_jibun = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "BR1")))[3].text
            document_jibun = document_jibun.replace("산 ", "")

            if total_jibun == document_jibun:
                print("   지번 일치(2)")
                match_checked = True
                break
            else:
                print("   지번 불일치(2)")
                match_checked = False
                driver.close()

    return match_checked, total_jibun
