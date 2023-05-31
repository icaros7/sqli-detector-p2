import argparse
import os

import crawl
import data_export
import init

from urllib.parse import urlparse

# Parameter parsing
parser = argparse.ArgumentParser(description="SQL Injection Detection Project v2")
parser.add_argument('-u', '--url', action='store', default='', help='Target site url', required=True)
parser.add_argument('-b', '--browser', action='store', default='Edge', help='Select browser to use (Edge / Chrome / '
                                                                            'Firefox)')
parser.add_argument('-t', '--thread', action='store', default='4', help='Number of Thread (1-10)')

# Init var
args = parser.parse_args()
url = args.url.rstrip("/")
domain = urlparse(url).netloc
browser = args.browser
thread = args.thread

# Check args and dependency module validity
init.args(thread)
init.module()

# Make dir with domain name
directory_path = f'./{domain}'
parsing_file_path = f'{directory_path}/_parsing_.txt'
tag_file_path = f'{directory_path}/_tag_struct_.xlsx'
injectable_file_path = f'{directory_path}/_injectable_.txt'

# Init Web Driver
driver = init.driver(browser)

# Make workdir
os.makedirs(directory_path, exist_ok=True)
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
    tags, dic = data_export.extract_tags(txtf)
    data_export.export_excel(tags, dic, tag_file_path)

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