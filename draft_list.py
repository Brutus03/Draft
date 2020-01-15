#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# スクレイピングに必要なモジュールをインポート
import csv
import sys
sys.path.append('/home/pi/.local/lib/python3.5/site-packages/')
import time
import traceback

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Headless Chromeを使うためのオプション
options = webdriver.chrome.options.Options()
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
options.add_argument('--headless')
options.add_argument('--user-agent=#{user_agent}')

# ドライバー設定
browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", chrome_options=options)

# 関数
list = []
dict = {}
page = ""
last = 20 

def get_list_companies():
    url = "https://job-draft.jp/companies?page="
    url = url+str(page)
    browser.get(url)
    count = 21
    if not page:
        url = "https://job-draft.jp/companies"
    if page == 19:
        count = 18
    num = 1
    while num < count:
        try:
            company_name = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td.table-manage-col-6.text-center > a")
            if not company_name:
                company_name = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td.table-manage-col-6.text-center")
            gentleman = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td.table-manage-col-3.text-center")
            love_calls = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(4)")
            name = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(5)")
            consent = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(6)")
        except NoSuchElementException:
            print("要素がありませんでした")
            sys.exit(1)
        for company_name, gentleman, love_calls, name, consent in zip(company_name, gentleman, love_calls, name, consent):
            company_name = company_name.text
            gentleman = gentleman.text
            love_calls = love_calls.text
            name = name.text
            consent = consent.text
            consent = consent.replace('\n', '')
            print(company_name)
            print(gentleman)
            print(love_calls)
            print(name)
            print(consent)
            dict = {"company_name": company_name, "gentleman": gentleman, "love_calls": love_calls, "name": name, "consent": consent }
            list.append(dict)
            with open('./companies_list.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(dict.values())
            num += 1

def main2():
    print("データスクレイピングを開始します")
    global page
    try:
        if not page:
            get_list_companies()
            page = 2
            time.sleep(3)
        # 最後のページまでループ
        while page < last:
            get_list_companies()
            page += 1
            time.sleep(3)

    except Exception as e:
         traceback.print_exc()
         sys.exit(99)
    # ドライバを終了し、関連するすべてのウィンドウを閉じる
    browser.quit()
    print("データスクレイピングが正常終了しました")

# 処理
if __name__ == '__main__':
    main2()
