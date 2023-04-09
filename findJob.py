#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 14:33:33 2023

@author: ml
"""
import getWebPage
import time
from bs4 import BeautifulSoup
import json

def find_jobs(dom, date):

    #with open('job.html') as file:
    soup = BeautifulSoup(dom, 'html.parser')
    jobs = []
    divs = soup.find_all('article', 'b-block--top-bord job-list-item b-clearfix js-job-item')
    for d in divs:
        job = {}
        from_date = d.find('span', 'b-tit__date')
        #如果不是當天的工作資料則不抓取
        if from_date.text.strip() == date: 
            
            job_items = d.find_all('a')
            company_level = from_date.parent.next_sibling.next_sibling
            company_desc = find_company_desc('https:' + job_items[1]['href'])
            
            job["job_name"] = job_items[0].text
            job["job_url"] = job_items[0]['href']
            job["job_desc"] = find_job_desc('https:'+ job_items[0]['href'])
            job["company_name"] = job_items[1].text
            job["company_url"] = job_items[1]['href']
            #如果公司資訊有資料才取值
            job["company_desc"] = company_desc[0].text if company_desc[0] else ''
            job["company_benefit"] = company_desc[1].text if company_desc[1] else ''
            job["indcat_name"] = company_level.find_all('li')[-1].text
            job["company_addr"] = company_level.next_sibling.next_sibling.find('li').text
            job["apply_nums"] = job_items[-1].text
                     
            '''
            (V)job_name
            (V)job_url 
            (V)job_desc
            (V)company_name
            (V)company_url
            (V)company_desc
            (V)Indcat_name
            (V)company_addr
            (V)apply_nums

            '''
            jobs.append(job)
        else:
            break
                
    return jobs
        
        

def find_job_desc(url):
    current_job = getWebPage.get_web_page(url)
    soup = BeautifulSoup(current_job, 'html.parser')
    return soup.find('div', 'job-description col-12').text

def find_company_desc(url):
    print(url)
    current_job = getWebPage.get_web_page(url)
    soup = BeautifulSoup(current_job, 'html.parser')
    return [soup.find('p', 'r3 mb-0 text-break'), soup.find('div', 'row benefits-description')]


def find_job_page(keyword):
    #抓取使用關鍵字查詢的當日職缺資訊
    #ro => 0:全部 1:全職
    #order => 17:依日期排序
    #page => 一頁抓取20筆工作資料，一天更新幾頁？
    #從第一頁開始抓取當日資料
    jobs = []
    page = 1
    while True:
        job_url = 'https://www.104.com.tw/jobs/search/?ro=1&keyword='+ keyword +'&order=17&page='+ str(page)
        current_page = getWebPage.get_web_page(job_url)
    
        if current_page:
            
            today = time.strftime('%m/%d').lstrip('0')
            current_jobs = find_jobs(current_page, today)
            #如果不為空list，則繼續往下抓取資料
            if current_jobs:
                jobs.append(current_jobs)
                #往下一頁抓取工作資料   
                page +=1 
            else:
                break
    
    with open('job_'+ str(today).replace('/','') +'.json', 'w', encoding='utf-8') as file:
        json.dump(jobs, file, indent = 2, sort_keys = True, ensure_ascii = False)


find_job_page('python')

