import argparse
import os
import subprocess

import crawl
import data_export

from urllib.parse import urlparse

# Parameter parsing
parser = argparse.ArgumentParser(description="SQL Injection Detection Project v2")
parser.add_argument('-u', '--url', action='store', default='', help='Target site url', required=True)
parser.add_argument('-b', '--browser', action='store', default='Edge', help='Select browser to use (Edge / Chrome / Firefox)')
parser.add_argument('-t', '--thread', action='store', default='4', help='Number of Thread (1-10)')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc
browser = args.browser
thread = args.thread

try:
    if int(thread) < 1 or int(thread) > 11:
        print('Error: thread option must be in range of 1, 10')
        exit()

except ValueError:
    print('Error: thread option must be Int type, in range of 1,10')
    exit()

# Check pip module installed
while True:
    try:
        import bs4
        import selenium
        import pandas
        import openpyxl

    except ModuleNotFoundError as e:
        print('Error: Dependency module not found. Try to installing')
        subprocess.call(['python', '-m', 'pip', '--disable-pip-version-check', 'install', 'BeautifulSoup4'])
        subprocess.call(['python', '-m', 'pip', '--disable-pip-version-check', 'install', 'pandas'])
        subprocess.call(['python', '-m', 'pip', '--disable-pip-version-check', 'install', 'openpyxl'])
        subprocess.call(['python', '-m', 'pip', '--disable-pip-version-check', 'install', 'selenium'])

    else:
        break

# Make dir with domain name
directory_path = f'./{domain}'
parsing_file_path = f'{directory_path}/_parsing_.txt'
tag_file_path = f'{directory_path}/_tag_struct_.xlsx'
injectable_file_path = f'{directory_path}/_injectable_.txt'

# Make workdir
os.makedirs(directory_path, exist_ok=True)

from selenium import webdriver
# Init Browser
driver_options = {
    'Edge': webdriver.EdgeOptions(),
    'Chrome': webdriver.ChromeOptions(),
    'Firefox': webdriver.FirefoxOptions()
}

options = driver_options.get(browser)
options.add_argument('window-size=1920,1080')
options.add_argument('--headless')  # Run webdriver in headless mode (without opening a browser window)

driver_executables = {
    'Edge': './msedgedriver.exe',
    'Chrome': './chromedriver.exe',
    'Firefox': './geckodriver.exe'
}

driver = webdriver.__getattribute__(browser)(executable_path=driver_executables.get(browser), options=options)

dir = os.listdir(directory_path)

# Skip if has already crawling data
if len(dir) == 0:
    # Crawling All Page
    try:
        a_tag = crawl.root_scan(url, driver)
        href_list = crawl.recursive_scan(a_tag)
        result = crawl.cleanup(href_list)
        crawl.save_to_file(result, directory_path, driver)

    except FileNotFoundError:
        print('Error: File Not Found')

    except IOError as e:
        print(f'Error: {e}')

# Scan specific tag and export to xlsx
try:
    txtf = data_export.scan_txt(directory_path)
    tags, dict = data_export.extract_tags_from_files(txtf)
    data_export.save_tags_to_excel(tags, dict, tag_file_path)

except Exception as e:
    print(f'Error: {e}')

# TODO: Complete Sqli test module
# try:
#     sql = sqli.init(url, thread)
#     out, injectable = sqli.process_run(sql)
#     result = sqli.result(out, injectable, injectable_file_path)
#
#     print()
#
# except Exception as e:
#     print(f'Error: {e}')