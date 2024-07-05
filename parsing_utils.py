from method import *

def parsing_part(driver, num, san, total_jibun, file_name):
    print('토지대장 데이터 수집시작...')
    ### 날짜
    tms = time.localtime()
    all_date = time.strftime('%Y-%m-%d', tms)

    ### 공유지연명부 여부
    if '연명부' in driver.find_element(By.TAG_NAME, "body").text:
        category = '공유지연명부'
    else:
        category = '소유자'

    ### 현재페이지의 html 파싱
    html = BeautifulSoup(driver.page_source, 'lxml')

    ### pnt,법정동명
    pnu = html.find('td', attrs={'class': 'B1R2'}).text.replace("\n", " ").replace("\t", "").replace("-", "").replace(
        " ", "")
    legal_dongname = html.find_all('td', attrs={'class': 'B1R2'})[1].text

    ### 토지표시 목록중 마지막 값들을 수집하기위해 페이지 개수를 확인해야함
    ### 토지표시와 소유자 항목들이 같은 table에 묶여 있었고 페이지별로도 나눠져 있어서
    ### 지목, 면적, 사유 별로 모두 수집한후 마지막 값들만 가져오려고 한다.
    ### 각 페이지의 테이블
    l2_box = []
    for class_l2 in html.find_all('table', attrs={'class': 'L2'}):
        if '토     지    표    시' in class_l2.text:  # 임야대장에서 '토     지    표    시'라는 text가 있다면
            l2_box.append(class_l2)  # l2_box 라는 list에 append
    ground_part_box = []
    for l2 in l2_box:
        ground_part_box.append(l2.find('tbody').find_all('tr')[3:])  # 3번째 index부터 값이 있음

    ### 토지표시와 , 소유자를 구분할수가 없어서
    ### 각 행의 첫번째줄, 두번째줄을 리스트에 담아서 구분
    line_1st_box = []  # tr중 홀수라인
    line_2nd_box = []  # tr중 짝수라인
    for gb in ground_part_box:
        for i, g in enumerate(gb):
            if (i + 1) % 2 != 0:
                line_1st_box.append(g)
            else:
                line_2nd_box.append(g)

    owrner_date_box = []
    owrner_reason_box = []
    owrner_mail_box = []
    owrner_name_box = []
    owrner_code_box = []
    cnt_box = []
    share_box = []
    category_box = []
    for st1 in line_1st_box:
        ### 지목
        ### 지목은 마지막 값만 넣으면 되기대문에 변수 jimok 에 대입
        ### 값이 '\n\n' 이면 거르기
        if st1.find_all('td')[0].text != '\n\n':
            # print(st1.find_all('td')[0].text)
            jimok = st1.find_all('td')[0].text.split(")")[-1]

        ### 면적
        ### 면적은 마지막 값만 넣으면 되기대문에 변수 m2 에 대입
        ### 값이 '' 이면 거르기
        if st1.find_all('td')[1].text != '':
            # print(st1.find_all('td')[1].text)
            m2 = st1.find_all('td')[1].text

        ### 토지표시변경사유, 토지표시변경일자
        ### 토지표시변경사유, 토지표시변경일자는 마지막 값만 넣으면 되기대문에 각각 변수 reason, reason_date에 대입
        if '여백' in st1.find_all('td')[2].text:
            pass
        elif st1.find_all('td')[2].text == "":
            pass
        else:
            #             test_box.append(st1.find_all('td')[2].text)
            reason = st1.find_all('td')[2].text.replace("\t", "").split("\n")[-1]
            reason_date = st1.find_all('td')[2].text.replace("\t", "").split("\n")[:-1]
            reason_date = \
                " ".join(reason_date).replace("년  ", " - ").replace("월  ", " - ").replace("일 ", "").split(")")[
                    -1]

        ### 소유권변동일자
        ### 소유권변동일자는 첫번째줄에서 4번째 td에 해당

        owrner_date_box.append(
            st1.find_all('td')[3].text.replace("\n", "").replace("\t", "").replace("년 ", "-").replace("월 ",
                                                                                                      "-").replace(
                "일 ", ""))

        ### 소유자 주소
        if '여백' in st1.find_all('td')[4].text:
            break
        else:
            owrner_mail_box.append(st1.find_all('td')[4].text)

    for nd2, st1 in zip(line_2nd_box, line_1st_box):
        ### 소유권변동원인
        if nd2.find_all('td')[0].text != "":
            owrner_reason_box.append(nd2.find_all('td')[0].text[4:])
        elif '여백' in st1.find_all('td')[4].text:
            break
        else:
            owrner_reason_box.append("")

        ### 소유자명
        if nd2.find_all('td')[1].text != "":
            owrner_name_box.append(nd2.find_all('td')[1].text)
        elif '여백' in st1.find_all('td')[4].text:
            break
        else:
            owrner_name_box.append("")

        ### 소유자코드(주민,법인)
        if nd2.find_all('td')[2].text != "":
            owrner_code_box.append(nd2.find_all('td')[2].text)
        elif '여백' in st1.find_all('td')[4].text:
            break
        else:
            owrner_code_box.append("")

    ### 순번(등기순위번호)
    for i, o in enumerate(owrner_reason_box):
        cnt_box.append(i + 1)
        share_box.append("")
        category_box.append('소유자')

    ### 공유지 연명부가 있으면
    if category == '공유지연명부':
        print('공유지 연명부 있음')
        sh_cnt = []
        sh_change_date_box = []
        sh_share_box = []
        sh_mail_box = []
        sh_code_box = []

        sh_change_reason_box = []
        sh_name_box = []
        sh_category_box = []

        for p in html.find_all('div', attrs={'class': 'page'}):
            if '공유지 연명부' in p.text:

                ppp = p.find_all('table')
                share = ppp[-1].find("tbody").find_all('tr')[7:]

                ### 첫째줄의 정보와, 둘째쭐의 정보를 나눠서 각각 리스트 담기기
                share_line_1st_box = []
                share_line_2nd_box = []
                for i, s in enumerate(share):
                    if (i + 1) % 2 != 0:
                        share_line_1st_box.append(s)
                    else:
                        share_line_2nd_box.append(s)

                ### 공유지 연명부 첫번째 줄 ( 순번, 변공일자 , 소유권지분, 주소 , 등록번호 / 총 5개)
                for sh1 in share_line_1st_box:
                    ### 공유지 연명부 순번
                    if sh1.find_all('td')[0].text == '\n\n':
                        pass
                    elif sh1.find_all('td')[0].text == '':
                        pass
                    else:
                        sh_cnt.append(sh1.find_all('td')[0].text)
                        sh_category_box.append("공유지 연명부")

                    ### 공유지 연명부 변동일자
                    if sh1.find_all('td')[1].text == '\n\n':
                        pass
                    elif sh1.find_all('td')[1].text == '':
                        pass
                    else:

                        sh_change_date_box.append(
                            sh1.find_all('td')[1].text.replace("\n", "").replace("\t", "").replace("년 ",
                                                                                                   "-").replace(
                                "월",
                                "-").replace(
                                "일 ", "").replace(" ", ""))

                    ### 공유지 연명부 소유권 지분
                    if sh1.find_all('td')[2].text == '\n\n':
                        pass
                    elif sh1.find_all('td')[2].text == '':
                        pass
                    else:
                        sh_share_box.append(sh1.find_all('td')[2].text)

                    ### 공유지 연명부 소유자 주소
                    if sh1.find_all('td')[3].text == '\n\n':
                        pass
                    elif sh1.find_all('td')[3].text == '':
                        pass
                    elif '여백' in sh1.find_all('td')[3].text:
                        pass
                    else:
                        sh_mail_box.append(sh1.find_all('td')[3].text)

                    ### 공유지 연명부 소유자 등록번호
                    if sh1.find_all('td')[4].text == '\n\n':
                        pass
                    elif sh1.find_all('td')[4].text == '':
                        pass
                    elif '여백' in sh1.find_all('td')[4].text:
                        pass
                    else:
                        # print(sh1.find_all('td')[4].text)
                        sh_code_box.append(sh1.find_all('td')[4].text)

                ### 공유지 연명부 두번째 줄 ( 번동원인, 성명 또는 명칭 / 총 2개)
                for sh2 in share_line_2nd_box:
                    ### 공유지 연명부 변동원인
                    if sh2.find_all('td')[0].text == '\n\n':
                        pass
                    elif sh2.find_all('td')[0].text == '':
                        pass
                    else:
                        sh_change_reason_box.append(sh2.find_all('td')[0].text[4:])

                    ### 공유지 연명부 성명 또는 명칭
                    if sh2.find_all('td')[1].text == '\n\n':
                        pass
                    elif sh2.find_all('td')[1].text == '':
                        pass
                    else:
                        # print(sh2.find_all('td')[1].text)
                        sh_name_box.append(sh2.find_all('td')[1].text)

                ### 공유지 연명부가 있다면 양식에 맞게 저장하기위해 토지대장의 항목과 공유지연명부의 항목을 합치기
                total_date_box = owrner_date_box + sh_change_date_box
                total_change_reason_box = owrner_reason_box + sh_change_reason_box
                total_mail_box = owrner_mail_box + sh_mail_box
                total_name_box = owrner_name_box + sh_name_box
                total_code_box = owrner_code_box + sh_code_box
                total_cnt_box = cnt_box + sh_cnt
                total_share_box = share_box + sh_share_box
                total_category_box = category_box + sh_category_box

    else:
        print('공유지 연명부 없음')
        total_date_box = owrner_date_box
        total_change_reason_box = owrner_reason_box
        total_mail_box = owrner_mail_box
        total_name_box = owrner_name_box
        total_code_box = owrner_code_box
        total_cnt_box = cnt_box
        total_share_box = share_box
        total_category_box = category_box

    now = datetime.now()
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')
    for t1, t2, t3, t4, t5, t6, t7, t8 in zip(total_date_box, total_change_reason_box, total_mail_box,
                                              total_name_box, total_code_box, total_cnt_box, total_share_box,
                                              total_category_box):
        df = pd.DataFrame({
            '일련번호': [num],
            'pnu': [pnu],
            '법정동명': [legal_dongname],
            '지번': [total_jibun],
            '지목': [jimok.strip()],
            '면적': [m2],
            '토지표시변경사유': [reason],
            '토지표시변경일자': [reason_date],
            "대장구분명": [san],
            '대장발급일': [all_date],
            '구분': [t8],
            '등기순위번호': [t6],
            '소유자구분': ["확인필요"],
            "소유자명": [t4.strip().replace("\t", "")],
            "주민법인코드": [t5],
            '소유자주소': [t3],
            '소유권변동원인': [t2],
            '소유권변동일자': [t1],
            '지분': [t7],
            '업데이트시간': [current_time]

        })

        # 탭 공백을 제거한 데이터프레임
        df = remove_tabs_from_dataframe(df)
        # 파일이 존재하는지 확인
        file_exists = os.path.isfile(file_name)
        # 파일이 존재하지 않으면 헤더 포함하여 저장, 존재하면 헤더 없이 추가
        df.to_csv(file_name, mode='a', header=not file_exists, index=False)



