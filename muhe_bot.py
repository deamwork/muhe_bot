#!/usr/bin/python
#-*- coding:utf-8 -*-
# File Name: muhe_bot.py
# Author: o0xmuhe
# Mail: o0xmuhe@gmail.com
# Created Time: 2018-02-01 10:08:22

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from SearchCVE import *
import logging
import json
import os,re

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


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi! Welcome to muhe\'s bot :)')


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


def echo(bot, update):
    """Echo the user message."""
    update.message.reply_text("zzzzzzZZZZZZZZZ.....")
    update.message.reply_text("Why not take a look at help?")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def get_all_vendors(bot,update):
    vendors = SearchCVE.getAllVendors()
    text = update.message.text.split()
    if len(text) == 1:
        # return all vendors
        update.message.reply_text("Here are all vendors({0}):".format(len(vendors)))
        for idx in range(0,len(vendors),20):
            msg = "".join('--> ' + item + '\n' for item in vendors[idx:idx+20])
            # logger.debug(msg)
            update.message.reply_text(msg)
    elif len(text) == 2:
        split_char = text[1][0]
        # return vendors,name begin with user specificate
        update.message.reply_text("Here all all vendors begin with `{0}`".format(split_char))
        for vendor in vendors:
            if vendor.startswith(split_char):
                update.message.reply_text("--> {0}".format(vendor))
            else:
                pass
    else:
        # format wrong
        update.message.reply_text("Wrong cmd format...why not take look at help info?")


def get_product_of_vendor(bot,update,vendor):
    products = SearchCVE.getProductsByVendor(vendor)
    if products != "None":
        update.message.reply_text("Here are all products({0}):".format(len(products)))
        for idx in range(0,len(products),20):
            msg = "".join('--> ' + item + '\n' for item in products[idx:idx+20])
            # logger.debug(msg)
            update.message.reply_text(msg)
    else:
        update.message.reply_text("No such a vendor...Are you kidding me,man ? :(")


def get_cve_of_product(bot,update,vendor,product,count=20):
    cve_data = searchVendorProduct(vendor,product)
    update.message.reply_text("There {0} CVEs of {1}".format(len(cve_data),product))
    update.message.reply_text("Just show top {0}".format(count))
    if count < len(cve_data):
        cve_data = cve_data[0:count]
    else:
        cve_data = cve_data[0:20]
    if cve_data:
        for cve in cve_data:
            msg = "CVE_ID : {0}\n" \
                  "Summary : {1}\n".format(cve["id"], \
                                           cve["summary"])
            ref = "ReferenceURL : {0}\n\n".format(["references"])
            more_info =  "More info : http://cve.circl.lu/cve/{0}".format(cve["id"])
            update.message.reply_text(msg)
            update.message.reply_text(ref)
            update.message.reply_text(more_info)
    else:
        update.message.reply_text("Vendor or Product info error...Are you kidding me,man ? :(")


def search(bot,update):
    '''
        This is a dispatcher.
        1. Search products by vendor.
            /search adobe
        2. Search CVEs of products.
            /search adobe acrobat [count]
    '''
    text = update.message.text.split()
    if len(text) == 2:
        # get vendors all product
        vendor = text[1]
        get_product_of_vendor(bot,update,vendor)
    elif len(text) == 3:
        vendor = text[1]
        product = text[2]
        get_cve_of_product(bot,update,vendor,product)
    elif len(text) == 4:
        vendor = text[1]
        product = text[2]
        count = text[3]
        get_cve_of_product(bot, update, vendor, product,count)


def get_last_cves(bot,update):
    update.message.reply_text("The lastest CVEs as followed:")
    cve_data = SearchCVE.getLastCVEs()
    for cve in cve_data:
        msg = "CVE_ID : {0}\n" \
              "Summary : {1}\n" \
              "ReferenceURL : {2}\n\n".format(cve["id"],\
                                          cve["summary"],\
                                          cve["references"])
        msg += "More info : http://cve.circl.lu/cve/{0}".format(cve["id"])
        update.message.reply_text(msg)



def check_cve_format(string):
    r = re.compile(r"cve-.*-.*")
    r1  = re.compile(r"CVE-.*-.*")
    if (r.match(string) is not None) or (r1.match(string) is not None):
        return True
    else:
        return False



def search_cve(bot,update):
    text = update.message.text.split()
    cve_id = text[1]
    if check_cve_format(cve_id):
        info = SearchCVE.searchCVEDetails(cve_id)
        msg = "CVE_ID : {0}\n" \
              "Summary : {1}\n" \
              "References : {2}\n\n".format(info['id'],\
                                        info['summary'],\
                                        info['references'])
        msg += "More info : http://cve.circl.lu/cve/{0}".format(cve_id)
        update.message.reply_text(msg)
    else:
        update.message.reply_text("CVE id format error :( ")
        update.message.reply_text("eg : cve-xxxx-xxxx")



def sentry(bot,update):
    '''
        TODO,not finish.
    '''
    global sentry_status
    text = update.message.text.split()
    op = text[1]
    if op == "start":
        sentry_status = True
        update.message.reply_text("Begin early warning... ")
    elif op == "stop":
        sentry_status = False
        update.message.reply_text("Stop early warning...")
    else:
        update.message.reply_text("unknown op :( ")



def main():
    """Init token"""
    init()
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # my own methos
    dp.add_handler(CommandHandler("vendors", get_all_vendors))
    dp.add_handler(CommandHandler("search", search))
    dp.add_handler(CommandHandler("cves", get_last_cves))
    dp.add_handler(CommandHandler("cve", search_cve))
    dp.add_handler(CommandHandler("sentry",sentry))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
