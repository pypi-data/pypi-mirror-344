import time

from selenium.common import ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from qte_parts_crawler.utils.bypass_recaptcha import bypass_recaptcha
from qte_parts_crawler.utils.admin_server_api import post_crawl_detail, post_crawl_prepare, get_prepare_tasks
from qte_parts_crawler.utils.actions import PageActions
import random
import argparse
import subprocess
import platform


# CONFIGURATION
url = "https://www.showmetheparts.com/"

p_submit_button_captcha = "//a[@id='button-1408']"

id_input_year = "//input[@id='combo-1060-inputEl']"
id_input_make = "//input[@id='combo-1061-inputEl']"
id_input_model = "//input[@id='combo-1062-inputEl']"
id_input_part_type = "//input[@id='combo-1063-inputEl']"
id_input_engine = "//input[@id='combo-1064-inputEl']"

xpath_trigger_year = "//div[@id='combo-1060-trigger-picker']"
xpath_trigger_make = "//div[@id='combo-1061-trigger-picker']"
xpath_trigger_model = "//div[@id='combo-1062-trigger-picker']"
xpath_trigger_part_type = "//div[@id='combo-1063-trigger-picker']"
path_trigger_engine = "//div[@id='combo-1064-trigger-picker']"

xpath_picker_year = "//ul[@id='combo-1060-picker-listEl']"
xpath_picker_make = "//ul[@id='combo-1061-picker-listEl']"
xpath_picker_model = "//ul[@id='combo-1062-picker-listEl']"
xpath_picker_part_type = "//ul[@id='combo-1063-picker-listEl']"
xpath_picker_engine = "//ul[@id='combo-1064-picker-listEl']"

xpath_message_box_1001 = "//div[@id='messagebox-1001']"
xpath_message_box_button = "//div[@id='messagebox-1001']//a[@id='button-1005']"

xpath_parts_view_list_wrap = "//div[@class='PartsViewListWrap']"

xpath_view_list = "//a[@id='button-1071']"
xpath_view_grid = "//a[@id='button-1072']"

fields = ["Supplier", "Location", "Brand", "Part Number", "Part Type", "Comment", "Application", "Qty"]

id_header = '__header'
xpath_header = '//div[@id="__header"]'

message_no_parts = 'No part(s) found matching the specified application.'
message_no_coverage = 'No coverage available for'

PROXIES = []


def get_random_proxy():
    return random.choice(PROXIES)


def extract_part_details(browser):
    part_details = []
    WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.XPATH, xpath_parts_view_list_wrap)))
    products = browser.find_elements(By.XPATH, xpath_parts_view_list_wrap)
    for item in products:
        part_detail = extract_part_detail(item)
        part_details.append(part_detail)
    return part_details


def extract_part_detail(container):
    # Extract texts
    data = {}
    for field in fields:
        try:
            field_element = container.find_element(By.XPATH, f'.//div[span[contains(text(),"{field}:")]]')
            value = field_element.text.replace(f"{field}:", '').strip()
            data[field] = value
        except Exception as e:
            data[field] = ''
    print(data)
    return data


def crawl_prepare(year: str, debugMode=False, use_proxy=False) -> None:
    print(f'Crawling tasks', year)

    browser = open_browser(debugMode, use_proxy)

    if not debugMode:
        bypass_recaptcha(browser, p_submit_button_captcha)

    page_actions = PageActions(browser)
    page_actions.fulfill_input(id_input_year, year, xpath_header)

    makes = page_actions.fetch_all_ul_value(xpath_picker_make)
    for make in makes:

        page_actions.fulfill_input(id_input_make, make, xpath_header)
        time.sleep(2)
        page_actions.click_ok_if_starts_with(message_no_coverage)

        try:
            models = page_actions.fetch_all_ul_value(xpath_picker_model)
        except TimeoutException:
            print(f'No models found for {year}, {make}')
            continue

        for model in models:
            post_crawl_prepare(year, make, model)


def crawl_details(year: str, make: str, model: str, debugMode=False, use_proxy=False) -> None:
    print(f'Crawling details for {year}, {make}, {model}')

    browser = open_browser(debugMode, use_proxy)
    if not debugMode:
        # bypass recaptcha and click the submit button
        bypass_recaptcha(browser, p_submit_button_captcha)

    page_actions = PageActions(browser)

    page_actions.fulfill_input(id_input_year, year, xpath_header)
    page_actions.fulfill_input(id_input_make, make, xpath_header)
    # page_actions.fulfill_input(id_input_model, model, xpath_header)
    page_actions.click_li(model)

    try:
        part_types = page_actions.fetch_all_ul_value(xpath_picker_part_type)
    except TimeoutException:
        part_type_value = page_actions.get_input_value(id_input_part_type)
        part_types = [part_type_value]
        print(f'Part type not found, using value: {part_type_value}')

    for part_type in part_types:
        page_actions.fulfill_input(id_input_part_type, part_type, xpath_header)
        # page_actions.click_ok_if_exists_text(text=message_no_parts, timeout=2)

        try:
            engines = page_actions.fetch_all_ul_value(xpath_picker_engine)
        except TimeoutException:
            engines = ['All']
        # 如果这里找不到 engine,
        for engine in engines:
            page_actions.fulfill_input(id_input_engine, engine, xpath_header)

            page_actions.click_ok_if_starts_with(text=message_no_parts, timeout=2)
            time.sleep(2)
            # Click Grid view
            try:
                page_actions.get_clickable_element(xpath_view_grid).click()
            except ElementClickInterceptedException:
                print(f"Element {xpath_view_grid} not clickable")
                continue

            parts = extract_part_details(browser)
            for part in parts:
                post_crawl_detail(year, make, model, part_type, engine, part)


def open_debug_browser():
    system_name = platform.system()
    # if the operating system is MacOS, use the following command to open the browser
    # /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \ --remote-debugging-port=9222 \ --user-data-dir="/tmp/chrome-debug"
    if system_name == 'Windows':
        print("Windows OS detected")
        subprocess.Popen([
            "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
            "--remote-debugging-port=9222",
            "--user-data-dir=C:\\tmp\\chrome-debug"
        ])
    elif system_name == 'Darwin':
        # MacOS
        print("MacOS detected")
        subprocess.Popen([
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "--remote-debugging-port=9222",
            "--user-data-dir=/tmp/chrome-debug"
        ])
    else:
        print(f'Unsupported OS: {system_name}')


def open_browser(debugMode: bool, use_proxy: bool) -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)...")

    if debugMode:
        options.debugger_address = "127.0.0.1:9222"
    else:
        # options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--user-data-dir=/tmp/chrome-debug')

    if use_proxy:
        proxy = get_random_proxy()
        options.add_argument(f'--proxy-server={proxy}')
        print(f'Using proxy: {proxy}')

    browser = webdriver.Chrome(options=options)
    # open a selenium browser with the url
    if not debugMode:
        browser.get(url)
    return browser


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Crawl tasks and details from ShowMeTheParts')
    parser.add_argument('--task', type=str, help='Task to perform: browser, prepare, details')
    parser.add_argument('--year', type=int, help='Year to crawl', default=2025)
    parser.add_argument('--count', type=int, help='Count of tasks to crawl', default=3)
    args = parser.parse_args()
    # print(args)
    if args.task == 'browser':
        open_debug_browser()
    elif args.task == 'prepare':
        crawl_prepare(year=args.year, debugMode=True, use_proxy=False)
    elif args.task == 'details':
        tasks = get_prepare_tasks(count=args.count)
        data = tasks.get('data')
        print(data)
        if not data or len(data) == 0:
            print('No tasks to crawl')
            exit(0)
        for item in data:
            print(item)
            crawl_details(year=item['year'],
                          make=item['make'],
                          model=item['model'],
                          debugMode=True,
                          use_proxy=False)

        # crawl_details(year='2022', make='AUDI', model='A1', debugMode=True, use_proxy=False)
