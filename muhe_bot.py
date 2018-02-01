#!/usr/bin/python
# -*- coding: utf-8 -*-
# File Name: muhe_bot.py
# Author: o0xmuhe
# Mail: o0xmuhe@gmail.com
# Created Time: 2018-02-01 10:08:22

import sys
from telegram.ext import CommandHandler, MessageHandler, Filters
from telegram.ext.dispatcher import run_async
import telegram
from flask import Flask, request
import threading
import logging
import json
import os
import common

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

token = ""
current_path = os.path.split(os.path.realpath(__file__))[0]
sentry_status = False


def init():
    global token
    conf_file = current_path + '/conf.json'
    if os.path.exists(conf_file):
        with open(conf_file,'r') as f:
            data = json.loads(f.read().strip())
        token = data["Token"]
        logger.info("[*]Get token ok.")
    else:
        logger.error("[*]Cannot find config file,plz double check it!")


@run_async
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Welcome to muhe\'s bot :)')


@run_async
def help(bot, update):
    """Send a message when the command /help is issued."""
    help_info = """Help info as follow:
    /vendors : get all vendors.
    /search [vendor] : get vendor's all product.
    /search [vendor] [product] : get all cve's about product of vendor.
    /cves : get last cves.
    /cve [cve-xxxx-xxxx] : get info of cve-xxxx-xxxx.
    /sentry start : Begin early waring
    /sentry stop  : Stop early waring
    """
    update.message.reply_text(help_info)


@run_async
def ping(bot, update):
    """Echo the user message."""
    message = """Pong!
    ```text
    UserID: %d
    ChatID: %d```
    """ % (
        update.message.from_user.id,
        update.message.chat_id
    )
    update.message.reply_text(message, parse_mode='Markdown')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def add_handlers(dispatcher):
    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))

    # on non-command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text, ping))

    # log all errors
    dispatcher.add_error_handler(error)

bot = telegram.Bot(token)
web_server = Flask(__name__)
job_queue = telegram.ext.updater.Queue()
dispatch = telegram.ext.updater.Dispatcher(bot, job_queue)


@web_server.route('/', methods=['POST'])
def run_bot():
    incoming = json.dumps(request.get_json(force=True))
    update = telegram.update.Update.de_json(request.get_json(force=True), bot)
    is_edited = update.message or update.edited_message or update.channel_post or update.callback_query.message

    logging.info("@%s (%s) - chat:%d - msg:%d: %s" % (
        is_edited.from_user.username,
        is_edited.from_user.id,
        is_edited.chat_id,
        is_edited.message_id,
        is_edited.text
    ))

    # dispatch.process_update(update)
    job_queue.put(update)
    return "OK"


def main():
    """Init token"""
    init()
    """Start the bot."""
    common.dispatcher = dispatch

    # You can import your modules here:
    import cmd

    # And finally, register all commends.
    add_handlers(common.dispatcher)

    # Multiple thread
    thread = threading.Thread(target=dispatch.start, name='dispatch')
    thread.start()

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    # Flask log
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    # All set, run.
    logging.info("Successfully login and ready for processing request.")
    web_server.run(host='0.0.0.0', port=6000, debug=False)


if __name__ == '__main__':
    sys.exit(int(main() or 0))
