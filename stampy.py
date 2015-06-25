#!/usr/bin/env python
#
# Description: Bot for controlling karma on Telegram
# Author: Pablo Iranzo Gomez (Pablo.Iranzo@gmail.com)
#
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.    See the
# GNU General Public License for more details.

# TODO
# Mostly everything :), initial steps are there for accessing URL
# - Database integration and updating with new values
# - Confirm last processed message and save it in database as well as sending request to telegram api to mark as read
# - Create functions for the calls to increase/decrease karma
# - Create functions for sending back karma count to originating channel
# - Run loop to get new messages and post updates
# - Consider moving to webhook for async operation

import optparse
import json
import urllib
# import sqlite3 as lite
import sys

description = """
Stampy is a script for controlling Karma via Telegram.org bot api

"""

# Option parsing
p = optparse.OptionParser("stampy.py [arguments]", description=description)
p.add_option("-t", "--token", dest="token", help="API token for bot access to messages", default=None)
p.add_option("-b", "--database", dest="database", help="database file for storing karma and last processed message",
             default="stampy.db")
p.add_option('-v', "--verbosity", dest="verbosity", help="Show messages while running", metavar='[0-n]', default=0,
             type='int')
p.add_option('-u', "--url", dest="url", help="Define URL for accessing bot API", default="https://api.telegram.org/bot")
p.add_option('-c', '--control', dest='control', help="Define chat_id for monitoring service", default=None)

(options, args) = p.parse_args()


if options.token:
    token = options.token
else:
    print "Token required for operation, please check https://core.telegram.org/bots"
    sys.exit(1)

con = None


def sendmessage(options, chat_id=0, text="", reply_to_message_id=None):
    url = "%s%s/sendMessage" % (options.url, options.token)
    message = "%s?chat_id=%s&text=%s" % (url, chat_id, urllib.quote_plus(text))
    if reply_to_message_id:
            message = message + "&reply_to_message_id=%s" % reply_to_message_id
    return json.load(urllib.urlopen(message))


def getupdates(options, offset=0, limit=100):
    url = "%s%s/getUpdates" % (options.url, options.token)
    message = "%s?" % url
    if offset != 0:
        message = message + "&offset=%s" % offset
    message = message + "&limit=%s" % limit
    result = None
    try:
        result = json.load(urllib.urlopen(message))
    except:
        result = None
    for item in result['result']:
        yield item


# Main code

date = 0
lastupdateid = 0
print "Initial message at %s" % date
texto = ""
for message in getupdates(options):
    update_id = message['update_id']
    try:
        texto = message['message']['text']
        chat = message['message']['chat']['id']
    except:
        error = 1

    if update_id > lastupdateid:
        lastupdateid = update_id
    newdate = int(float(message['message']['date']))
    if newdate > date:
        date = newdate
        for word in texto.split():
            if "++" in word:
                print "++ Found in %s at %s with id %s" % (word, chat, update_id)
            if "--" in word:
                print "-- Found in %s at %s with id %s" % (word, chat, update_id)

print "Last processed message at %s" % date
print "Last processed update id %s" % lastupdateid
print "Last processed text %s" % texto

# sendmessage(options, chat_id=options.control, text="Stampy execution ended")
