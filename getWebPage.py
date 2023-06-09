#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:19:59 2023

@author: ml
"""
import requests
import random
import time

def get_web_page(url):
    resp = requests.get(url = url)
                        #cookies = {'over18':'1'}) #針對ptt 18歲許可跳窗所需
    #隨機暫停1～5秒
    time.sleep(random.uniform(1, 5))
                    
    if resp.status_code != 200:
        print(resp.status_code)
        print('Invalid url:', resp.url)
        return None
    else:
        return resp.text