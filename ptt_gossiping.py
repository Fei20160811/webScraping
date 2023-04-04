#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 17:34:10 2023

@author: ml
"""

import getWebPage
from bs4 import BeautifulSoup
import time
import json    
    
def get_articles(dom, date):
    soup = BeautifulSoup(dom, 'html.parser')
    
    paging_div = soup.find('div', 'btn-group btn-group-paging')
    prev_url = paging_div.find_all('a')[1]['href']
    
    articles = []
    divs = soup.find_all('div', 'r-ent')
    for d in divs:
        if d.find('div', 'date').text.strip() == date:
            push_count = 0
            push_str = d.find('div', 'nrec').text
            if push_str:
                try:
                    push_count = int(push_str)
                except ValueError:
                    if push_str == '爆':
                        push_count = 99
                    elif push_str.startswith('X'):
                        push_count = -10
                        
            if d.find('a'):
                href = d.find('a')['href']
                title = d.find('a').text
                author = d.find('div', 'author').text if d.find('div', 'author') else ''
            
                articles.append({
                    'title':title,
                    'href':href,
                    'push_count':push_count,
                    'author':author
                    })
    return articles, prev_url

PTT_URL = 'https://www.ptt.cc'
current_page = getWebPage.get_web_page(PTT_URL + '/bbs/Gossiping/index.html')

if current_page:
    articles = []
    today = time.strftime("%m/%d").lstrip('0')
    current_articles, pre_url = get_articles(current_page, today)
    
    while current_articles:
        articles += current_articles
        current_page = getWebPage.get_web_page(PTT_URL + pre_url)
        current_articles, pre_url = get_articles(current_page, today)
        
print('今天有', len(articles), '篇文章')
threshold = 50
#print('熱門文章(> %d 推):' %(threshold)）
for a in articles:
    if int(a['push_count'] > threshold):
        print(a)
        
with open('gossiping.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, indent = 2, sort_keys=True, ensure_ascii=False)

    