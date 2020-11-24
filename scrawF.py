"""
Created on Fri Oct 16 23:07:42 2020

@author: abdullah alka kandilli
"""

#%%

import pandas as pd 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request
import os
import sys


team_infos = sys.argv
#%%


binary = r'C:\Program Files\Mozilla Firefox\firefox.exe' #PATH YOUR firefox.exe
options = Options()
options.set_headless(headless=True)
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True #optional

driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path=r'C:\Users\alka\Desktop\SCRAWLER\geckodriver.exe')##path\to\geckodriver.exe

driver.get(team_infos[1]) #get team url from cmd argv 

html = driver.page_source
soup = BeautifulSoup(html)

names = [] #initial name for start scraping
links = [] #initial link for start scraping
position = [] #inner links positions
image_links = [] #inner image links
team = [] #inner team info
local_link = [] #local directory link for every image

reviews_selector = soup.find_all('a', class_='spielprofil_tooltip tooltipstered')
     
for tag in reviews_selector:
    names.append(tag.text)
    
    links.append("https://www.transfermarkt.com.tr" + tag.get('href'))
           
df = pd.DataFrame(list(zip(names,links)),
                  columns = ['names', 'links'])

for link in df.links:
    driver.get(link)   
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2)
    
    reviews_selector2 = soup2.find_all('div', class_='large-6 large-pull-6 small-12 columns spielerdatenundfakten')
    position_selector = soup2.select('#main > div:nth-child(10) > div > div > div.dataContent > div > div:nth-child(2) > p:nth-child(2) > span.dataValue')
    imglink_selector = soup2.select('#main > div:nth-child(10) > div > div > div.dataBild > img')
    
    for tag in position_selector:
        c_name = tag.text.strip()
        position.append(c_name)  
        team.append(team_infos[2])
        
    for tag in imglink_selector:
       
        image_links.append(tag.get('src'))
           
        
        
ex_frame = pd.DataFrame(list(zip(names,position,image_links,team)),
                           columns = ['names','position','image_links','team'])
ex2_frame = ex_frame[~ex_frame['names'].str.split().str[-1].duplicated()]
final_frame = ex2_frame.reset_index(drop=True)# I reset the indexes because the indexes do not match each other when adding the local links of the downloaded photos


FILE_PATH = r'C:\Users\alka\Desktop\SCRAWLER'
FINAL_PATH = '{}\{}'.format(FILE_PATH, team_infos[2]) # team directory name

# Create target directory & all intermediate directories if don't exists
os.makedirs(FINAL_PATH)


def url_to_jpg(i, jpg, file_path):
        '''
         Args:
             -- i = number of image
             -- url = a URL adress of a given şmage
             -- file_path = where to save final
             '''
    
        filename = 'image-{}.jpg'.format(i)
        full_path = '{}\{}'.format(file_path, filename)
        urllib.request.urlretrieve(url, full_path)
        local_link.append(full_path)

for i,url in enumerate(final_frame.image_links):
    url_to_jpg(i,url,FINAL_PATH)

local_link_values = pd.Series(local_link)
final_frame.insert(loc=0, column='local_links', value=local_link_values)

filename2 = team_infos[2]+'.csv'
x_path = r'C:\Users\alka\Desktop\SCRAWLER'
full_path2 = '{}\{}'.format(x_path, filename2)


final_frame.to_csv(full_path2)

driver.quit()














