import pandas as pd
import os
import time


df = pd.read_csv(r'C:\Users\alka\Desktop\SCRAWLER\teamlink.csv')
link_list = []
team_names = []

 
for link in df.team_links:
    link_list.append(link)
    
for names in df.team_names:
    team_names.append(names)   
    
os.chdir(r'C:\Users\alka\Desktop\SCRAWLER') 
g = os.getcwd() 

program_starts = time.time()
for i in range(436):
    reponse = os.system('py scrawF.py ' + str(link_list[i+344]) + ' ' + str(team_names[i+344]).replace(' ',''))

    print(reponse)
    now = time.time()
    print("It has been {0} seconds since the loop started".format(now - program_starts))
    


