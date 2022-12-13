import os
import connect
import logging
from telegram.ext import *

# Heroku deployment configurations
BOT_KEY = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', 500))
LOG_LEVEL = logging.INFO


def start_command(update, context):
    message = '''
    Hey there!

I play the [online multiplayer card-matching game](https://setwithfriends.com/) _Set_. Invite me to a game with you and your friends!

*Let's Play*
Send me a link to a lobby to get started!
    '''

    update.message.reply_text(message, parse_mode='Markdown')


def help_command(update, context):
    message = '''
*How can I help you?*
    
    /start - starts the bot
    /help - bot information
    
Send a game lobby link into the chat to invite me to a game of Set!

*How To Use:*
1.   Visit https://setwithfriends.com/
2.   Create a new game
3.   Ensure "Normal" setting is selected
4.   Send the lobby link to me!
    
If I am not working properly... :(

For bug related issues, report it under *issues* [here](https://github.com/RyanLauQF/set-with-friends-bot)
    
Do not use me to cheat!
    '''

    update.message.reply_text(message, parse_mode='Markdown', disable_web_page_preview=True)


def url_link(update, context):
    game_url = str(update.message.text)

    # check for set with friends link
    if 'setwithfriends.com/room/' not in game_url:
        update.message.reply_text("I can't join this game lobby!")

    else:
        # join lobby
        update.message.reply_text("I'm joining!")
        connect.link_to_game(update, game_url)


def error(update, context):
    logging.warning(f"Update {update} caused error: {context.error}")


def main():
    # Create logger and log telegram bot start
    logging.basicConfig(format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p', level=LOG_LEVEL)
    logging.info("Bot starting...")

    # telegram updater to fetch messages
    updater = Updater(BOT_KEY, use_context=True)
    dp = updater.dispatcher

    # command handlers and url filter to get lobby links
    dp.add_handler(CommandHandler('start', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(MessageHandler(Filters.entity('url'), url_link))

    # error handling
    dp.add_error_handler(error)

    # listen for user messages on telegram via webhook
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=BOT_KEY,
                          webhook_url='https://set-with-friends-telebot.herokuapp.com/' + BOT_KEY)

    updater.idle()


if __name__ == '__main__':
    main()
