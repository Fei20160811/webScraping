#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:46:50 2023

@author: ml
"""

import pandas as pd
import os
import csv

def job_analysis(date):
    output_list = []
    df_jobs = pd.read_json('job_'+ date.lstrip('0') +'.json', orient='records')
    df_jobs = [job_arr for index in df_jobs for job_arr in df_jobs[index] if job_arr != None]
    df_jobs = pd.DataFrame(df_jobs)
    df_jobs["company_addr"] = df_jobs["company_addr"].str[:3]
    df_jobs = df_jobs[df_jobs["company_addr"].isin(['台北市' ,'新北市', '新竹市', '新竹縣'])]
       
    print(df_jobs.groupby(["company_name", "company_desc"]))
    for key, item in df_jobs.groupby(["company_name", "company_desc"]):
        job_row = (key[0], key[1], item["job_name"], item["company_addr"])
        output_list.append(job_row)
        
    with open('job_'+ date.lstrip('0') +'.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['公司名稱', '公司產品','職稱', '公司所在縣市'])
        for item in output_list:
            writer.writerow(item)
    
job_analysis('0411')
