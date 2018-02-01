#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division,\
    print_function, unicode_literals
import re
import telegram.ext

dispatcher = None


def register_command(cmd, **kw):
    def func_recver(func):
        dispatcher.add_handler(
            telegram.ext.CommandHandler(cmd, func, **kw))
        return func
    return func_recver


def register_callback(cmd, **kw):
    def func_recver(func):
        dispatcher.add_handler(
            telegram.ext.CallbackQueryHandler(func))
        return func
    return func_recver


def register_regex(cmd, **kw):
    def func_recver(func):
        dispatcher.add_handler(
            telegram.ext.RegexHandler(cmd, func, **kw))
        return func
    return func_recver


def check_cmd_user(func):
    def checker(bot, update, **kw):
        command_name = update.message.text.split()[0].split('@')
        if len(command_name) > 1\
           and command_name[1] != bot.getMe()['username']:
            return
        bot.sendChatAction(
            chat_id=update.message.chat_id,
            action=telegram.ChatAction.TYPING
        )
        return func(bot, update, **kw)
    return checker


def check_cve_format(string):
    r = re.compile(r"cve-.*-.*")
    r1 = re.compile(r"CVE-.*-.*")
    if (r.match(string) is not None) or (r1.match(string) is not None):
        return True
    else:
        return False
