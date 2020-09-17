# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 13:28:01 2020

@author: atseewal
"""

#%% Create Function
def daily_bounties(username, password):
    # imports
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from bs4 import BeautifulSoup
    from dotenv import load_env
    import re, time, os
    
    # Load Environment
    load_dotenv('.env')
    
    # Driver Setup
    chromedriver = os.getenv('CHROME_DRIVER')
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chromedriver, options = chrome_options)
    
    #Login
    driver.get('https://www.seaofthieves.com/login')
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.NAME, 'loginfmt'))).send_keys(username)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').send_keys(Keys.ENTER)
    wait.until(EC.element_to_be_clickable((By.NAME, 'passwd'))).send_keys(password)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').send_keys(Keys.ENTER)
    
    wait.until(EC.element_to_by_clickable((By.ID, 'idSIButton9').send_keys(Keys.ENTER)
    
    time.sleep(2)
    if re.search('seaofthieves', driver.current_url):
        driver.get('https://www.seaofthieves.com/event-hub/')
    else:
        print('You were not returned to a sea of thieves page, login may have been unsuccessful')
    
    #Get the Daily bounty info
    d_bounty_htmltext=driver.page_source
    d_bounty_soup = BeautifulSoup(d_bounty_htmltext, 'lxml')
    d_bounty_title = d_bounty_soup.find('div', class_='bounty-panel__item bounty-panel__item--active').find('h2', class_='bounty-panel__title').get_text()
    d_bounty_description = d_bounty_soup.find('div', class_='bounty-panel__item bounty-panel__item--active').find('p', class_='bounty-panel__copy').get_text()
    d_bounty_time = d_bounty_soup.find('div', class_='bounty-panel__item bounty-panel__item--active').find('p', class_='bounty-panel__dates').get_text()
    
    #Create new bounty info
    d_bounty_end = re.findall(r'[A-Z][a-z]+\s\d{1,2}\w{2}:\s\d{1,2}:\d{2}\w{2}', d_bounty_time)[1]
    d_bounty_type = re.findall(r'gold|doubloons', d_bounty_description)[0]
    
    d_bounty_info = {'Title': d_bounty_title, 'Description': d_bounty_description, 'Bounty_End': d_bounty_end, 'Bounty_Type': d_bounty_type}
    
    driver.close()
    
    return(d_bounty_info)
