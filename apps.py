from moduls import *

import method
import mdriver
import crawler_utils
import parsing_utils

print(2)
print("Ver 3.0")
print("2025-07-11")


def download_script(url):
    headers = {'Cache-Control': 'no-cache'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text

def load_module_from_string(module_name, module_content):
    module = types.ModuleType(module_name)
    exec(module_content, module.__dict__)
    sys.modules[module_name] = module
    return module

def download_and_load_all_scripts(scripts_json_url):
    scripts_content = download_script(scripts_json_url)
    scripts_data = json.loads(scripts_content)
    for script_url in scripts_data["scripts"]:
        script_name = script_url.split('/')[-1].split('.')[0]
        print(script_name)
        script_content = download_script(script_url)
        load_module_from_string(script_name, script_content)
    print("\n" + '='*50 + "\n")

try:
    # # scripts.json 파일의 URL
    # scripts_json_url = "https://raw.githubusercontent.com/sungno/land_document/main/scripts.json"
    # # 모든 스크립트 다운로드 및 로드
    # download_and_load_all_scripts(scripts_json_url)



    ################### 실행 코드 시작 ###########################################
    logger, file_handler = method.setup_logging()
    print('토지대장 수집 시작')
    print(f"파일 변환중....")

    file_name = "토지대장_VM_결과.csv"
    fail_file_name = '토지대장_VM_실패리스트.csv'  # 실패파일 파일명 만들기
    account_df = pd.read_csv("계정.csv")
    df = pd.read_csv("input.csv")

    # 이어서 하기 위해 결과 파일에서 마지막 일련번호 찾기
    try:
        df = method.df_to_lastnumber(file_name, df)
    except Exception as e:
        print(e)

    # 계정 파일과 INPUT파일 합치기
    original_df = method.merge_dataframe(df, account_df)
    print(f"파일 변환 완료.")
    print(f"□ 수집 시작")

    ### 수집 시작
    ip_cnt = 0
    for num, do, si, dong, ri, san, jibun, boobun, user_id, user_pw in original_df.to_numpy().tolist():
        #     user_id = 'jiralma86'
        #     user_pw = '!gkffhd8686'
        ip_cnt += 1
        ########################## 세팅 파트 ########################################
        if boobun != '':
            boobun = str(int(boobun))
        total_mail = f"{num} {do} {si} {dong} {ri} {san} {jibun} {boobun}".replace("  ", " ")

        # input파일에 지번이 없는경우 체크
        try:
            jibun_1 = float(jibun)
            print(total_mail)
        except Exception as e:
            # print(e)
            print(f"★ {total_mail} 수집 실패")
            print(f"★ input.csv 파일에서 지번 입력값 확인요망")
            # 실패파일 저장
            method.fail_savefile(num, do, si, dong, ri, san, jibun, boobun, fail_file_name)
            # 로그저장
            logger.error(f'{user_id} - {total_mail} - input 파일에서 지번 입력값 확인요망')
            continue

        try:
            ########################## 매크로 파트 ########################################
            driver, wait = mdriver.starter()
            crawler_utils.gov_login(driver, wait, user_id, user_pw)

            # 토지대장 발금 페이지로 이동
            crawler_utils.issued_go_page(wait)

            # 펼쳐보기
            try:
                crawler_utils.see_more(driver, wait, san, dong)
            except:
                print("펼쳐보기 EXCEPTION!")
                time.sleep(5)
                driver.switch_to.window(driver.window_handles[-1])  # 새창 변환
                driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.HOME)
                time.sleep(1)
                crawler_utils.see_more(driver, wait, san, dong)

            # 동으로 검색한 결과에서 해당 주소 선택
            crawler_utils.search_result_list_select(driver, si, dong, ri)

            # 나머지 정보 입력
            crawler_utils.info_input(driver, wait, jibun, boobun)




            # 팝업 처리
            # try:
            #     temporary_wait = WebDriverWait(driver, 10)
            #     elements = temporary_wait.until(EC.presence_of_element_located((By.CLASS_NAME, "survey_pop")))
            #     wait.until(EC.presence_of_element_located((By.CLASS_NAME, "pop_btn_close"))).click()
            # except TimeoutException:
            #     print("팝업 없음")

            # input파일 지번과 열람문서 지번이 일치하는지 체크
            match_checked, total_jibun = crawler_utils.jinbun_match_chekced(driver, wait, jibun, boobun)
            if not match_checked:
                method.fail_savefile(num, do, si, dong, ri, san, jibun, boobun, fail_file_name)
                logger.critical(
                    f'{user_id} - {total_mail} - input 지번,부번과 열람문서의 지번,부번이 일치하지 않음 - 정부24오류 - 해당주소는 실패파일에 저장하겠습니다.')
                crawler_utils.driver_close(driver)
                continue

            ########################## 수집 파트 ########################################
            print('토지대장 데이터 수집시작...')
            parsing_utils.parsing_part(driver, num, san, total_jibun, file_name)

            # 로그저장
            logger.debug(f'{user_id} - {total_mail} - 수집에 성공하여 파일에 저장합니다.')

        except:
            method.fail_savefile(num, do, si, dong, ri, san, jibun, boobun, fail_file_name)
            # 로그저장
            logger.error(f'{user_id} - {total_mail} - 수집에 실패 하였습니다.실패 파일에 저장하겠습니다.')
        crawler_utils.driver_close(driver)

        ### 아이피 변경
        try:
            if ip_cnt % 50 == 0:
                method.ip_change_click()
        except:
            print('★ 아이피 변경 실패')

        print()
    print('■■■■■■ 전체 수집 완료 ■■■■■■')

except Exception as e:
    print(f"[apps.py] An error occurred: {e}")