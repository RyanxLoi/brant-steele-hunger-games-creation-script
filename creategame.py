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

    #read csv
    with open('cast.csv', newline='') as castFile:
        castReader = csv.reader(castFile)
        for row in castReader:
            cast.append(row)

    #The cast list can be shuffled to randomly pair tributes. Comment the line below to disable it.
    random.shuffle(cast)

    #['2020/03/12 12:58:30 PM AST', 'Glimmer', 'Glimmer', 'She/Her', 'https://i.imgur.com/JgiO6zy.png', 'Player 2 performs an action']

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

    submitBtn = driver.find_element_by_xpath("//input[@type='submit' and @value='Submit']").click()
    submitBtn.click()

    #Generate game and get link
    proceed = driver.find_element_by_link_text("Proceed.")
    proceed.click()
 
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
