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
options.add_argument('--headless')

# ドライバー設定
browser = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", chrome_options=options)

# 関数
list = []
dict = {}

def get_results():
    url = "https://job-draft.jp/festivals"
    browser.get(url)
    count = 23
    num = 1
    while num < count:
        try:
            times = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(1) > a")
            num_participants = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(2)")
            num_participating_com = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(3)")
            total_nominations = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(4)")
            ave_annual_income = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(5)")
            cent_annual_income = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(6)")
            presen_annual_income = browser.find_elements_by_css_selector("#page-wrapper > div.container > div > div:nth-child(2) > div.ibox-content > table > tbody > tr:nth-child("+(str(num))+") > td:nth-child(7)")
        except NoSuchElementException:
            print("要素がありませんでした")
            sys.exit(1)
        for times, num_participants, num_participating_com, total_nominations, ave_annual_income, cent_annual_income, presen_annual_income in zip(times, num_participants, num_participating_com, total_nominations, ave_annual_income, cent_annual_income, presen_annual_income):
            times = times.text
            num_participants = num_participants.text
            num_participating_com = num_participating_com.text
            total_nominations = total_nominations.text
            ave_annual_income = ave_annual_income.text
            ave_annual_income = ave_annual_income.replace('万円', '')
            cent_annual_income = cent_annual_income.text
            cent_annual_income = cent_annual_income.replace('万円', '')
            presen_annual_income = presen_annual_income.text
            presen_annual_income = presen_annual_income.replace('億円', '')
            print(times)
            print(num_participants)
            print(num_participating_com)
            print(total_nominations)
            print(ave_annual_income)
            print(cent_annual_income)
            print(presen_annual_income)
            dict = {"times": times, "num_participants": num_participants, "num_participating_com": num_participating_com, "total_nominations": total_nominations, "ave_annual_income": ave_annual_income, "cent_annual_income": cent_annual_income, "presen_annual_income": presen_annual_income }
            list.append(dict)
            with open('./past_bid_results.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(dict.values())
            num += 1

def main3():
    print("データスクレイピングを開始します")
    try:
        get_results()
    except Exception as e:
        traceback.print_exc()
        sys.exit(99)
    # ドライバを終了し、関連するすべてのウィンドウを閉じる
    browser.quit()
    print("データスクレイピングが正常終了しました")

# 処理
if __name__ == '__main__':
    main3()
