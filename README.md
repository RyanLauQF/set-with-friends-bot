# Set with Friends Bot

A Bot that plays the [online multiplayer card-matching game](https://setwithfriends.com/) _Set_!
> It can join live game lobbies and will play once the game begins!

_Set_ revolves around matching a combination of 3 cards based on 4 features:
- colour (purple, red, green)
- number (1, 2, 3)
- shape (oval, diamond, squiggle)
- shading (solid, outline, striped)

The cards of a set must display features that are either all the same or all different.

## Technical Details
- On start, bot will request for `html` of game lobby. (Timeout after 5 minutes if game does not start)
- `Selenium` library to dynamically scrape javascript elements that control the game.
- `Beautiful Soup 4` library to parse html and process into card information.
- Backtracking to generate all combinations of sets of 3 cards from cards shown. Sets are checked after generation based on game rules.

## License

MIT License.

Enjoy playing against it!
