from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

import random
import csv

url = "https://brantsteele.net/hungergames/disclaimer.php"

def create(numTributes):

    #Create firefox profile with preferences to disable loading images
    #Disabling images allows the page to load faster
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')

    #create driver
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.implicitly_wait(20)
    driver.maximize_window()

    #Start process
    driver.get(url)

    agreeLink = driver.find_element_by_link_text("I am 13 years or older. I have read and understand these terms.")
    agreeLink.click()

    if numTributes == 36 or numTributes == 48:
        adjustSize = driver.find_element_by_link_text("Adjust Size")
        adjustSize.click()
        if numTributes == 36:
            newSize = driver.find_element_by_link_text("Use 36 tributes.")
            newSize.click()
        elif numTributes == 48:
            newSize = driver.find_element_by_link_text("Use 48 tributes.")
            newSize.click()

    hoverLink = driver.find_element_by_link_text("Simulate")
    hover = ActionChains(driver).move_to_element(hoverLink)
    hover.perform()
    driver.implicitly_wait(10)

    createPersonal = driver.find_element_by_link_text("Personal")
    createPersonal.click()

    driver.implicitly_wait(10)

    seasonName = driver.find_element_by_name("seasonname")
    seasonName.send_keys("uOttawa Hunger Games")
    logoUrl = driver.find_element_by_name("logourl")
    logoUrl.send_keys("https://i.imgur.com/JgiO6zy.png")

    cast = []

    #read csv for cast
    with open('cast.csv', newline='') as castFile:
        castReader = csv.reader(castFile)
        for row in castReader:
            cast.append(row)

    #['2020/03/12 12:58:30 PM AST', 'Glimmer', 'Glimmer', 'She/Her', 'https://i.imgur.com/JgiO6zy.png', 'Player 2 performs an action']

    #Create cast
    for i in range(1,numTributes+1):
        if i < 10:
            num = "0" + str(i)
        else:
            num = str(i)
        tribName = "cusTribute" + num
        tribImg = tribName + "img"
        tribGender = tribName + "gender"

        driver.find_element_by_name(tribName).send_keys(cast[i][1])
        driver.find_element_by_name(tribImg).send_keys(cast[i][4])

        selectGender = Select(driver.find_element_by_name(tribGender))
        if cast[i][3] == "He/Him":
            selectGender.select_by_index("1")
        else:
            selectGender.select_by_index("2")

    bwBtn = driver.find_element_by_class_name("MakeEvictedBW")
    bwBtn.click() 

    sameNickBtn = driver.find_element_by_class_name("MakeEvictedNames")
    sameNickBtn.click()

    submitBtn = driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']")
    submitBtn.click()

    #Create events

    events = []

    #read csv for events
    with open('events.csv', newline='') as eventsFile:
        eventsReader = csv.reader(eventsFile)
        for row in eventsReader:
            events.append(row)

    modifyEvents = driver.find_element_by_link_text("Modify Events")
    modifyEvents.click()

    #['Type', 'Fatal', 'NumberTrib', 'T1Killer', 'T1Killed', 'T2Killer', 'T2Killed', 'T3Killer', 'T3Killed', 'T4Killer', 'T4Killed', 'T5Killer', 'T5Killed', 'T6Killer', 'T6Killed', 'Event']
    #['Arena', 'Y', '6', 'N', 'Y', 'N', 'Y', 'N', 'Y', 'N', 'Y', 'N', 'Y', 'N', 'Y', '(Player1), (Player2), (Player3), (Player4), (Player5), and (Player6) all get lit on fire.']

    for j in range(1,len(events)):
        eventType = events[j][0].lower()
        killerCol = 3
        killedCol = 9
        #Bloodbath events
        #The outer if condition checks for the type of event. The inner if condition checks if the event is fatal.
        
        if events[j][1] == "N":
            driver.get("https://brantsteele.net/hungergames/AddEvent.php?type="+eventType)
            numTribsSelect = Select(driver.find_element_by_name("EventNumber"))
            numTribsEvent = events[j][2]
            numTribsSelect.select_by_value(str(numTribsEvent))
            driver.find_element_by_name("EventText").send_keys(events[j][15])
            driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()
        elif events[j][1] == "Y":
            driver.get("https://brantsteele.net/hungergames/AddEvent.php?type="+eventType+"fatal")
            numTribsSelect = Select(driver.find_element_by_name("EventNumber"))
            numTribsEvent = events[j][2]
            numTribsSelect.select_by_value(str(numTribsEvent))

            for trib in range(1,(int(numTribsEvent)+1)):
                if events[j][killerCol] != "-" or events[j][killedCol] != "-":
                    killerSelect = Select(driver.find_element_by_name("killer"+str(trib)))
                    killedSelect = Select(driver.find_element_by_name("killed"+str(trib)))
                    killerSelect.select_by_value(events[j][killerCol])
                    killedSelect.select_by_value(events[j][killedCol])
                    killerCol += 1
                    killedCol += 1
                else:
                    continue
            
            driver.find_element_by_name("EventText").send_keys(events[j][15])
            driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()

        driver.get("https://brantsteele.net/hungergames/ModifyEvents.php")

    #Generate game and get link
    driver.find_element_by_link_text("Save").click()
    driver.find_element_by_link_text("Yes").click()

    print("Game saved successfully! Obtain the url to the game provided by the simulator and enjoy! :)")
    
 
def main():
    print("Input '1' for 24 tributes")
    print("Input '2' for 36 tributes")
    print("Input '3' for 48 tributes")

    numTributes = int(input("Select number of tributes: "))

    #Assume correct inputs for now. We'll add exception handling later.
    if numTributes == 1:
        numTributes = 24
    elif numTributes == 2:
        numTributes = 36
    elif numTributes == 3:
        numTributes = 48
    else:
        print("Incorrect input.")
        
    create(numTributes)

main()
