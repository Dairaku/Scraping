#!/usr/bin/env python
# coding: utf-8

import csv
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import re
import pandas as pd
import time

base_url = "https://tabelog.com/tokyo/A1304/A130401/rstLst/"
begin_page = 1
end_page = 10

#最終ページの計算用
r_base = requests.get(base_url)
soup_base = BeautifulSoup(r_base.content, 'html.parser')

page_num = begin_page

#csvリストの作成
csvlist = [["store_name", "score", "review_num", "url", "category_name", "reserve_tel", "prefecture", "district", "seat_num", "facebook", "restaurant_tel", "homepage", "open_date"]]

#CSVファイルを開く。ファイルがなければ新規作成する。
f = open("output.csv", "w", encoding="utf_8_sig")
writecsv = csv.writer(f, lineterminator='\n')

while True:
    list_url = base_url + str(page_num) + "/"
    print(list_url)

    # 一覧ページで、ページネーション順に取得
    r1 = requests.get(list_url)
    soup1 = BeautifulSoup(r1.content, 'lxml')
    soup_a_list = soup1.find_all('a', class_='list-rst__rst-name-target')

    # 店の個別ページURLを取得
    for soup_a in soup_a_list:
        item_url = soup_a.get('href')
        print(item_url)

        r = requests.get(item_url)
        soup = BeautifulSoup(r.content, 'lxml')

        #点数
        try:
            score = soup.find("span", class_="rdheader-rating__score-val-dtl").get_text()
            print(score)
        except:
            score="NULL"
            pass
        print(score)

        # 口コミ数
        try:
            review_num = soup.find("em", class_="num").get_text()
        except:
            review_num="NULL"
            pass
        print(review_num)

        #情報取得
        info = str(soup)

        #店舗名
        try:
            store_name = info.split('display-name')[1].split('<span>')[1].split('</span>')[0].strip()
        except:
            store_name="NULL"
            pass
        print(store_name)

        #ジャンル名
        try:
            category_name = info.split('<th>ジャンル</th>')[1].split('<td>')[1].split('</td>')[0].split('<span>')[1].split('</span>')[0].strip()
        except:
            category_name="NULL"
            pass
        print(category_name)

        #予約電話番号
        try:
            reserve_tel = info.split('<strong class="rstinfo-table__tel-num">')[1].split('</strong>')[0].strip()
        except:
            reserve_tel="NULL"
            pass
        print(reserve_tel)

        #都道府県
        try:
            prefecture = info.split('<p class="rstinfo-table__address">')[1].split('/">')[1].split('</a>')[0].strip()
        except:
            prefecture="NULL"
            pass
        print(prefecture)

        #区
        try:
            district = info.split('<p class="rstinfo-table__address">')[1].split('/rstLst/')[1].split('">')[1].split('</a>')[0].strip()
        except:
            district="NULL"
            pass
        print(district)

        #席数
        try:
            seat_num = info.split('<th>席数</th>')[1].split('<td>')[1].split('</td>')[0].split('<p>')[1].split('席</p>')[0].strip()
        except:
            seat_num="NULL"
            pass
        print(seat_num)

        #公式アカウント facebook
        try:
            facebook = info.split('rstinfo-sns-link rstinfo-sns-facebook')[1].split('<span>')[1].split('</span>')[0].strip()
        except:
            facebook="NULL"
            pass
        print(facebook)

        #電話番号
        try:
            restaurant_tel = info.split('<th>電話番号</th>')[1].split('<strong class="rstinfo-table__tel-num">')[1].split('</strong>')[0].strip()
        except:
            restaurant_tel="NULL"
            pass
        print(restaurant_tel)

        #ホームページ
        try:
            homepage = info.split('<th>ホームページ</th>')[1].split('<span>')[1].split('</span>')[0].strip()
        except:
            homepage="NULL"
            pass
        print(homepage)

        #オープン日
        try:
            open_date = info.split('rstinfo-opened-date">')[1].split('</p>')[0].strip()
        except:
            open_date="NULL"
            pass
        print(open_date)

        #csvリストに順に追加
        csvlist.append([store_name, score, review_num, item_url, category_name, reserve_tel, prefecture, district, seat_num, facebook, restaurant_tel, homepage, open_date])

    if page_num >= end_page:
        print(csvlist)
        break
    page_num += 1

# 出力
writecsv.writerows(csvlist)
# CSVファイルを閉じる
f.close()
