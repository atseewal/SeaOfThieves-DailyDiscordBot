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
    from bs4 import BeautifulSoup
    import re
    import time
    
    # Driver Setup
    chromedriver = r'C:\Users\seewa\Documents\drivers\chromedriver.exe'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=chromedriver, options = chrome_options)
    
    #Login
    driver.get('https://www.seaofthieves.com/login')
    driver.find_element_by_name('loginfmt').send_keys(username)
    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').send_keys(Keys.ENTER)
    driver.find_element_by_name('passwd').send_keys(password)
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="idSIButton9"]').send_keys(Keys.ENTER)
    
    driver.implicitly_wait(5)
    driver.find_element_by_id('idSIButton9').send_keys(Keys.ENTER)
    
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