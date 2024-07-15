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
SLEEP_TIME:int = 3600; #1hr
START_FS_POINT:tuple = (0x00, 0x00)

def write_file(proxies:list):
    unique:int = 0x00
    with open(OF_HANDLE, mode='ab+') as fhandle:
        for i, x in enumerate(proxies, start=0):
            fhandle.seek(*START_FS_POINT)
            if(not re.search(x, fhandle.read().decode('utf-8','ignore'))):
                fhandle.write((f'{x}{chr(0x0a)}').encode('utf-8')); 
                unique+=0x01
    return unique    
                
def get_https_proxies():
    raw_data:object = sp(requests.get(PROXY_SITE).text, 'html.parser')
    textarea:object = raw_data.find('textarea')
    proxies:list = re.findall(r'([0-9\S]*\:0?[0-9]*)',str(textarea))[1:]
    proxies_written:int = write_file(proxies)
    return proxies_written

def main():
    iteration_count:int = 0x01
    total_proxies:int = 0x00
    print('\nGathering proxies...')
    
    
    while(True):
        try:
            new_proxies:int = get_https_proxies()
            print('='*25)
            print(f'Scrape Iteration: {iteration_count}')
            print(f'Unique Proxies Found: {new_proxies}')
            print(f'Total Unique Proxies: {total_proxies}')
            print('='*25)
            iteration_count+=0x01
            print('Press "ctl + c" to quit scraping...')
            time.sleep(SLEEP_TIME)
        except KeyboardInterrupt: break
    print('Exiting')
