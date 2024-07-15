'''
NOTE: This program scrapes ################### for https proxies
which are updated often. Proxies found are appended to a .bin file
This process is repeated indefinately every x-minutes and any 
newly added proxies to the site will be compared to the data in the 
output file. If the proxyaddr:port combination does not already exist
within the file, it will be appended to the file. 
File does not write duplicate data.

NOTE: Press key [ctl + c] to quit.
'''
from bs4 import BeautifulSoup as sp
import requests
import re
import time

PROXY_SITE_URL:str = "#####################"
OF_HANDLE:str = 'proxies.bin'
SLEEP_TIME:int = 1800 #30 minutes
START_FILE_READ:tuple = (0, 0)

def write_file(proxies:list):
    with open(OF_HANDLE, mode='ab+') as fhandle:
        for i, x in enumerate(proxies, start=0):
            fhandle.seek(*START_FILE_READ)
            if(not re.search(x, fhandle.read().decode('utf-8', errors='ignore'))):
                fhandle.write((f'{x}\n').encode('utf-8'))      
                
def get_https_proxies():
    raw_data:object = sp(requests.get(PROXY_SITE_URL).text, 'html.parser')
    textarea:object = raw_data.find('textarea')
    proxies:list = re.findall('([0-9\S]*\:0?[0-9]*)',str(textarea))[1:]
    write_file(proxies)

def main():
    print('\nGathering proxies...\nPress "ctl + c" to quit or close the window.')
    while(True):
        try:
            get_https_proxies()
            #pause between iterations
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            break
    print('exiting')
    
if __name__=='__main__':
    main()
