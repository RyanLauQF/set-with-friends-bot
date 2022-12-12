import main
import time
import re
import logging

from card import Card
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import TimeoutException, InvalidArgumentException
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


def link_to_game(updater, game_url):

    # create Chrome browser using selenium for bot to access website
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    logging.info("LINKING TO GAME...")

    # try to enter game lobby
    try:
        driver.get(game_url)
    except InvalidArgumentException:
        updater.message.reply_text("I can't join this game lobby!")
        return

    # clicker used to select cards in browser
    clicker = ActionChains(driver)

    # wait for browser to load page and click away "enter" pop-up
    time.sleep(3)
    enter_button = driver.find_element(By.ID, 'root')
    clicker.move_to_element_with_offset(enter_button, 300, 200).click().perform()

    logging.info("ENTERED GAME LOBBY")
    updater.message.reply_text("I've entered the lobby!")

    # wait max 5 minutes for game to start
    try:
        wait = WebDriverWait(driver, 300)

        # wait for card table to completely load
        wait.until(EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div/div[2]/div[2]''')))

    except TimeoutException:
        logging.info("Timeout after 5 minutes")
        updater.message.reply_text("This game is taking forever to start... I'm going to sleep... zZz")
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
                logging.info("GAME ENDED")
                updater.message.reply_text("Good game! Let's play again!")
                break
            game_end_counter += 1
            continue

        # log sets found
        set_to_string = "Found Set!\n"
        for card in set_found:
            set_to_string += (card.__str__() + "\n")
        logging.info(set_to_string)

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
