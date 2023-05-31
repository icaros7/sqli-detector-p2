import subprocess

from selenium import webdriver


def driver(browser):
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

    return webdriver.__getattribute__(browser)(executable_path=driver_executables.get(browser), options=options)


def module():
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


def args(thr):
    # Check argument validity
    try:
        if int(thr) < 1 or int(thr) > 11:
            print('Error: Thread option must be in range of 1, 10')
            exit()

    except ValueError:
        print('Error: Thread option must be Int type, in range of 1,10')
        exit()
