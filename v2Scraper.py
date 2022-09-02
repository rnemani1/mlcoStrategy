from selenium import webdriver
import time
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import datetime
import threading
import curses

import v2FirestoreManager

from datetime import date

def runA(URL):
    
    driver = None
    dPath = '/Users/rnemani/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Keep/Developer/chromedriver'

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=dPath, options=options)

    try:
        driver.get(URL)
    except:
        time.sleep(1)
        driver.get(URL)

    while True:
        try:

            t1Score_old = '00'
            t2Score_old = '00'
            t1Spread_old = '+0.0'
            t2Spread_old = '+0.0'
            t1mLine_old = '+000'
            t2mLine_old = '+000'

            league = get_league(URL)

            try:    
                t1mLine = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[3]/span').text
                t2mLine = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[6]/span').text
            except NoSuchElementException:
                t1mLine = t1mLine_old
                t2mLine = t2mLine_old
            
            #trigger: new mLine
            if t1mLine_old != t1mLine or t2mLine_old != t2mLine:

                teams = get_teams_mLine(URL, t1mLine, t2mLine)

                v2FirestoreManager.out(league, teams[0], teams[1], teams[2], teams[3])

                t1mLine_old = t1mLine
                t2mLine_old = t2mLine
  
            try:
                t1Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[1]/span').text
                t2Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[2]/span').text
            except NoSuchElementException:
                t1Score = t1Score_old
                t2Score = t2Score_old

            #trigger: new score
            if t1Score_old != t1Score or t2Score_old != t2Score:

                teams = get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine)

                v2FirestoreManager.in_(league, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5])

                t1Score_old = t1Score
                t2Score_old = t2Score

            try: 
                t1Spread = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[2]/span').text
                t2Spread = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[5]/span').text
            except NoSuchElementException:
                t1Spread = t1Spread_old
                t2Spread = t2Spread_old

            #trigger: new spread
            if t1Spread_old != t1Spread or t2Spread_old != t2Spread:

                teams = get_teams(URL, t1Spread, t2Spread)

                v2FirestoreManager.open(league, teams[0], teams[1], teams[2])

                t1Spread_old = t1Spread
                t2Spread_old = t2Spread

        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

def runB(URL):
    
    driver = None
    dPath = '/Users/rnemani/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Keep/Developer/chromedriver'

    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=dPath, options=options)

    try:
        driver.get(URL)
    except:
        time.sleep(1)
        driver.get(URL)

    while True:
        try:

            t1Score_old = '00'
            t2Score_old = '00'
            t1Spread_old = '+0.0'
            t2Spread_old = '+0.0'
            t1mLine_old = '+000'
            t2mLine_old = '+000'

            league = get_league(URL)

            try:    
                t1mLine = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[2]/span').text
                t2mLine = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[5]/span').text
            except NoSuchElementException:
                t1mLine = t1mLine_old
                t2mLine = t2mLine_old
            
            #trigger: new mLine
            if t1mLine_old != t1mLine or t2mLine_old != t2mLine:

                teams = get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine)

                v2FirestoreManager.out(league, teams[0], teams[1], teams[2], teams[3])

                t1Score_old = t1Score
                t2Score_old = t2Score
  
            try:
                t1Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[1]/span').text
                t2Score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[2]/span').text
            except NoSuchElementException:
                t1Score = t1Score_old
                t2Score = t2Score_old

            #trigger: new score
            if t1Score_old != t1Score or t2Score_old != t2Score:

                teams = get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine)

                v2FirestoreManager.in_(league, teams[0], teams[1], teams[2], teams[3], teams[4], teams[5])

                t1Score_old = t1Score
                t2Score_old = t2Score

            try: 
                t1Spread = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[1]/span').text
                t2Spread = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[4]/span').text
            except NoSuchElementException:
                t1Spread = t1Spread_old
                t2Spread = t2Spread_old

            #trigger: new spread
            if t1Spread_old != t1Spread or t2Spread_old != t2Spread:

                teams = get_teams(URL, t1Spread, t2Spread)

                v2FirestoreManager.open(league, teams[0], teams[1], teams[2])

                t1Spread_old = t1Spread
                t2Spread_old = t2Spread

        except NoSuchElementException:
            pass
        except StaleElementReferenceException:
            pass

def get_league(URL):
    return(URL.split("/", 10)[4])

def get_teams(URL, t1Spread, t2Spread):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1Spread:
        uTeam = team1
        fTeam = team2
        fSpread = float(t2Spread[1:])
    else:
        uTeam = team2
        fTeam = team1
        fSpread = float(t1Spread[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(fSpread)

    return(teams)

def get_teams_spread(URL, t1Spread, t2Spread):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1Spread:
        uTeam = team1
        fTeam = team2
        fSpread = float(t2Spread[1:])
    else:
        uTeam = team2
        fTeam = team1
        fSpread = float(t1Spread[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(fSpread)

    return(teams)

def get_teams_score(URL, t1Score, t2Score, t1mLine, t2mLine):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1mLine:
        uTeam = team1
        fTeam = team2
        uScore = t1Score
        fScore = t2Score
        fmLine = float(t2mLine[1:])
        umLine = float(t1mLine[1:])
    else:
        uTeam = team2
        fTeam = team1
        uScore = t2Score
        fScore = t1Score
        fmLine = float(t1mLine[1:])
        umLine = float(t2mLine[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(uScore)
    teams.append(fScore)
    teams.append(umLine)
    teams.append(fmLine)

    return(teams)

def get_teams_mLine(URL, t1mLine, t2mLine):
    
    tUnformated = URL.split("/", 10)[-1]
    team1 = tUnformated.split("@", 3)[0]
    team2 = tUnformated.split("@", 3)[1]
    t1Unformated = team1.split("-", 30)
    t2Unformated = team2.split("-", 30)
    del(t2Unformated[-1])
    
    team2 = ""
    for i in t2Unformated:
        team2 += i + " "

    team1 = ""
    for j in t1Unformated:
        team1 += j + " "

    if '+' in t1mLine:
        uTeam = team1
        fTeam = team2
        fmLine = float(t2mLine[1:])
        umLine = float(t1mLine[1:])
    else:
        uTeam = team2
        fTeam = team1
        fmLine = float(t1mLine[1:])
        umLine = float(t2mLine[1:])

    teams = []

    teams.append(uTeam.strip(' '))
    teams.append(fTeam.strip(' '))
    teams.append(umLine)
    teams.append(fmLine)

    return(teams)

