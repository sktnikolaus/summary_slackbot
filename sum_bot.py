import os
import time
from slackclient import SlackClient

import sys
sys.path.insert(0, '../nltk')

import summarize

ss = summarize.SimpleSummarizer()


"""
first code adapted from:
https://www.fullstackpython.com/blog/build-first-slack-bot-python.html
"""


# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + str(BOT_ID) + ">"
EXAMPLE_COMMAND = "sum"

DEFAULT_SUMMARY_LENGTH = 3

var = os.environ.get('SLACK_BOT_TOKEN')

# instantiate Slack clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """

    print 'Msg received'
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* (x) command where x is the (optional) desired summary length (number of sentences). Default=1"
    if command.startswith(EXAMPLE_COMMAND):
        #response = "Sure...wait a second!"

        slack_client.api_call("chat.postMessage", channel=channel,
                          text="Sure...here is your summary:", as_user=True)

        if command[4].isdigit():
            output_length = int(command[4])
            command = command[6:]
        else:
            output_length = DEFAULT_SUMMARY_LENGTH
            command = command[4:]
        #print output_length
        
        response = ss.summarize(command, output_length)
    
        print response


    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    #print "wdsd"
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        print output_list
        for output in output_list:

            if output and 'text' in output and AT_BOT in output['text']:
                #@print output['text'].split()
                #os = [str(a) for a in output['text'].split()]
                #print os,AT_BOT
                #if AT_BOT in os:# 
                #print 'abab'
                # return text after the @ mention, whitespace removed
                #    print "ababa"
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                           output['channel']
    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("Summary Bot connected and running!")
        while True:
            #print 'd'
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")







