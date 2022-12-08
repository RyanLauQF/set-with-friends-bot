import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from main import Card

colour_dict = {
    '#800080': 'purple',
    '#008002': 'green',
    '#ff0101': 'red'
}


def get_game():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    game_url = input("Enter game URL: ")

    driver.get(game_url)
    time.sleep(3)  # wait for browser to open

    game_over = False;
    while not game_over:
        time.sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')  # get entire html of swf page
        divs = soup.find_all("div", {"class": "MuiPaper-root MuiPaper-elevation1 MuiPaper-rounded"})

        for card_box in divs[1].contents[1:]:
            if 'opacity: 1' in card_box['style']:
                card = process_html_info(str(card_box.contents[0]))
                card.print_card()
        print()


# returns the card displayed at div alongside its position
def process_html_info(div):
    soup = BeautifulSoup(div, 'html.parser')

    # get all shape classes, objects[0] refers to the first shape
    objects = soup.find_all('svg')

    # number
    num = len(objects)

    # shape
    shape = objects[0].contents[1]['href'].replace('#', '')

    # colour
    colour = colour_dict[objects[0].contents[1]['stroke']]

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

# DEBUG
# d = '''<div class="jss35 jss36" style="width: 146px; height: 88px; margin: 5px; border-radius: 5px; background: initial; transition: width 0.5s ease 0s, height 0.5s ease 0s;"><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg><svg class="jss34" height="64" style="transition: width 0.5s ease 0s, height 0.5s ease 0s;" viewbox="0 0 200 400" width="32"><use fill="#800080" href="#squiggle" mask=""></use><use fill="none" href="#squiggle" stroke="#800080" stroke-width="18"></use></svg></div>'''


# process_html_info(d)
get_game()
