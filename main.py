from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
import pandas as pd
import urllib.request
from bs4 import BeautifulSoup
import requests
import re
import pyautogui
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.common.exceptions import InvalidArgumentException, StaleElementReferenceException
from datetime import date
import mysql.connector as mc
import xlsxwriter
############################################################################################    
########################################## DATA CLEAN/PROCESSING ##################################################
############################################################################################
def postcodeDict():
    postcodeUKDict = {'AB' : 'Aberdeen', 'AL' : 'St Albans', 'B' : 'Birmingham', 'BA' : 'Bath', 'BB' : 'Blackburn', \
                  'BD' : 'Bradford', 'BH' : 'Bournemouth', 'BL' : 'Bolton', 'BN' : 'Brighton', 'BR' : 'Bromley', \
                  'BS' : 'Bristol', 'BT' : 'Belfast', 'CA' : 'Carlisle', 'CB' : 'Cambridge', 'CF' : 'Cardiff', \
                  'CH' : 'Chester', 'CM' : 'Chelmsford', 'CO' : 'Colchester', 'CR' : 'Croydon', 'CT' : 'Canterbury', \
                  'CV' : 'Coventry', 'CW' : 'Crewe', 'DA' : 'Dartford', 'DD' : 'Dundee', 'DE' : 'Derby', \
                  'DG' : 'Dumfries/Dumfries and Galloway', 'DH' : 'Durham', 'DL' : 'Darlington', 'DN' : 'Doncaster', \
                  'DT' : 'Dorchester', 'DY' : 'Dudley', 'E' : 'London E', 'EC' : 'London EC', 'EH' : 'Edinburgh', \
                  'EN' : 'Enfield', 'EX' : 'Exeter', 'FK' : 'Falkirk and Striling', 'FY' : 'Blackpool/Fyde', \
                  'G' : 'Glasgow', 'GL' : 'Gloucester', 'GU' : 'Guildford', 'GY' : 'Guernsey', 'HA' : 'Harrow', \
                  'HD' : 'Huddersfield', 'HG' : 'Harrogate', 'HP' : 'Hemel Hempstead', 'HR' : 'Hereford', \
                  'HS' : 'Outer Hebridies', 'HU' : 'Hull', 'HX' : 'Halifax', 'IG' : 'Ilford', 'IM' : 'Isle of Man', \
                  'IP' : 'Ipswich', 'IV' : 'Iverness', 'JE' : 'Jersey', 'KA' : 'Kilmarnock', 'KT' : 'Kingston Upon Thames', \
                  'KW' : 'Kirkwall', 'KY' : 'Kirkcaldy', 'L' : 'Liverpool', 'LA' : 'Lancaster', 'LD' : 'Llandrindod Wells', \
                  'LE' : 'Leicester', 'LL' : 'Llandudno', 'LN' : 'Lincoln', 'LS' : 'Leeds', 'LU' : 'Luton', \
                  'M' : 'Manchester', 'ME' : 'Rochester/Maidstone', 'MK' : 'Milton Keynes', 'ML' : 'Motherwell', \
                  'N' : 'London N', 'NE' : 'Newcastle Upon Tyne', 'NG' : 'Nottingham', 'NN' : 'Northampton', \
                  'NP' : 'Newport', 'NR' : 'Norwich', 'NW' : 'London NW', 'OL' : 'Oldham', 'OX' : 'Oxford', \
                  'PA' : 'Paisley', 'PE' : 'Peterborough', 'PH' : 'Perth', 'PL' : 'Plymouth', 'PO' : 'Portsmouth', \
                  'PR' : 'Preston', 'RG' : 'Reading', 'RH' : 'Redhill', 'RM' : 'Romford', 'S' : 'Sheffield', \
                  'SA' : 'Swansea', 'SE' : 'London SE', 'SG' : 'Stevenage', 'SK' : 'Stockport', 'SL' : 'Slough', \
                  'SM' : 'Sutton', 'SN' : 'Swindon', 'SO' : 'Southampton', 'SP' : 'Salisbury/Salisbury Plain', \
                  'SR' : 'Sunderland', 'SS' : 'Southend-on-Sea', 'ST' : 'Stoke-on-Trent', 'SW' : 'London SW', \
                  'SY' : 'Shrewsbury', 'TA' : 'Taunton', 'TD' : 'Galashiels/Tweeddale', 'TF' : 'Telford', \
                  'TN' : 'Tonbridge', 'TQ' : 'Torquay', 'TR' : 'Truro', 'TS' : 'Cleveland/Teesside', 'TW' : 'Twickenham', \
                  'UB' : 'Southall/Uxbridge', 'W' : 'London W', 'WA' : 'Warrington', 'WC' : 'London WC', 'WD' : 'Watford', \
                  'WF' : 'Wakefield', 'WN' : 'Wigan', 'WR' : 'Worcester', 'WS' : 'Walsall', 'WV' : 'Wolverhampton', \
                  'YO' : 'York', 'ZE' : 'Lerwick/Zetland'}
    
    return postcodeUKDict
############################################################################################
def clean_data(link):

    link = str(link)
    link = link.replace('[', '')
    link = link.replace(']', '')
    link = link.replace('"', '')
    link = link.replace(' ', '')
    data = link.replace('\'', '')
    

    return data
############################################################################################
def clean_postcode(data):

    data = str(data)
    data = data.replace('[', '')
    data = data.replace(']', '')
    data = data.replace("'", "")

    return data
############################################################################################
def clean_company(company):

    company = str(company)
    company = company.replace('[', '')
    company = company.replace(']', '')
    company = company.replace('  ', '')
    company = company.replace("'", "")
    company = company.replace('®', '')
    company = company.replace('&amp;', '&')
    company_name = company.replace('"', '')

    if ',' in company_name:
        company_name = company_name.split(',')[0]

    if '(' in company_name:
        company_name = company_name.split('(')[0]

    return company_name
############################################################################################
def clean_location(location):

    location = str(location)
    location = location.replace('              ', '')
    location = location.replace('[', '')
    location_name = location.replace("'", "")

    if ',' in location:
        location_name = location_name.split(',')[0]

    return location_name
############################################################################################

def clean_tags(header):

    header = header.replace('<td>', '')
    header = header.replace('<b>', '')
    header = header.replace('</td>', '')
    header_clean = header.replace('</b>', '')

    return header_clean
############################################################################################
def clean_duration(duration):

    duration = str(duration)
    duration = duration.replace(']', '')
    duration = duration.replace('[', '')
    clean_duration = duration.replace("'", "")


    return clean_duration
############################################################################################    
####################################### LOGIN FUNCTION #########################################
############################################################################################    

def Login(browser, userid, passwrd):   
    browser.implicitly_wait(10)
    browser.maximize_window()
    
    ##Site
    browser.get("https://www.linkedin.com/uas/login?")
    
    ##Login
    # userid = 'esa.ikram@yahoo.com'
    # passwrd = 'Jume!rah198'
    
        
    browser.find_element_by_id('username').send_keys(userid)
    browser.find_element_by_id('password').send_keys(passwrd)
        
    signin = browser.find_element_by_xpath("//button[contains(.,'Sign in')]")
    signin.click()
    sleep(5)
    
    
    
    
    return
############################################################################################    
############################################ NAME/LINK ################################################
############################################################################################
#finds the number of pages
def num_of_pages(browser):
    browser.execute_script("window.scrollTo(0, 1400)") 
    sleep(4)
    page_num = browser.find_elements_by_tag_name('artdeco-pagination')
    
    for i in page_num:
        itemm = browser.find_elements_by_tag_name('button')
        for i in itemm[37:38:]:
            item = i.get_attribute("outerHTML") 
            #print(item)
        
            test = re.findall(r'label=(.*?)data', item)
            num = clean_data(test)
            final_page_num = num.replace('Page', '')
            #print(test)
    
    return final_page_num
############################################################################################    
    
    ##Finds next page button id
def next_page(browser):
    browser.execute_script("window.scrollTo(0, 1400)") 
    sleep(4)
    next_page_id = browser.find_elements_by_tag_name('artdeco-pagination')
    
    for i in next_page_id:
        itemm = browser.find_elements_by_css_selector("button[class='artdeco-pagination__button artdeco-pagination__button--next artdeco-button artdeco-button--muted artdeco-button--icon-right artdeco-button--1 artdeco-button--tertiary ember-view']")
        for i in itemm:
            item = i.get_attribute("outerHTML") 
            #print(item)
        
            test = re.findall(r'id=(.*?)class', item)
            page_id = clean_data(test)
            # print(page_id)

        
    sleep(3)
    
    return page_id
############################################################################################    
  ##profession search 
def profession_loop(browser, professionList, str):
    resultsDict = dict()
    
    
    
    for iProf in professionList:
        profDict = professionRet(browser, iProf, str)
        resultsDict.update({iProf : profDict})
        print(iProf)

    cleanDict(resultsDict, 'link')

    browser.close()
    return resultsDict
############################################################################################    
def professionRet(browser, iProf, str):

    addNumber = browser.current_url
    if addNumber == 'https://www.linkedin.com/check/add-phone?country_code=gb':
        skip = browser.find_element_by_css_selector("button[class='secondary-action']")
        skip.click()

    ##profession search
    search = browser.find_element_by_css_selector("input[placeholder='Search']")
    search.send_keys(iProf)
    search.send_keys(Keys.ENTER)
    sleep(3)

    try:
        launchpad = browser.find_element_by_css_selector("button[data-control-name='launchpad.close']")
        launchpad.click()
        sleep(2)

    except NoSuchElementException:
        print('All good')


    if str == 'people':
        AllProfiles = browser.find_elements_by_css_selector("button[aria-label='View only People results']")
        if AllProfiles != []:
            for i in AllProfiles:
                i.click()
                sleep(3)

        dataDict = switch(browser, search)



    if str == 'companies':
        moreOptions = browser.find_element_by_css_selector("artdeco-dropdown[class='search-vertical-filter__dropdown ember-view']")
        moreOptions.click()
        AllCompanies = browser.find_element_by_css_selector("artdeco-dropdown-item[class='search-vertical-filter__dropdown-list-item-button t-14 t-black--light t-bold full-width search-vertical-filter__dropdown-list-item-button--COMPANIES ember-view']")
        AllCompanies.click()

        dataDict = switch(browser, search)
    
    return dataDict
############################################################################################    
def switch(browser, search):

    search.clear()
    sleep(2)
    ##profile data
    suffix = 'https://www.linkedin.com'
    
    #profile = browser.find_elements_by_css_selector("div[class='search-result__info pt3 pb4 ph0']") #This returns some stuff
    # first_page(profile, suffix)
    # num_of_pages(browser)
    page_nums = '100'
    click_id = next_page(browser)
    dataDict = link_loop(browser, click_id, page_nums, suffix)

    sleep(6)

    return dataDict
############################################################################################    
########################################### PROFILE DATA #################################################
############################################################################################
def profile_data(browser, suffix, outDict):
  

    
    #iDict = {'Name' : name, 'Link' : full_link}
    browser.execute_script("window.scrollTo(0, 800)")
    sleep(1)
    profile = browser.find_elements_by_css_selector("li[class='search-result search-result__occluded-item ember-view']") #This returns some stuff
    counter = 1

    for i in profile:

        item = i.get_attribute('innerHTML')
        #Name
        name = re.findall(r'name actor-name">(.*?)<',item)
        name = clean_data(name)
        name = re.sub(r"(?<=\w)([A-Z])", r" \1", name)
        if name == '':
            name = 'No Result'
        # iDict = {'Name' : name}
        print(name)
        
        

        
        #Link
        link = re.findall(r'href=(.*?)id=',item)
        clean_link = clean_data(link)

        if '/in/' in clean_link:
            clean_link = ",".join(clean_link.split(",")[:-1])
            full_link = suffix + clean_link
            #print(full_link)

        if ',' in clean_link:
            clean_link = clean_link.split(',')[0]
            full_link = suffix + clean_link

        iDict = {'URL' : full_link, 'Name' : name}



        outDict.update({counter : iDict})
        counter = counter + 1
        

        
    return outDict
############################################################################################    
def Age(resultsDict):

    today = int(date.today().strftime('%Y'))

    base = 21

    for iKey in resultsDict.keys():
        iJob = resultsDict[iKey]
    
        for page in iJob:
            iPage = iJob[page]


            for i in iPage:
                gradYear = iPage[i]['Graduation Year']
        

                if gradYear == 'No Result':
                    resultsDict[iKey][page][i].update({'Age' : 'No Result', 'Years In Field' : 'No Result'})
        
                else:
                    iYear = int(gradYear)
                    yearsInField = today - iYear
                    Age = base + yearsInField

                    resultsDict[iKey][page][i].update({'Age' : Age, 'Years In Field' : yearsInField})
                    # print(Age)


    return resultsDict
############################################################################################    

#loop for profile data per page
def link_loop(browser, click_id, page_nums, suffix):
    #final_page_num = num_of_pages(browser)
    #page_id = next_page(browser)
    outDict = {}
    counter = 1
    for i in range(1, (int(page_nums)+1)):
        iDict = {}
        profile_data(browser, suffix, iDict)
        sleep(1)
        next_page = browser.find_element_by_id(click_id)
        next_page.click()
        sleep(2)
        outDict.update({counter : iDict})
        counter = counter + 1

    return outDict


############################################################################################    
def location(browser, resultsDict, iKey, i, page):

    location = browser.find_element_by_css_selector("li[class='t-16 t-black t-normal inline-block']").get_attribute("innerHTML")
    location = re.findall(r'\n(.*?)\n', location)
    location_name = clean_location(location)

    resultsDict[iKey][page][i].update({'Location' : location_name})

    return resultsDict
############################################################################################    

def profileData(resultsDict, browser):

    for iKey in resultsDict.keys():
        iJob = resultsDict[iKey]

        for page in iJob:
            iPage = iJob[page]


            for i in iPage:
                iLink = iPage[i]['URL']
                # if iLink == 'https://www.linkedin.com#':
                #     del(resultsDict[iKey][page][i])

                # else:
                browser.get(iLink)
                # page = urllib.request.urlopen(iLink)
                # soup1 = BeautifulSoup(page, 'html.parser')#parse the html
    
#Attribute 1    #Location
                try:

                    location = browser.find_element_by_css_selector("li[class='t-16 t-black t-normal inline-block']").get_attribute("innerHTML")
                    location = re.findall(r'\n(.*?)\n', location)
                    location_name = clean_location(location)
        
                    resultsDict[iKey][page][i].update({'Location' : location_name})

                except NoSuchElementException:
                    resultsDict[iKey][page][i].update({'Location' : 'No Result'})
#Attribute 2    #company
                try:
                    profile = browser.find_element_by_css_selector("a[data-control-name='position_see_more']").get_attribute("outerHTML")
    
    
                    company = re.findall(r'style="-webkit-line-clamp: 2">(.*?)\n', profile)
                    company_name = clean_company(company)
                    print(company_name)
                    resultsDict[iKey][page][i].update({'company' : company_name})
    
                except NoSuchElementException:
                    print('No Result')
                    resultsDict[iKey][page][i].update({'company' : 'No Result'})


#Attribute 3    #Gathers university
                try:
                    uni = browser.find_element_by_css_selector("a[data-control-name='education_see_more']").get_attribute("outerHTML")
                    education = re.findall(r'style="-webkit-line-clamp: 2">(.*?)\n', uni)
                    education_name = clean_company(education)
        
                    resultsDict[iKey][page][i].update({'Education' : education_name})
        
        
                except NoSuchElementException:
        
                    resultsDict[iKey][page][i].update({'Education' : 'No Result'})


#Attribute 4    #Gathers graduation date
                newList = []
    
                #This bit finds the location of the attributes containing the university info on the profile and returns its position
                university = browser.find_elements_by_css_selector("div[class='pv-entity__degree-info']")
            
                for g in university:
                    education = g.find_elements_by_tag_name("h3")
                    # print(education)
                    for element in education:
                        item = element.get_attribute("innerHTML")
                        newList.append(item)
            
                check = resultsDict[iKey][page][i]['Education']
                if check in newList:
                    position = newList.index(check)
            
                else:
                    resultsDict[iKey][page][i].update({'Graduation Year' : 'No Result'})
            
            
                #Uses the position to return the correct graduation date
                timeList = []
                graduation = browser.find_elements_by_css_selector("div[class='pv-entity__summary-info pv-entity__summary-info--background-section']")
            
                for u in graduation:
                    times = u.find_elements_by_css_selector("p[class='pv-entity__dates t-14 t-black--light t-normal']")
                    for t in times:
                        # inner = t.get_attribute("innerHTML")
                        time = t.find_elements_by_tag_name("time")
                        for x in time[1:]:
                            edit = x.get_attribute("outerHTML")
                            timee = re.findall(r'<time>(.*?)</time>', edit)
                            graduation_time = clean_data(timee)
                            # print(graduation_time)
                            timeList.append(graduation_time)

                if timeList != []:
                    gradTime = timeList[position]
                    resultsDict[iKey][page][i].update({'Graduation Year' : 'No Result'})

                else:
                    resultsDict[iKey][page][i].update({'Graduation Year' : 'No Result'})


#Attribute 5        #Duration at firm
                if resultsDict[iKey][page][i]['company'] != 'No Result':
                    try:
                        result = browser.find_element_by_css_selector("section[id='experience-section']")
                        experience = result.find_element_by_css_selector("div[class='display-flex']")
                        time = experience.find_element_by_css_selector("span[class='pv-entity__bullet-item-v2']").get_attribute("outerHTML")
                        
                        duration = re.findall(r'v2">(.*?)</span', time)
                        duration = clean_duration(duration)

                        resultsDict[iKey][page][i].update({'Duration' : duration})

                    except NoSuchElementException:

                        resultsDict[iKey][page][i].update({'Duration' : 'No Result'})

                else:
                    resultsDict[iKey][page][i].update({'Duration' : 'No Result'})
#Attribute 6    #Age
    Age(resultsDict)

    return resultsDict
############################################################################################    

def companyData(resultsDict, browser):

    for iKey in resultsDict.keys():
        iJob = resultsDict[iKey]

        for page in iJob:
            iPage = iJob[page]


            for i in iPage:
                iLink = iPage[i]['URL']
                print(iLink)
                try:
                    browser.get(iLink)
    
                    #Company name
                    try:
                        profile = browser.find_element_by_css_selector("span[dir='ltr']").get_attribute("outerHTML") #This returns some stuff
                        name = re.findall(r'<span dir="ltr">(.*?)</span>', profile)
                        compName = clean_company(name)
                        print(compName)
        
                        resultsDict[iKey][page][i].update({'company' : compName})
    
                    except NoSuchElementException:
                        print('No Result')
                        resultsDict[iKey][page][i].update({'company' : 'No Result'})
    
                    #business link
                    try:
                        company = browser.find_element_by_css_selector("div[class='org-top-card-primary-actions__inner']").get_attribute("outerHTML")
                        link = re.findall(r'href=(.*?)id=', company)
                        link = clean_data(link)
        
                        resultsDict[iKey][page][i].update({'business url' : link})
    
                    except NoSuchElementException:
                        print('No Result')
                        resultsDict[iKey][page][i].update({'business url' : 'No Result'})
    
                    #location
                    try:
                        location = browser.find_element_by_css_selector("div[class='org-top-card-summary__info-item org-top-card-summary__headquarter']").get_attribute('innerHTML')
                        loc = clean_duration(location)
                        location = loc.replace('\n', '')
        
                        resultsDict[iKey][page][i].update({'location' : location})
    
                    except NoSuchElementException:
                        print('No Result')
                        resultsDict[iKey][page][i].update({'location' : 'No Result'})








                except InvalidArgumentException:
                    resultsDict[iKey][page][i].update({'company' : 'No Result', \
                               'business url' : 'No Result', 'location' : 'No Result'})


    return resultsDict
############################################################################################    






############################################################################################    
def resultData(resultsDict, browser, str):

    if str == 'people':
        profileData(resultsDict, browser)

    if str == 'companies':
        companyData(resultsDict, browser)
        # companyHouse(resultsDict, browser)

    return resultsDict
############################################################################################    
######################################### PLACENAME ALGORITHM ###################################################
############################################################################################    
def placeSearch(resultsDict, browser):

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:
                iLoc = iPage[i]['location']

                iSearch1 = iLoc + ' postcode'
                iSearch2 = iLoc

                searchList = [iSearch1, iSearch2]

                for iSearch in searchList:
                    contCond2(iSearch, browser, resultsDict, iKey, page, i)
                    if resultsDict[iKey][page][i]['area'] != 'no result':
                        break


    return resultsDict
############################################################################################
def contCond2(iSearch, browser, resultsDict, iKey, page, i):

    Search(iSearch, browser)
    sleep(2)
    
    try:
        result = browser.find_elements_by_xpath('/html/body/div[7]/div[3]/div[7]/div[1]/div/div/div/div/div/div[2]/div/g-scrolling-carousel/div[1]/div/div[1]/div/div[1]/a/div[2]/div/div/div')
#        print(result)
        for g in result[0:1]:
            item = g.get_attribute('innerHTML')
            if item[0].isdigit():
                item = 'no result'
            print(item)
            # print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAa')
            

        if result == []:
            try:
                placeVariation2(iSearch, browser, resultsDict, iKey, page, i)
                
            except NoSuchElementException:
                resultsDict[iKey][page][i].update({'area' : 'no result'})
            
        
        else:
            resultsDict[iKey][page][i].update({'area' : item})

    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})


    return resultsDict
############################################################################################
def placeVariation2(iSearch, browser, resultsDict, iKey, page, i):
    
#    browser.execute_script("window.scrollTo(0, 400)")
#    sleep(2)
    
    try: 
        result = browser.find_elements_by_css_selector("div[class='Z0LcW AZCkJd']")
        for k in result:
            item = k.get_attribute('innerHTML')
            if item[0].isalpha():
                print(item)
                # print('BBBBBBBBBBBBBBBBBBBBBBBBB')
            
            else:
                item = 'no result'
        
        if result == []:
            try:
                placeVariation3(iSearch, browser, resultsDict, iKey, page, i)
                
            except NoSuchElementException:
                resultsDict[iKey][page][i].update({'area' : 'no result'})
            
        
        else:
            resultsDict[iKey][page][i].update({'area' : item})
    
    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})


    return resultsDict
############################################################################################
def placeVariation3(iSearch, browser, resultsDict, iKey, page, i):
    
#    newSearch = iSearch
    try: 
        result = browser.find_elements_by_css_selector("div[data-attrid='subtitle']")
        for j in result:
            item = j.get_attribute('innerHTML')
            town = re.findall(r'AI">(.*?)</span>', item)
            clean_town = clean_postcode(town)
            print(clean_town)
            # print('CCCCCCCCCCCCCCCCCCCCCC')

            
            #Want data to be like this 'UK_postcodeChange'
        if result == []:
            try:
                placeVariation4(iSearch, browser, resultsDict, iKey, page, i)

            except NoSuchElementException:
                #'No Result'
                resultsDict[iKey][page][i].update({'area' : 'no result'})
        
        else:
            resultsDict[iKey][page][i].update({'area' : clean_town})
    
    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})
    
    return resultsDict
############################################################################################
def placeVariation4(iSearch, browser, resultsDict, iKey, page, i):

    browser.execute_script("window.scrollTo(0, 200)")
    sleep(2)
    try: 
        result = browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/div[1]/div/div[1]/div/div[2]/table/tbody/tr[2]/td[1]')

        for j in result:
            item = j.get_attribute("innerHTML")
            print(item)
            
            #Want data to be like this 'UK_postcodeChange'
        if result == []:
            # try:
                # placeVariation5
            # except NoSuchElementException:
                #'No Result'
                resultsDict[iKey][page][i].update({'area' : 'no result'})
        
        else:
            resultsDict[iKey][page][i].update({'area' : item})
    
    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})
    
    return resultsDict
############################################################################################
def convert(resultsDict, UKPostcodeDict):
    
    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:
                change = resultsDict[iKey][page][i]['area']
        #        revert = areaDict[iKey]['location']
                
                for aKey in UKPostcodeDict.keys():
        #            print(UKPostcodeDict[aKey])
                    
                    if change.startswith(aKey):
                        resultsDict[iKey][page][i].update({'area' : UKPostcodeDict[aKey]})

    
    return resultsDict
############################################################################################
def tagging(resultsDict, UKPostcodeDict):

    boroughList = []

    for aKey in UKPostcodeDict.keys():
        borough = UKPostcodeDict[aKey]
        boroughList.append(borough)

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:

                area = resultsDict[iKey][page][i]['area']
                #loc = resultsDict[iKey][page][i]['location']


                if area in boroughList:
        #            print('Match')
                    resultsDict[iKey][page][i].update({'country' : 'UK'})

                if area == 'English non-metropolitan county':
                    resultsDict[iKey][page][i].update({'country' : 'UK'})

                if area == 'English metropolitan country':
                    resultsDict[iKey][page][i].update({'country' : 'UK'})


                if area == 'Shire county':
                    resultsDict[iKey][page][i].update({'country' : 'UK'})

                if area == 'London':
                    resultsDict[iKey][page][i].update({'country' : 'UK'})

                if area not in boroughList:
                    resultsDict[iKey][page][i].update({'country' : 'INT'})

                if area == 'no result':
        #            print('No Match')
                    resultsDict[iKey][page][i].update({'country' : 'INT'})
                
                if area == '':
                    resultsDict[iKey][page][i].update({'country' : 'INT'})
                
                               
                if area.startswith('Country in'):
                    resultsDict[iKey][page][i].update({'country' : 'INT'})
                
                if area.startswith('Island in'):
                    resultsDict[iKey][page][i].update({'country' : 'INT'})
                
                if area.startswith('Capital of'):
                    resultsDict[iKey][page][i].update({'country' : 'INT'})

    return resultsDict
############################################################################################
def conversion(resultsDict, UKPostcodeDict):

    convert(resultsDict, UKPostcodeDict)
    tagging(resultsDict, UKPostcodeDict)
    cleanDict(resultsDict, 'placename')

    return resultsDict
############################################################################################
#Further filtration on no result locations
def retry(resultsDict, browser):

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]
    
        for page in iData:
            iPage = iData[page]
    
            for i in iPage:
                iLoc = iPage[i]['location']
                iComp = iPage[i]['company']
    
                if iLoc == 'No Result':
    
                    iSearch1 = iComp
                    iSearch2 = iComp + ' location'

                    searchList = [iSearch1, iSearch2]
        
                    for iSearch in searchList:
                        contCond4(iSearch, browser, resultsDict, iKey, page, i)
                        if resultsDict[iKey][page][i]['area'] != 'no result':
                            break

    return resultsDict
############################################################################################
def contCond4(iSearch, browser, resultsDict, iKey, page, i):

    Search(iSearch, browser)
    browser.execute_script("window.scrollTo(0, 200)")
    sleep(2)
    
    try:
        result = browser.find_elements_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[2]/div/div[2]/div/div')
# result = browser.find_elements_by_xpath("//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[2]/div/div[4]/div")
        for j in result:
            item = j.get_attribute("innerHTML")
            address = re.findall(r'"LrzXr">(.*?)</span>', item)
            # address = str(address)
            address = clean_postcode(address)
            address_split = address.split()
            if address_split != []:

                address_final = address_split[-2:]
                postcode = address_final[0]
                print(postcode)

            else:
                postcode = 'no result'

        if result == []:
            try:
                retryVariation2(iSearch, browser, resultsDict, iKey, page, i)
                
            except NoSuchElementException:
                resultsDict[iKey][page][i].update({'area' : 'no result'})
            
        
        else:
            resultsDict[iKey][page][i].update({'area' : postcode})

    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})

    return resultsDict
############################################################################################
def retryVariation2(iSearch, browser, resultsDict, iKey, page, i):

    try:
        result = browser.find_elements_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[2]/div/div[3]')
# result = browser.find_elements_by_xpath("//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[2]/div/div[4]/div")
        for j in result:
            item = j.get_attribute("innerHTML")
            address = re.findall(r'"LrzXr">(.*?)</span>', item)
            # address = str(address)
            address = clean_postcode(address)
            address_split = address.split()

            if address_split != []:
                address_final = address_split[-2:]
                postcode = address_final[0]
                print(postcode)

            else:
                postcode = 'no result'

        if result == []:
            # try:
                # retryVariation3(iSearch, browser, resultsDict, iKey, page, i)
                
            # except NoSuchElementException:
            resultsDict[iKey][page][i].update({'area' : 'no result'})
            
        
        else:
            resultsDict[iKey][page][i].update({'area' : postcode})

    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})

    return resultsDict
############################################################################################
def retryVariation3(iSearch, browser, resultsDict, iKey, page, i):

    try:
        result = browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/div[1]/div/div/div/div/div')
# result = browser.find_elements_by_xpath("//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[2]/div/div[4]/div")
        for j in result:
            item = j.get_attribute("innerHTML")
            address = re.findall(r'"Z0LcW">(.*?)</div>', item)
            # address = str(address)
            address = clean_postcode(address)
            address_split = address.split()
            address_final = address_split[-2:]
            postcode = address_final[0]
            print(postcode)

        if result == []:
            #try:
                #variation4
            #except
                #'No Result'
            resultsDict[iKey][page][i].update({'area' : 'no result'})
        
        else:
            resultsDict[iKey][page][i].update({'area' : postcode})

    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'area' : 'no result'})

    return resultsDict
############################################################################################
########################################### NUMBER SEARCH #################################################
############################################################################################
def Search(iSearch, browser):
    browser.get('https://www.google.com')

    search = browser.find_element_by_css_selector("input[aria-label='Search']")

    try:
        search.send_keys(iSearch)
        search.send_keys(Keys.ENTER)
    
    except StaleElementReferenceException:
        print('')

    return
############################################################################################    
def Variation4(browser, resultsDict, iKey, page, i):

    sleep(2)

    result = browser.find_elements_by_xpath('//*[@id="rso"]/div[1]/div/div[1]/div/div[1]/div/div/div/div/div')
    # result = browser.find_elements_by_xpath("//*[@id='rhs_block']/div/div[1]/div/div[1]/div[2]/div[2]/div/div[4]/div")
    for j in result:
        item = j.get_attribute("innerHTML")
        number = re.findall(r'<span>(.*?)</span>', item)
        number = clean_data(number)
        print(number)

    if result == []:
        #ADD NEXT VARIATION IN HERE
        resultsDict[iKey][page][i].update({'Contact' : 'No Result'})


    else:
        resultsDict[iKey][page][i].update({'Contact' : number})



    return resultsDict
############################################################################################    
def Variation3(browser, resultsDict, iKey, page, i, iComp):


    # browser.execute_script("window.scrollTo(0, 200)")
    sleep(2)

    result = browser.find_elements_by_css_selector("span[class='rllt__details lqhpac']")


    numList = []
    for res in result:
        item = res.find_elements_by_tag_name("div")
        for j in item:
            final = j.get_attribute("outerHTML")
            final_num = re.findall(r'</span>(.*?)</div>', final)
            final_num = clean_data(final_num)
            final_num = final_num.replace('·', '')
            numList.append(final_num)


    name = browser.find_elements_by_css_selector("div[class='dbg0pd']")
    nameList = []
    for res in name:
        name = res.find_element_by_tag_name("span").get_attribute("outerHTML")
        name = re.findall(r'<span>(.*?)</span>', name)
        name = str(name)
        name = name.replace('[', '')
        name = name.replace(']','')
        name = name.replace("'", "")
        nameList.append(name)


    if result == []:
        try:
            Variation4(browser, resultsDict, iKey, page, i)


        except NoSuchElementException:
            resultsDict[iKey][page][i].update({'Contact' : 'No Result'})



    else:

        for g in nameList:
            if iComp in g:

                approved = ['+', '0']
                appList = []
                
                for app in approved:
                    matching = [n for n in numList if n.startswith(app)]
                    for match in matching:
                        appList.append(match)
                
                length = len(appList)
                if length > 1:
                    xMatch = appList[0]
        
                else:
                    resultsDict[iKey][page][i].update({'Contact' : 'No Result'})
        
        
                
                count = 0
                for num in appList[1:]:
                    if xMatch in appList:
                        count = count + 1
        
                if count > 0:
                    print(xMatch)
                    resultsDict[iKey][page][i].update({'Contact' : xMatch})

                else:
                    resultsDict[iKey][page][i].update({'Contact' : 'No Result'})

            else:
                resultsDict[iKey][page][i].update({'Contact' : 'No Result'})


    return resultsDict
############################################################################################
def Variation2(browser, resultsDict, iKey, page, i, iComp):

    browser.execute_script("window.scrollTo(0, 400)")
    sleep(2)

    
    result = browser.find_elements_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[2]/div/div[4]/div/div')

    for j in result:
        item = browser.find_element_by_css_selector("span[class='LrzXr zdqRlf kno-fv']").get_attribute("innerHTML")
        number = re.findall(r'<span>(.*?)</span>', item)
        number = clean_data(number)

    if result == []:
    ##[
        try:
            Variation3(browser, resultsDict, iKey, page, i, iComp)

        except NoSuchElementException:
            resultsDict[iKey][page][i].update({'Contact' : 'No Result'})
    ##]


    else:
        resultsDict[iKey][page][i].update({'Contact' : number})

    return resultsDict
############################################################################################    
def ContCond(iSearch2, browser, resultsDict, iKey, page, i, iComp):

    Search(iSearch2, browser)

    browser.execute_script("window.scrollTo(0, 100)")
    sleep(2)
    try:

        result = browser.find_elements_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[2]/div/div[3]/div/div/span[2]')

        for j in result:
    
            item = browser.find_element_by_css_selector("span[class='LrzXr zdqRlf kno-fv']").get_attribute("innerHTML")
            number = re.findall(r'<span>(.*?)</span>', item)
            number = clean_data(number)

        if result == []:
        ##[
            try:
                Variation2(browser, resultsDict, iKey, page, i, iComp)
    
            except NoSuchElementException:
                resultsDict[iKey][page][i].update({'Contact' : 'No Result'})
        ##]
        else:
            resultsDict[iKey][page][i].update({'Contact' : number})

    except NoSuchElementException:
        resultsDict[iKey][page][i].update({'Contact' : 'No Result'})

    return resultsDict

############################################################################################    
def contact_num(resultsDict, browser, str):

    # browser = webdriver.Safari()
    browser.maximize_window()

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:

                iComp = iPage[i]['company']

                if str != 'companies':
                    iLoc = iPage[i]['Location']

                if str == 'companies':
                    iLoc = iPage[i]['area']

                if iComp != 'No Result':
                    iSearch1 = iComp + ' ' + iLoc + ' office contact number'
                    iSearch2 = iComp + ' ' + iLoc + ' office contact'
                    iSearch3 = iComp + ' ' + iLoc + ' office'
                    iSearch4 = iComp + ' ' + iLoc
                    iSearch5 = iComp + ' HQ ' + iLoc
                    iSearch6 = iComp + ' ' + iLoc + ' office contact details'

                    SearchList = [iSearch1, iSearch2, iSearch3, iSearch4, iSearch5, \
                                  iSearch6]
                
                    for k in SearchList:
                        ContCond(k, browser, resultsDict, iKey, page, i, iComp)
                        if resultsDict[iKey][page][i]['Contact'] != 'No Result':
                            break
                
                    print(resultsDict[iKey][page][i]['Contact'])

                else:
                    resultsDict[iKey][page][i].update({'Contact' : 'No Result'})
                    print(resultsDict[iKey][page][i]['Contact'])

    return resultsDict
############################################################################################
########################################## COMPANY NAME CLARIFICATION ##################################################
############################################################################################    
def nameClarify(resultsDict, browser):

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:
                iComp = iPage[i]['company']

                if iComp!= 'No Result':
                    iSearch1 = iComp

                    SearchList = [iSearch1]

                    for k in SearchList:
                        ContCond3(k, browser, resultsDict, iKey, page, i)
                        if resultsDict[iKey][page][i]['company'] != 'No Result':
                            break
    return resultsDict
############################################################################################
def ContCond3(k, browser, resultsDict, iKey, page, i):

    Search(k, browser)
    browser.execute_script("window.scrollTo(0, 400)")
    sleep(2)

    try:
        result = browser.find_elements_by_xpath('//*[@id="rhs"]/div/div[1]/div/div[1]/div/div[1]/div[2]/div[2]/div[1]/div/div/div[1]')

        for f in result:
            item = f.get_attribute('outerHTML')
            newName = re.findall(r'<span>(.*?)</span>', item)
            name = clean_company(newName)

            resultsDict[iKey][page][i].update({'company' : name})

        if result == []:
            print('')

    except NoSuchElementException:
        print('')

    return resultsDict
############################################################################################
########################################## RESULT CLEANING ##################################################
############################################################################################    
#This function finds all elements in dictionary where link is dud
def findElem(resultsDict, str):


    remElemDict = dict()
    # subDict = dict()
    counter = 1

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:

                if str == 'link':
                    iLink = iPage[i]['URL']
    
                    if iLink == 'https://www.linkedin.com#':
                        # print(iKey, page, i)
    
                        subDict = ({'profession' : iKey, 'page' : page, 'element' : i})
                        remElemDict.update({counter : subDict})
    
                        counter = counter + 1

                if str == 'placename':
                    iPlace = iPage[i]['country']

                    if iPlace != 'UK':

                        subDict = ({'profession' : iKey, 'page' : page, 'element' : i})
                        remElemDict.update({counter : subDict})

                        counter = counter + 1


    return remElemDict
############################################################################################
#This function removes dud elements from resultsDict
def remElem(resultsDict, locDict):

    for elem in locDict.keys():
        item = locDict[elem]

        page = item['page']
        element = item['element']
        iKey = item['profession']

        del(resultsDict[iKey][page][element])

    return resultsDict
############################################################################################
#Puts find and rem functions into one
def cleanDict(resultsDict, str):

    locDict = findElem(resultsDict, str)
    cleanDict = remElem(resultsDict, locDict)


    return cleanDict
############################################################################################    
############################################ QUERYING/OUTPUT ################################################
############################################################################################
def insertQuery(resultsDict):

    for iKey in resultsDict.keys():
        iData = resultsDict[iKey]

        for page in iData:
            iPage = iData[page]

            for i in iPage:
                iName = iPage[i]['Name']
                iLink = iPage[i]['URL']
                iAge = iPage[i]['Age']
                iAge = str(iAge)
                iDuration = iPage[i]['Duration']
                iLocation = iPage[i]['Location']
                iCompany = iPage[i]['company']
                iContact = iPage[i]['Contact']

                query = "INSERT INTO `Sys`.`profile_data`(`link`, `Name`, `Age`, `Duration`, `Contact`, `Location`, `Company`, `Profession`)VALUES" + \
                '(' + '"' + iLink + '"' + ',' + '"' + iName + '"' + ',' + '"' + iAge+ '"' + ',' + '"' + iDuration + '"' + ',' + '"' + iContact + '"' + ',' + \
                '"' + iLocation + '"' + ',' + '"' + iCompany + '"' + ',' + '"' + iKey + '"' + ')' + ';'

                # print(query)
                connection(query, 'in')



    return
############################################################################################
def connection(query, str):

    try:
        connection = mc.connect(host = "127.0.0.1",
                                user = "root",
                                passwd = "Jumeirah198",
                                db = "Sys")
    
    except mc.Error as e:
        print("Error %d: %s" % (e.args[0], e.args[1]))
        mc.exit(1)


    cursor = connection.cursor(buffered=True)

    if str == 'in':
        try:
            cursor.execute(query)
            connection.commit()
    
        except mc.IntegrityError:
            print('Already in Database')

    if str == 'out':
        try:
            cursor.execute(query)
            connection.commit()
            data = cursor.fetchall()

            # print("it works")
            spreadsheet(data)

        except mc.Error as e:
            print("Error", e)


    cursor.close()
    connection.close()


    return
############################################################################################
def spreadsheet(data):
    workbook = xlsxwriter.Workbook('linkedin_company_output1.xlsx')
    worksheet = workbook.add_worksheet()
    
    excel_row = 0
    excel_col = 0
    
    bold = workbook.add_format({'bold' : True, 'bottom' : 2 })
    width1 = len("len(longest profession)")
    width2 = len("I wonder how long a name we could have")
    width3 = len(" Age ")
    width4 = len("London, England")
    width5 = len("15 yrs 14 mos")
    width6 = len("The longest company name you could possibly think of goes here")
    width7 = len(" +447807055187 ")
    
    
    #NAME
    worksheet.write(0, 1, "Profession", bold)
    worksheet.set_column(0, 2, width1)
    
    worksheet.write(0, 2, "Name", bold)
    worksheet.set_column(0, 2, width2)
    
    worksheet.write(0, 3, "Age", bold)
    worksheet.set_column(0, 2, width3)
    
    worksheet.write(0, 4, "Location", bold)
    worksheet.set_column(0, 2, width4)
    
    worksheet.write(0, 5, "Company", bold)
    worksheet.set_column(0, 2, width6)
    
    worksheet.write(0, 6, "Duration at firm", bold)
    worksheet.set_column(0, 2, width5)
    
    worksheet.write(0, 7, "Contact", bold)
    worksheet.set_column(0, 2, width7)


    populateSpreadsheet(data, worksheet, excel_row, excel_col)


    workbook.close()

    return
############################################################################################
def populateSpreadsheet(data, worksheet, excel_row, excel_col):

    for row in data:
        profession = row[7]
        name = row[1]
        age = row[2]
        location = row[4]
        company = row[6]
        duration = row[3]
        contact = row[5]



        if contact != 'No Result':
            worksheet.write(excel_row+1, excel_col+1, profession)
            worksheet.write(excel_row+1, excel_col+2, name)
            worksheet.write(excel_row+1, excel_col+3, age)
            worksheet.write(excel_row+1, excel_col+4, location)
            worksheet.write(excel_row+1, excel_col+5, company)
            worksheet.write(excel_row+1, excel_col+6, duration)
            worksheet.write(excel_row+1, excel_col+7, contact)
            excel_row += 1


    return
############################################################################################
def output():

    select_query = "SELECT * FROM `Sys`.`profile_data`"

    connection(select_query, 'out')

    return

############################################################################################
def main():

    #individual profiles
    professionList = ['independent financial advisers']
    userid = 'esa.ikram@yahoo.com'
    passwrd = 'Jume!rah198'
    browser = webdriver.Safari()
    Login(browser, userid, passwrd)
    resultsDict = profession_loop(browser, professionList, 'companies')

    # clean_dict = cleanDict(resultsDict)

    #profile data
    try:
        browser = webdriver.Safari()
        Login(browser, userid, passwrd)
        resultData(resultsDict, browser, 'companies')
        # profileData(resultsDict, browser)

    except WebDriverException:
        browser.close()
        browser = webdriver.Safari()
        Login(browser, userid, passwrd)
        resultData(resultsDict, browser, 'companies')
        # profileData(testDict, browser)
        browser.close()

#variation 1, 2 dont work
#note Freelance may not be a company

#placenames - UK based - for companies only
    UKPostcodeDict = postcodeDict()
    chromedriver = r"/Users/Student/Desktop/side_projects/LinkedIn/chromedriver"
    browser = webdriver.Chrome(chromedriver)
    placeSearch(resultsDict, browser)
    browser.close()

#Change the postcode bit to test, and take the last two
    browser = webdriver.Safari()
    retry(resultsDict, browser)
    browser.close()

    browser = webdriver.Safari()
    browser.maximize_window()
    nameClarify(resultsDict, browser)
    browser.close()

    conversion(resultsDict, UKPostcodeDict)


#######
    browser = webdriver.Safari()
    contact_num(resultsDict, browser, 'companies')
    browser.close()

    insertQuery(resultsDict)
    output()

    return


https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&geoIncluded=102257491&industryIncluded=43&logHistory=true&rsLogId=1198651481&searchSessionId=XmArMbFdTS2MGtbGcJrNZQ%3D%3D&tenureAtCurrentCompany=3&tenureAtCurrentPosition=2%2C3&titleExcluded=assistant%2Cexecutive%2520assistant%2Cwealth%2520management&titleIncluded=Head%2520of&titleTimeScope=CURRENT&yearsOfExperience=5

