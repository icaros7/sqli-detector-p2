from selenium.common import UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
import os
from urllib.error import HTTPError


def root_scan(url, driver):
    driver.get(url)

    # a 태그 찾기
    a_tag = driver.find_elements(By.TAG_NAME, "a")

    return a_tag


def recursive_scan(a_tag):
    # href 속성 리스트 선언
    href_list = []

    # a 태그 내 href 속성 탐색 후 href_list 에 추가
    for li in a_tag:
        href_text = li.get_attribute('href')
        href_list.append(href_text)

    return href_list


def cleanup(href_list):
    result = []

    # 리스트 중복 제거
    for value in href_list:
        if value not in result:
            result.append(value)

    strr = "http"

    # 수집한 링크 중 http 로 시작하지 않는 링크 (ex. javascript;;;, tel.02~ 등 삭제)
    for word in result:
        if strr not in word:
            result.remove(word)

    return result


def save_to_file(result, path, driver):
    for href_url in result:
        try:
            driver.get(href_url)
            html_source = driver.page_source

            # 파일 제목으로 입력할 수 없는 문자 제거
            sliced_url = href_url[len("http://"):]
            file_name = f'{sliced_url.replace("/", "_").replace("?", "_")}.txt'

            file_path = os.path.join(path, file_name)

            # text 파일 저장
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(str(html_source))

            print(f'Page saved: {file_path}')

        # 404 not found 에러 예외 처리
        except HTTPError as e:
            print(f'Error: {e}')

        # alert 창이 나왔을 때 에러 예외 처리
        except UnexpectedAlertPresentException as e:
            print(f'Error: {e}')

        # tag 타입 에러 예외 처리
        except AttributeError as e:
            print(f'Error: {e}')
