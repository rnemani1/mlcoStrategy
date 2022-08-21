from selenium import webdriver
import time
from time import sleep
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import datetime
import threading
import curses

import firestoreManager

from datetime import date

def wait_for_q(stdscr):
    curses.cbreak()
    stdscr.keypad(1)
    curses.noecho()

    stdscr.addstr(13,0,"Hit 'q' to quit")
    stdscr.refresh()

    key = ''
    while key != ord('q'):
        key = stdscr.getch()

    curses.endwin()

def time(stdscr):
    while True:
        # datetime object containing current date and time
        now = datetime.datetime.now()

        stdscr.addstr(0, 0, now.strftime("%m/%d/%Y %H:%M:%S"))
        stdscr.refresh()

        sleep(1)
    
def get_league(URL):
    return(URL.split("/", 10)[4])

def get_team(URL):
    unformated_team = URL.split("/", 10)[-1]

    seperate_team_1 = unformated_team.split("@", 3)[0]
    seperate_team_2 = unformated_team.split("@", 3)[1]

    unformated_team_2 = seperate_team_2.split("-", 30)
    unformated_team_1 = seperate_team_1.split("-", 30)

    del(unformated_team_2[-1])
    
    team_2 = ""
    for i in unformated_team_2:
        team_2 += i + " "

    team_1 = ""
    for e in unformated_team_1:
        team_1 += e + " "


    teams = []


    teams.append(team_1.strip(' '))
    teams.append(team_2.strip(' '))

    return(teams)

def run(URL, stdscr): 
    #initialzes variables
    driver = None

    #sets chrome driver
    DRIVER_PATH = '/Users/rnemani/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Keep/Developer/chromedriver'

    #adds chrome options
    options = webdriver.ChromeOptions()

    options.headless = True

    #disables warnings cause they mad anoying
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    #sets driver
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    try:
        #opens web page
        driver.get(URL)
    except:
        time.sleep(1)
        #opens web page
        driver.get(URL)

    old_team_1_score = ""
    old_team_2_score = ""
    old_spread_team_1= ""
    old_spread_team_2= ""
    old_money_team_1= ""
    old_money_team_2= ""

    #Comment these two lines to debug
    #processThread = threading.Thread(target=time, args=(stdscr,))  # <- note extra ','
    #processThread.start()

    while True:
        try:
            try:
                team_1_score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[1]/span').text
                team_2_score = driver.find_element('xpath', '(//div[starts-with(@aria-label, "current score")])[2]/span').text
            except NoSuchElementException:
                team_1_score = "00"
                team_2_score = "00"
            
            spread_team_1 = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[1]/span').text
            spread_team_2 = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[4]/span').text

            money_team_1 = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[2]/span').text 
            money_team_2 = driver.find_element('xpath', '(//div[@role="button" and (span or *[name()="svg"])])[5]/span').text

            teams = get_team(URL)

            team_1 = teams[0]
            team_2 = teams[1]

            if '+' in spread_team_1:
                underdog_spread = spread_team_1
                underdog_spread_team = team_1

                favorite_spread = spread_team_2
                favorite_spread_team = team_2
            else:
                underdog_spread = spread_team_2
                underdog_spread_team = team_2

                favorite_spread = spread_team_1
                favorite_spread_team = team_1

            if '+' in money_team_1:
                underdog = team_1
                underdog_score = team_1_score
                underdog_money = money_team_1
                underdog_money_team = team_1

                favorite = team_2
                favorite_score = team_2_score
                favorite_money = money_team_2
                favorite_money_team = team_2
            else:
                underdog = team_2
                underdog_score = team_2_score
                underdog_money = money_team_2
                underdog_money_team = team_2

                favorite = team_1
                favorite_score = team_1_score
                favorite_money = money_team_1
                favorite_money_team = team_1


            if old_team_1_score != team_1_score or old_team_2_score != team_2_score or old_spread_team_1 != spread_team_1 or old_spread_team_2 != spread_team_2 or old_money_team_1 != money_team_1 or old_money_team_2 != money_team_2:
                
                """
                if old_team_1_score != team_1_score:
                    changed = f"{team_1}'s score | {old_team_1_score} -> {team_1_score}"
                elif old_team_2_score != team_2_score:
                    changed = f"{team_2}'s score | {old_team_2_score} -> {team_2_score}"
                elif old_spread_team_1 != spread_team_1:
                    changed = f"{team_1}'s spread | {old_spread_team_1} -> {spread_team_1}"
                elif old_spread_team_2 != spread_team_2:
                    changed = f"{team_2}'s spread | {old_spread_team_2} -> {spread_team_2}"
                elif old_money_team_1 != money_team_1:
                    changed = f"{team_1}'s money | {old_money_team_1} -> {money_team_1}"
                elif old_money_team_2 != money_team_2:
                    changed = f"{team_2}'s money | {old_money_team_2} -> {money_team_2}"
                """

                if old_money_team_1 != money_team_1 or old_money_team_2 != money_team_2:
                    #out(uTeam, umLine, fmLine)
                    firestoreManager.out(underdog, underdog_money, favorite_money)
                    changed = f"{team_1}'s money | {old_money_team_1} -> {money_team_1}"

                if old_team_1_score != team_1_score or old_team_2_score != team_2_score:
                    #in_(uTeam, uLead, fLead, umLine, fmLine)
                    firestoreManager.in_(underdog, int(underdog_score) - int(favorite_score), int(favorite_score) - int(underdog_score), underdog_money, favorite_money)
                    changed = f"{team_1}'s score | {old_team_1_score} -> {team_1_score}"
    
                if old_spread_team_1 != spread_team_1 or old_spread_team_2 != spread_team_2:
                    #open(league, uTeam, fTeam, uSpread, uLead)
                    firestoreManager.open(get_league(URL), underdog, favorite, underdog_spread, int(underdog_score) - int(favorite_score))
                    changed = f"{team_1}'s spread | {old_spread_team_1} -> {spread_team_1}"

                old_team_1_score = team_1_score
                old_team_2_score = team_2_score
                old_spread_team_1= spread_team_1
                old_spread_team_2= spread_team_2
                old_money_team_1= money_team_1
                old_money_team_2= money_team_2

                stdscr.addstr(1,0, f"League: {get_league(URL)}")
                stdscr.addstr(3,0, f"{team_1} Score: {team_1_score} | {team_2} Score: {team_2_score}")
                stdscr.addstr(5,0, f"Underdog Team: {underdog}  | Favorite Team: {favorite}")
                stdscr.addstr(6,0, f"Underdog Spread: {underdog_spread_team} @ {underdog_spread} | Favorite Spread: {favorite_spread_team} @ {favorite_spread}")
                stdscr.addstr(7,0, f"Underdog Lead: {int(underdog_score) - int(favorite_score)} | Favorite Lead: {int(favorite_score) - int(underdog_score)}")
                stdscr.addstr(8,0, f"Underdog Money Line: {underdog_money_team} @ {underdog_money} | Favorite Money Line: {favorite_money_team} @ {favorite_money}")
                stdscr.addstr(10,0, changed)

                stdscr.refresh()

        except NoSuchElementException:
            print("LOCKED")
            pass
        except StaleElementReferenceException:
            pass
