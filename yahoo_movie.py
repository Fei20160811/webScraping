#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 15:59:36 2023

@author: ml
"""
import getWebPage
from bs4 import BeautifulSoup
import re
import json

from lxml import html

def get_movie_id(url):
    return url.split('-')[-1]

def get_date(data):
    pattern = '\d+-\d+-\d+'
    match = re.search(pattern, data)

    if match is None:
        return data
    else:
        return match.group(0)
  

def get_movies(dom):

    '''
    從本機讀取html檔案，驗證抓取內容是否正確
    with open('./movie.html', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'lxml')
    
    '''
    
    soup = BeautifulSoup(dom, 'lxml')
    
    movies = []
    rows = soup.find_all('div', 'release_info_text')

    
    for row in rows:
        movie = {}
        
        movie["expectation"] = row.find('div', 'leveltext').span.text.strip()
        movie["ch_name"] = row.find('div', 'release_movie_name').a.text.strip()
        movie["eng_name"] = row.find('div', 'release_movie_name').find('div', 'en').a.text.strip()
        movie["movie_id"] = get_movie_id(row.find('div', 'release_movie_name').a['href'])
        movie['poster_url'] = row.parent.find_previous_sibling('div', 'release_foto').a.img['data-src']
        movie['release_date'] = get_date(row.find('div', 'release_movie_time').text)
        movie["intro"] = row.find('div', 'release_text').text.replace(u'詳全文', '').strip()
        
        trailer_a = row.find_next_sibling('div', 'release_btn color_btnbox').find_all('a')[1]
        movie["trailer_url"] = trailer_a['href'] if 'href' in trailer_a.attrs else ''
        movies.append(movie)
    
    return movies



page = getWebPage.get_web_page('https://movies.yahoo.com.tw/movie_thisweek.html')
if page:
    movies = get_movies(page)
    '''for movie in movies:
        print(movie)'''
    with open('movie.json', 'w', encoding='utf-8') as f:
        json.dump(movies, f, indent=2, sort_keys=True, ensure_ascii = False)