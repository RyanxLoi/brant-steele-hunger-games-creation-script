# The Brant Steele Hunger Games Generator Script
Given two csv files, this script can quickly generate a simulated Hunger Game using Brant Steele's generator. 

This script was specifically created for a Discord server, but can be modified as necessary to suit your needs. 

# Prerequisites

In order to use this script, you'll need:

* FireFox or Google Chrome: [Download Google Chrome here](https://www.google.com/chrome/) OR [Download Firefox here](https://www.mozilla.org/en-CA/firefox/)
* The web driver for your preferred browser above: [ChromeDriver for Google Chrome](https://chromedriver.chromium.org/) OR [geckodriver for FireFox](https://github.com/mozilla/geckodriver/releases)
* Selenium WebDriver: [Download here](https://www.selenium.dev/)

Ensure that your browser drivers are placed in your PATH in order for the script to work. 

# Downloading and Set Up

To download, you may simply download the repository as a zip folder or clone the repository using git. 

Once downloaded, you'll have to make some modifications to `cast.csv`, `events.csv` and `creategame.py`.

Do not change the names of the above files as they are referenced in the code. 

## cast.csv

cast.csv is your file that contains information on your tributes. It contains the follow headers:

* Timestamp	
* Name	
* Discord Name
* Pronouns	
* Profile pic link	
* Event

If you have created a Google form that people can use to apply to your Hunger Games, you can simply export the results to this folder and rename it as cast.csv. 

## events.csv

events.csv contains custom events that may occur during your game. It has the following headers:

* Type	
* Fatal	
* NumberTrib	
* T1Killer	
* T2Killer	
* T3Killer	
* T4Killer	
* T5Killer	
* T6Killer	
* T1Killed	
* T2Killed	
* T3Killed	
* T4Killed	
* T5Killed	
* T6Killed	
* Event

### Type

The type refers to when the event occurs. It can occur during one of the following times of the day:

* Bloodbath
* Day
* Night
* Feast

**NOTE:** At this time, it cannot support arena events. 

### Fatal

Fatal determines if the event results in at least one tribute being eliminated from the game. The cells in the csv are either marked with a "Y" for yes (fatal) or "N" for no (not fatal).

### NumTributes

This refers to how many tributes are involved in an event. It can range from 1 to 6 inclusive. 

### T1-T6 Killer and Killed

These columns determine which players are the killers and which players are killed. Cells in this column are marked with either a 0 for "No" (Player is not the killer and/or not killed) and 1 for "Yes" (Player is the killer and/or not killed). Events where players are marked as a killer will have their kill count increase by 1 when the event occurs.   

### Event

This is the description of the event itself. 

## creategame.py

This is the script itself. The follow modifications can be made to the script:

### What Browser to Use

You have the option to create the game using either Firefox or Google Chrome. To select one of the browsers, comment out the code of the browser that you are not using in the code block below in the file. 

```
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
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    #create Chrome driver
    driver = webdriver.Chrome("/usr/local/share/chromedriver",chrome_options=chrome_options)
```

### Season Name and Season Url

These are fields that label and represent your game.

``` 
    seasonName = driver.find_element_by_name("seasonname")
    seasonName.send_keys("Hunger Games")
    logoUrl = driver.find_element_by_name("logourl")
    logoUrl.send_keys("https://upload.wikimedia.org/wikipedia/en/d/dc/The_Hunger_Games.jpg")
```

In this block above, you may change the name of the season in the quotaton marks inside `seasonName,send_keys` and the url of the logo for your game in the quotation marks inside `logoUrl.send_keys`.

# Usage

When everything has been set up, in your terminal, go into the folder and type in `python creategame.py`. From there, you'll be prompted to select to create a game with either 24, 36 or 48 tributes and you are good to go.

Once your game has been created, you can obtain the url provided by the generator and share it!