# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 22:04:26 2020

@author: alka
"""
import os
import glob
import pandas as pd
os.chdir(r"C:\Users\alka\Desktop\SCRAWLER")

extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]

#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv = combined_csv.reset_index(drop=True)
#combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')


#combined_csv['local_links'] = combined_csv['local_links'].map(lambda x: x.lstrip(r'C:\Users\alka\Desktop\SCRAWLER'))