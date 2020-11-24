import pandas as pd 
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


binary = r'C:\Program Files\Mozilla Firefox\firefox.exe' #PATH YOUR firefox.exe
options = Options()
options.set_headless(headless=True)
options.binary = binary
cap = DesiredCapabilities().FIREFOX
cap["marionette"] = True #optional

driver = webdriver.Firefox(firefox_options=options, capabilities=cap, executable_path='geckodriver.exe')##path\to\geckodriver.exe
driver.get('https://www.transfermarkt.com.tr/wettbewerbe/europa')    

html = driver.page_source
soup = BeautifulSoup(html)

league_names = [] #initial name for start scraping
links = [] #initial link for start scraping

team_names = []
team_links = [] #inner  links
for i in range(26): #Determining the number of leagues to search
    reviews_selector = soup.select('#yw1 > table > tbody > tr:nth-child('+str(i+1)+') > td:nth-child(1) > table > tbody > tr > td:nth-child(2) > a')
    
        
     
    for tag in reviews_selector:
        league_names.append(tag.text)
    
        links.append("https://www.transfermarkt.com.tr" + tag.get('href'))
    
df = pd.DataFrame(list(zip(league_names,links)),
                  columns = ['league_names', 'links'])


for link in links:
    driver.get(link)   
    html2 = driver.page_source
    soup2 = BeautifulSoup(html2)
    
    reviews_selector2 = soup2.find_all('a', class_='vereinprofil_tooltip tooltipstered')
    
    
    for tag in reviews_selector2:
        team_links.append("https://www.transfermarkt.com.tr" + tag.get('href'))
        team_names.append(tag.text)
        
        
ex_frame = pd.DataFrame(list(zip(team_names,team_links)),
                  columns = ['team_names', 'team_links'])    
final_frame = ex_frame[~ex_frame['team_names'].str.split().str[-1].duplicated()] #delete duplicates
final_frame = final_frame.reset_index(drop=True) #reset index numbers because of deleting duplicates
final_frame.to_csv(teamlink.csv')

  
           


        
















