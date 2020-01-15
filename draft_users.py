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

# ログイン情報
USER = "user"
PASS = "pass"

# ログイン画面を表示
url_login = "https://job-draft.jp/sign_in"
browser.get(url_login)
time.sleep(1)
print("ログインページにアクセスしました")

# フォームにメールアドレスとパスワードを入力
e = browser.find_element_by_id("user_email")
e.clear()
e.find_element_by_id("user_email").send_keys(USER)

e = browser.find_element_by_id("user_password")
e.clear()
e.find_element_by_id("user_password").send_keys(PASS)

time.sleep(1)

# フォームを送信
e.find_element_by_xpath("//*[@id=\"new_user\"]/div[4]").click()
print("ログインしました")

# 関数
list = []
dict = {}
page = ""
last = 50

def get_user_data():
    url = "https://job-draft.jp/festivals/22/users?page="
    url = url+str(page)
    browser.get(url)
    count = 12
    if page == 49:
        count = 8
    num = 2
    while num < count:
        try:
            user = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-3 > div:nth-child(2) > a > span")
            age = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-3 > div:nth-child(3) > span")
            name = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-9 > div.row > div.col-xs-4.col-sm-3.col-md-3.col-lg-3 > span.f-w-bold.u-font-ml")
            max_amount = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-9 > div.row > div:nth-child(2) > span.f-w-bold.u-font-ml")
            cum_avg = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-9 > div.row > div:nth-child(3) > span.f-w-bold.u-font-ml")
            ambition = browser.find_elements_by_css_selector("#page-wrapper > div.wrapper-content > div > div > div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.ibox > div > div > div:nth-child("+(str(num))+") > div > div.col-xs-9 > div.u-m-t-5 > div:nth-child(1) > span.f-w-bold.u-font-mm")
        except NoSuchElementException:
            print("要素がありませんでした")
            sys.exit(1)
        for user, age, name, max_amount, cum_avg, ambition in zip(user, age, name, max_amount, cum_avg, ambition):
            user = user.text
            age = age.text
            name = name.text
            max_amount = max_amount.text
            max_amount = max_amount.replace('万円', '')
            cum_avg = cum_avg.text
            cum_avg = cum_avg.replace('万円', '')
            ambition = ambition.text
            print(user)
            print(age)
            print(name)
            print(max_amount)
            print(cum_avg)
            print(ambition)
            dict = {"user": user, "age": age, "name": name, "max_amount": max_amount, "cum_avg": cum_avg, "ambition": ambition }
            list.append(dict)
            with open('./user_ranking.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(dict.values())
            num += 1

def main():
    print("データスクレイピングを開始します")
    global page
    global last
    try:
        if not page:
            get_user_data()
            page = 2
            time.sleep(3)
        # 最後のページまでループ
        while page < last:
            get_user_data()
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
    main()
