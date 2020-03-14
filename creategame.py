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

    #############################################################
    #
    #This script is currently supported on Firefox and Google Chrome. Select your preferred browser and disable the other one by #commenting out the code of the other browser below before the next line of hashtags. From my personal experience, Firefox #performs much faster than Chrome but Chrome is still an option.
    #
    ##############################################################
    
    #Create firefox profile with preferences to disable loading images
    #Disabling images allows the page to load faster
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference('permissions.default.image', 2)
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')
    #create Firefox Driver
    driver = webdriver.Firefox(firefox_profile=firefox_profile)


    #Create chrome profile with preferences to disable loading images
    #Disabling images allows the page to load faster
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    #create Chrome driver
    driver = webdriver.Chrome("/path/to/chromedriver",chrome_options=chrome_options)

    driver.implicitly_wait(20)
    driver.maximize_window()

    ##############################################################################################

    #Start process
    driver.get(url)

    #Agree to TOC
    agreeLink = driver.find_element_by_link_text("I am 13 years or older. I have read and understand these terms.")
    agreeLink.click()

    #Change cast size if user has selected 36 or 48 tributes
    if numTributes == 36 or numTributes == 48:
        adjustSize = driver.find_element_by_link_text("Adjust Size")
        adjustSize.click()
        if numTributes == 36:
            newSize = driver.find_element_by_link_text("Use 36 tributes.")
            newSize.click()
        elif numTributes == 48:
            newSize = driver.find_element_by_link_text("Use 48 tributes.")
            newSize.click()

    #Begin creating the game
    hoverLink = driver.find_element_by_link_text("Simulate")
    hover = ActionChains(driver).move_to_element(hoverLink)
    hover.perform()
    driver.implicitly_wait(10)

    createPersonal = driver.find_element_by_link_text("Personal")
    createPersonal.click()

    driver.implicitly_wait(10)

    #For send_keys, you may replace the content inside the quotation marks with another name for your season and another url for your logo
    seasonName = driver.find_element_by_name("seasonname")
    seasonName.send_keys("Hunger Games")
    logoUrl = driver.find_element_by_name("logourl")
    logoUrl.send_keys("https://upload.wikimedia.org/wikipedia/en/d/dc/The_Hunger_Games.jpg")

    cast = []

    #read csv for cast
    with open('cast.csv', newline='') as castFile:
        castReader = csv.reader(castFile)
        for row in castReader:
            cast.append(row)

    #[Timestamp,Name,Discord Name,Pronouns,Profile pic link,Events]

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
    
    #['Type', 'Fatal', 'NumberTrib', 'T1Killer', 'T2Killer', 'T3Killer', 'T4Killer', 'T5Killer', 'T6Killer', 'T1Killed', 'T2Killed', 'T3Killed', 'T4Killed', 'T5Killed', 'T6Killed', 'Event']

    for j in range(1,len(events)):
        eventType = events[j][0].lower()
        killerCol = 3
        killedCol = 9
        
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

    numTributes = 0
    validOption = False

    while numTributes < 1 or numTributes > 3 and validOption == False:
        try:
            numTributes = int(input("Select number of tributes: "))
            if numTributes == 1:
                numTributes = 24
                validOption = True
            elif numTributes == 2:
                numTributes = 36
                validOption = True
            elif numTributes == 3:
                numTributes = 48
                validOption = True
            if validOption == True:
                break
            else:
                print("Invalid input. Input 1, 2 or 3.")
        except ValueError:
            print("Invalid input. Input 1, 2 or 3.")
        
    create(numTributes)

main()
