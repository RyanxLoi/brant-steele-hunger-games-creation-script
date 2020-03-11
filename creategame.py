from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

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

    driver.get(url)

    agreeLink = driver.find_element_by_link_text("I am 13 years or older. I have read and understand these terms.")
    agreeLink.click()

    driver.implicitly_wait(10)

def main():
    print("Input '1' for 24 tributes")
    print("Input '2' for 36 tributes")
    print("Input '3' for 48 tributes")
    numTributes = input("Select number of tributes: ")
    
    create(numTributes)

main()
