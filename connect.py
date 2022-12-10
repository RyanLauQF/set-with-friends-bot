import main
import time
import re

from card import Card
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

COLOUR_DICT = {
    '#800080': 'purple',
    '#008002': 'green',
    '#ff0101': 'red'
}

# buffer time to wait for cards to be replaced
CARD_REPLACEMENT_TIME = 0.5

# buffer time for clicks to register
CLICK_DELAY = 0.1


def link_to_game():

    # create Chrome browser using selenium for bot to access website
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    print("BOT STARTED!")

    # prompt for game url
    game_url = input("Enter game URL: ")
    driver.get(game_url)

    # clicker used to select cards in browser
    clicker = ActionChains(driver)

    # wait for browser to load page and click away "enter" pop-up
    time.sleep(3)
    enter_button = driver.find_element(By.ID, 'root')
    clicker.move_to_element_with_offset(enter_button, 300, 200).click().perform()

    print("ENTERED GAME LOBBY!\n")

    # wait max 5 minutes for game to start
    try:
        wait = WebDriverWait(driver, 300)

        # wait for card table to completely load
        wait.until(EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div/div[2]/div[2]''')))

    except TimeoutException:
        print("This game is taking forever to start... I'm going to sleep... zZz")
        driver.quit()
        return

    game_end_counter = 0

    while True:
        # wait for card to be replaced
        # time.sleep(CARD_REPLACEMENT_TIME)

        # scrape from class cards are located in on html page
        elements = driver.find_elements(By.XPATH, "//*[@class='MuiPaper-root MuiPaper-elevation1 MuiPaper-rounded']")

        # get all html elements of cards on page
        all_html_cards = elements[1].find_elements(By.XPATH, "*")[1:]

        # get all cards that are currently shown on the screen
        card_dict = {}
        for card_element in all_html_cards:
            regex_info = re.findall(r'[0-9]+', card_element.get_attribute('style'))

            # check opacity set to 1
            if regex_info[3] == '1':

                # process html information into card object
                card = process_html_info(str(card_element.get_attribute('innerHTML')))
                card_dict[card] = card_element

        # find set amongst cards shown
        set_found = main.find_set(list(card_dict.keys()))

        # game ends when no sets are found 3 times consecutively
        if not set_found:
            if game_end_counter == 3:
                print("GAME ENDED!")
                break
            game_end_counter += 1
            continue

        # log sets found
        print("Found Set!")
        for card in set_found:
            print(card)
        print()

        # get web elements of sets on the screen
        web_element = [card_dict[card] for card in set_found]

        # click the cards
        click_set(web_element, clicker)

        # reset counter as a set has been found
        game_end_counter = 0

    driver.quit()


# returns the information card displayed
def process_html_info(div):
    soup = BeautifulSoup(div, 'html.parser')

    # get all shape classes, objects[0] refers to the first shape
    objects = soup.find_all('svg')

    # number
    num = len(objects)

    # shape
    shape = objects[0].contents[1]['href'].replace('#', '')

    # colour
    colour = COLOUR_DICT[objects[0].contents[1]['stroke']]

    # fill
    fill = objects[0].contents[0]['fill']
    mask = objects[0].contents[0]['mask']

    if fill == 'transparent':
        shading = 'outline'
    elif 'stripe' in mask:
        shading = 'striped'
    else:
        shading = 'solid'

    return Card(colour, shape, num, shading, 0)


# uses selenium ActionChains to click on card web elements
def click_set(web_element, clicker):
    for ele in web_element:
        time.sleep(CLICK_DELAY)
        clicker.move_to_element(ele).click().perform()


# DEBUG
# info = '''position: absolute; transform: translate(328px, 108px) rotate(0deg); opacity: 1; visibility: visible;'''
# d = '''<div class="jss35 jss36" style="width: 146px; height: 88px; margin: 5px; border-radius: 5px; background: initial; transition: width 0.5s ease 0s, height 0.5s ease 0s;"><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg></div>'''
# process_html_info(d)
