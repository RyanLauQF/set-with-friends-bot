# Set with Friends Telegram Bot

A Telegram bot [@setwithfriends_bot](https://t.me/setwithfriends_bot) that plays the [online multiplayer card-matching game](https://setwithfriends.com/) _Set_!
> It can join live game lobbies and will play once the game begins!

_Set_ revolves around matching a combination of 3 cards based on 4 features:
- colour (purple, red, green)
- number (1, 2, 3)
- shape (oval, diamond, squiggle)
- shading (solid, outline, striped)
          
The cards of a set must display features that are either all the same or all different.

## Technical Details
> Currently deployed on Heroku under the Eco-Dyno
- On start, bot will request for `html` of game lobby. (Timeout after 5 minutes if game does not start)
- `Selenium` library to dynamically scrape javascript elements that control the game.
- `Beautiful Soup 4` library to parse html and process into card information.
- Backtracking to generate all combinations of sets of 3 cards from cards shown. Sets are checked after generation based on game rules.

## Technologies
<img align="left" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg" style="padding-right:10px;" />
<img align="left" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/heroku/heroku-plain-wordmark.svg" style="padding-right:10px;" />
<img align="left" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/selenium/selenium-original.svg" style="padding-right:10px;" />
<img align="left" width="26px" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" style="padding-right:10px;" />

<br />
<br />

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Source codes are available under the MIT License. Developed by [Ryan Lau Q. F.](https://github.com/RyanLauQF)

Enjoy playing against it!
