from moduls import *


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





# 소요시간 계산산
def get_lab_time(start_time):
    end_time = time.time()  # 종료 시간 기록
    # 총 소요 시간 계산
    total_time = end_time - start_time
    # 분과 초로 변환
    minutes = int(total_time // 60)
    seconds = int(total_time % 60)
    return minutes, seconds


# 로그 설정
def setup_logging():
    current_time = datetime.today()
    logfilename = f"{current_time.strftime('%Y%m%d')} 로그.log"

    # 로거 생성
    logger = logging.getLogger('토지대장 로그')
    logger.setLevel(logging.DEBUG)

    # 기존 핸들러 제거
    if logger.hasHandlers():
        logger.handlers.clear()

    # 핸들러 생성 (파일 출력)
    file_handler = logging.FileHandler(logfilename)

    # 포매터 생성 및 핸들러에 설정
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # 로거에 핸들러 추가
    logger.addHandler(file_handler)

    return logger, file_handler


# 이어서 하기 위해 결과 파일에서 마지막 일련번호 찾기
def df_to_lastnumber(file_name,df):
    # 업데이트날짜 컬럼을 추가하면서
    # 기존 수집된 데이터와 이후 수집한 데이터의 열 개수가 달라
    # none 값 입력후 데이터프레임으로 변환
    f = open(file_name, 'rt', encoding='UTF8')
    reader = csv.reader(f)
    csv_list = []
    for l in reader:
        csv_list.append(l)
    f.close()
    df_db = pd.DataFrame(csv_list)
    header = df_db.iloc[0]
    df_db = df_db[1:]
    df_db.rename(columns=header, inplace=True)
    # 저장되어있는 데이터중 마지막 일련번호 찾기
    df_db_last_number = int(df_db['일련번호'][len(df_db['일련번호']) - 1])

    # 저장되어있는 마지막 일련번호를
    # input file 에서 찾고
    # 그 이후 데이터만 다시 df에 할당
    last_number = list(df['일련번호']).index(df_db_last_number + 1)
    df = df[last_number:]
    return df


# 실패 파일 저장
def fail_savefile(num, do, si, dong, ri, san, jibun, boobun, fail_file_name):
    fail_df = pd.DataFrame({
        '일련번호': [num],
        '시도': [do],
        '시군구': [si],
        '읍면동': [dong],
        '리': [ri],
        '구분': [san],
        '번': [jibun],
        '지': [boobun],

    })

    # 파일이 존재하는지 확인
    file_exists = os.path.isfile(fail_file_name)
    # 파일이 존재하지 않으면 헤더 포함하여 저장, 존재하면 헤더 없이 추가
    fail_df.to_csv(fail_file_name, mode='a', header=not file_exists, index=False)