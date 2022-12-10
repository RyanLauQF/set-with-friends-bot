import main
import time
import re

from card import Card
from bs4 import BeautifulSoup
from selenium import webdriver
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
CARD_REPLACEMENT_TIME = 0.75


def link_to_game():
    # create Chrome browser using selenium for bot to access website
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--start-maximised")
    driver = webdriver.Chrome(options=chrome_options)

    # prompt for game url
    game_url = input("Enter game URL: ")
    driver.get(game_url)

    # enter game lobby
    while True:
        user_start = input("Start Bot?: ")
        if user_start != 'y':
            continue
        else:
            print("BOT STARTED!")
            break

    # wait for card table to load completely
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '''//*[@id="root"]/div/div/div[2]/div[2]''')))

    # clicker used to select cards in browser
    clicker = ActionChains(driver)

    game_end_counter = 0

    while True:
        # wait for card to be replaced
        time.sleep(CARD_REPLACEMENT_TIME)

        # get entire html of swf page
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # class cards are located in on html page
        divs = soup.find_all("div", {"class": "MuiPaper-root MuiPaper-elevation1 MuiPaper-rounded"})

        # class name of the cards displayed
        class_name = None

        # get all cards that are currently shown on the screen
        cards = []
        for card_box in divs[1].contents[1:]:
            regex_info = re.findall(r'[0-9]+', card_box['style'])

            # check opacity set to 1
            if regex_info[3] == '1':

                # get class name of cards displayed
                if class_name is None:
                    class_name = ' '.join(card_box.contents[0]['class'])

                # process html information into card object
                card = process_html_info(str(card_box.contents[0]))
                cards.append(card)

        # get web elements of all cards
        elements = driver.find_elements(By.XPATH, "//*[@class='" + class_name + "']")

        # since order is preserved we can zip both together
        card_dict = dict(zip(cards, elements))

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
        clicker.move_to_element(ele).click().perform()
        time.sleep(0.01)


# DEBUG
# info = '''position: absolute; transform: translate(328px, 108px) rotate(0deg); opacity: 1; visibility: visible;'''
# d = '''<div class="jss35 jss36" style="width: 146px; height: 88px; margin: 5px; border-radius: 5px; background: initial; transition: width 0.5s ease 0s, height 0.5s ease 0s;"><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg></div>'''
# process_html_info(d)
