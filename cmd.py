#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, division,\
    print_function, unicode_literals

import telegram
import telegram.ext
from telegram.ext.dispatcher import run_async
import logging
import common
import SearchCVE


@common.register_command('cve', pass_args=False)
@run_async
@common.check_cmd_user
def search_cve(bot, update):
    text = update.message.text.split()
    cve_id = text[1]
    if common.check_cve_format(cve_id):
        info = SearchCVE.searchCVEDetails(cve_id)
        msg = "CVE_ID : {0}\n" \
              "Summary : {1}\n" \
              "References : {2}\n\n".format(info['id'],
                                            info['summary'],
                                            info['references'])
        keyboard = [[
            telegram.InlineKeyboardButton("More info", url="http://cve.circl.lu/cve/{0}".format(cve_id))
        ]]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, reply_markup=reply_markup)
    else:
        update.message.reply_text("CVE id format error :( \neg : cve-xxxx-xxxx")


@common.register_command('cves', pass_args=False)
@run_async
@common.check_cmd_user
def get_last_cves(bot, update):
    update.message.reply_text("The lastest CVEs as followed:")
    cve_data = SearchCVE.getLastCVEs()
    for cve in cve_data:
        msg = "CVE_ID : {0}\n" \
              "Summary : {1}\n" \
              "ReferenceURL : {2}\n\n".format(cve["id"],
                                              cve["summary"],
                                              cve["references"])
        keyboard = [[
            telegram.InlineKeyboardButton("More info", url="http://cve.circl.lu/cve/{0}".format(cve["id"]))
        ]]
        reply_markup = telegram.InlineKeyboardMarkup(keyboard)
        update.message.reply_text(msg, reply_markup=reply_markup)


@common.register_command('search', pass_args=True)
@run_async
@common.check_cmd_user
def search(bot, update, args):
    """
    This is a dispatcher.
        1. Search products by vendor.
            /search adobe
        2. Search CVEs of products.
            /search adobe acrobat [count]
    :param bot: 
    :param update:
    :param args:
    :return: 
    """
    text = args[0]
    if len(text) == 2:
        # get vendors all product
        vendor = text[1]
        get_product_of_vendor(bot, update, vendor)
    elif len(text) == 3:
        vendor = text[1]
        product = text[2]
        get_cve_of_product(bot, update, vendor, product)
    elif len(text) == 4:
        vendor = text[1]
        product = text[2]
        count = text[3]
        get_cve_of_product(bot, update, vendor, product, count)


def get_product_of_vendor(bot, update, vendor):
    products = SearchCVE.getProductsByVendor(vendor)
    if products != "None":
        update.message.reply_text("Here are all products({0}):".format(len(products)))
        for idx in range(0,len(products),20):
            msg = "".join('--> ' + item + '\n' for item in products[idx:idx+20])
            # logger.debug(msg)
            update.message.reply_text(msg)
    else:
        update.message.reply_text("No such a vendor...\nAre you kidding me, man ? :(")


def get_cve_of_product(bot, update, vendor, product, count=20):
    cve_data = SearchCVE.searchVendorProduct(vendor, product)
    update.message.reply_text("There {0} CVEs of {1}".format(len(cve_data),product))
    update.message.reply_text("Just show top {0}".format(count))
    if count < len(cve_data):
        cve_data = cve_data[0:count]
    else:
        cve_data = cve_data[0:20]
    if cve_data:
        for cve in cve_data:
            msg = "CVE_ID : {0}\n" \
                  "Summary : {1}\n".format(cve["id"],
                                           cve["summary"])
            ref = "ReferenceURL : {0}\n\n".format(["references"])
            more_info =  "More info : http://cve.circl.lu/cve/{0}".format(cve["id"])
            update.message.reply_text(msg)
            update.message.reply_text(ref)
            update.message.reply_text(more_info)
    else:
        update.message.reply_text("Vendor or Product info error...\nIs that a joke? :(")


@common.register_command('vendors', pass_args=True)
@run_async
@common.check_cmd_user
def get_all_vendors(bot, update, args):
    vendors = SearchCVE.getAllVendors()
    text = args[0]
    if len(text) == 1:
        # return all vendors
        update.message.reply_text("Here are all vendors({0}):".format(len(vendors)))
        for idx in range(0,len(vendors),20):
            msg = "".join('--> ' + item + '\n' for item in vendors[idx:idx+20])
            # logger.debug(msg)
            update.message.reply_text(msg)
    elif len(text) == 2:
        split_char = text[1][0]
        # return vendors,name begin with user specification
        update.message.reply_text("Here all all vendors begin with `{0}`".format(split_char))
        for vendor in vendors:
            if vendor.startswith(split_char):
                update.message.reply_text("--> {0}".format(vendor))
            else:
                pass
    else:
        # format wrong
        update.message.reply_text("Wrong cmd format...\nWhy not take look at help info?")


# TODO: I have no idea how to do this...
@common.register_command('sentry', pass_args=True)
@run_async
@common.check_cmd_user
def sentry(bot, update, args):
    """
    TODO,not finish.
    
    :param bot: 
    :param update:
    :param args: 
    :return: 
    """
    global sentry_status  # And what is this anyway...
    op = args[0]
    if op == "start":
        sentry_status = True
        update.message.reply_text("Begin early warning... ")
    elif op == "stop":
        sentry_status = False
        update.message.reply_text("Stop early warning...")
    else:
        update.message.reply_text("unknown op :( ")
