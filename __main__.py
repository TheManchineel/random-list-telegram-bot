from telegram import Update, ParseMode
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import random
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')
bot_token=config['Bot']['bot_token']

updater = Updater(token=bot_token)
dispatcher = updater.dispatcher

log_dir = os.path.join(os.getcwd(), 'logs')
log_path = os.path.join(log_dir, 'bot.log')

import os
if not os.path.exists(log_dir):
    os.mkdir(log_dir)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO, filename=log_path, filemode='w')

# Message texts
start_message = """Welcome to Random List Bot! Please use /randomize followed by the items of your list, separated by commas, like so:

/randomize
One,
Two,
Three,
...

or:

/randomize One, Two, Three

"""

random_list_message = "<b>Your randomized list:</b>\n\n{}"

# Commands
def start(update: Update, context: CallbackContext):
    """Send a message when the command /start is issued."""
    logging.info(f"*** Added to chat: {update.effective_chat.id}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=start_message)

def randomize(update: Update, context: CallbackContext):
    """Randomize a list"""
    input_text = ' '.join(context.args)
    logging.info(f">>> [{update.effective_chat.id}] Received command: /randomize {input_text}")
    if input_text == "":
        reply_message = "You need to enter at least one item, each item separated by a comma."
    else:
        input_list = [x.strip() for x in input_text.split(',')]
        random.shuffle(input_list)
        generated_list = ""
        for i in input_list:
            generated_list += f"• {str(i)}\n"
        reply_message = random_list_message.format(generated_list)
    logging.info(f"<<< [{update.effective_chat.id}] Issued reply: {reply_message.encode('unicode_escape')}")
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message, parse_mode=ParseMode.HTML)

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('randomize', randomize))

# Run bot
updater.start_polling()