#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 12:46:50 2023

@author: ml
"""

import pandas as pd
import os

def job_analysis(date):
    df_jobs = pd.read_json('job_'+ date.lstrip('0') +'.json')
    print(df_jobs.index)
    
job_analysis('0410')
