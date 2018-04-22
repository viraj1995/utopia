'''
Utopia is an Alexa skill programmed in Python to help with depression.

Disclaimer: This skill is not meant to be a cure for depression, but more of an aid for depression.

Author: Kevin Chuang
Date: March 8, 2018

'''

import os
from flask import Flask, json, render_template, jsonify
from flask_ask import Ask, request, session, question, statement, delegate, convert_errors, elicit_slot
import requests
import json
import logging
from num2words import num2words
from pprint import pprint, pformat
from datetime import datetime
import urllib
import re
import boto3
from textblob import TextBlob
import praw
import yaml
from random import randint
from bs4 import BeautifulSoup, Tag, NavigableString


##################################
# App & Environment Initialization
##################################

SESSION_FIRSTNAME = "firstname"
SESSION_SCORE = "SESSION_SCORE"
WORDS = "SENTIMENT_WORD_LIST"
QUESTION = 'QUESTION'
NUM_OF_QUESTIONS = 17
COUNT = 0
BONUS_CONFIRMED = "bonus"

app = Flask(__name__)
ask = Ask(app, "/")
logger = logging.getLogger('flask_ask').setLevel(logging.DEBUG)


##############################
# On Launch
##############################
# When app is first launched, user will wind up here with this @ask.launch decorator
@ask.launch
def start_skill():
    welcome_message = render_template('initial_welcome')
    welcome_reprompt = render_template('initial_welcome_reprompt')
    return question(welcome_message).reprompt(welcome_reprompt)


##########################
# Custom Intents
##########################
@ask.intent("NameIntent",
            mapping= {'firstname': 'FirstName'})
def get_name(firstname):
    name_message = render_template("official_welcome", firstname=firstname)
    name_message_reprompt = render_template("official_welcome_reprompt")
    session.attributes[SESSION_FIRSTNAME] = firstname
    session.attributes_encoder = json.JSONEncoder
    with open('session.json', 'w') as outfile:
        json.dump(session.attributes, outfile, indent=4, sort_keys=True)
    return question(name_message).reprompt(name_message_reprompt)


@ask.intent("SurveyIntent")
def start_survey():

    dialog_state = get_dialog_state()
    session.attributes_encoder = json.JSONEncoder

    ## ADD IN PROGRESS DIALOG STATE
    if dialog_state == "STARTED":
        session.attributes["COUNT"] = 0
        session.attributes["BONUS_COUNT"] = 0
        session.attributes["SCORE"] = 0
        # session.attributes["QUESTION"] = 'BonusOne'
        session.attributes["QUESTION"] = 'One'
        session.attributes["PREV_QUESTION"] = 'BonusOne'
        return delegate()
    elif dialog_state != "COMPLETED":
        # If do not want to continue survey:
        if request["intent"]["slots"]["StartSurvey"]["value"] == 'no':
            return stop()

        survey_question = session.attributes["QUESTION"]
        previous_question = session.attributes["PREV_QUESTION"]
        # If regular survey questions
        if not re.match("Bonus", survey_question):
            if 'value' in request["intent"]["slots"][survey_question]:

                if request["intent"]["slots"][survey_question]["value"] not in ('0', '1', '2', '3', '4'):
                    reprompt_answer = render_template("reprompt_survey")
                    return elicit_slot(survey_question, reprompt_answer)

                # Record answer for question
                session.attributes[survey_question] = int(request["intent"]["slots"][survey_question]["value"])
                # Add each score to get total survey score
                session.attributes["SCORE"] += int(request["intent"]["slots"][survey_question]["value"])
        # If Bonus Questions
        else:
            survey_wait = survey_question + "Wait"
            bonus_wait = request["intent"]["slots"][survey_wait]

            # If bonus wait question
            if 'value' in bonus_wait:
                if request["intent"]["slots"][survey_wait]["value"] == 'no':
                    if session.attributes["BONUS_COUNT"] > 0:
                        session.attributes["BONUS_COUNT"] -= 1
                    bonus_question = render_template(survey_wait)
                    return elicit_slot(survey_wait, bonus_question)

            if previous_question in request["intent"]["slots"]:
                # If actual bonus question
                bonus_question = request["intent"]["slots"][previous_question]
                if 'value' in bonus_question:
                    words = request["intent"]["slots"][previous_question]["value"]
                    session.attributes[previous_question] = words

        # Increment question count for both regular and bonus questions
        if session.attributes["COUNT"] < 16:

            session.attributes["COUNT"] += 1
            survey_question = num2words(session.attributes["COUNT"]).capitalize()
        elif session.attributes["BONUS_COUNT"] < 3:
            previous_question = "Bonus" + num2words(session.attributes["BONUS_COUNT"]).capitalize()
            session.attributes["BONUS_COUNT"] += 1
            survey_question = "Bonus" + num2words(session.attributes["BONUS_COUNT"]).capitalize()

        session.attributes["QUESTION"] = survey_question
        session.attributes["PREV_QUESTION"] = previous_question

        return delegate()

    # Get last bonus question answer
    last_question = session.attributes["QUESTION"]
    session.attributes[last_question] = \
        request["intent"]["slots"][last_question]["value"]

    # Bonus section calculation of score using sentiment analysis
    bonus_list = ['BonusOne', 'BonusTwo', 'BonusThree']
    for bonus in bonus_list:
        words = session.attributes[bonus]
        word_list = words.split()
        bonus_score = 0
        for word in word_list:
            analysis = TextBlob(word)
            bonus_score += analysis.sentiment.polarity

        # Normalize scores based on three adjectives
        bonus_score = bonus_score / 3

        # Increase score based on negative sentiment analysis of words in bonus section
        if bonus_score < 0:
            session.attributes["SCORE"] += (2 / 3) * (-bonus_score)

    score = round(float(session.attributes["SCORE"]), 2)

    session.attributes[SESSION_SCORE] = score

    # Dumping session data for debug
    with open('session.json', 'w') as outfile:
        json.dump(session.attributes, outfile, indent=4, sort_keys=True)

    if score >= 0 and score <= 7:
        # Normal
        score_message = render_template('normal', score=score)

    elif score > 7 and score <= 13:
        # Mild Depression
        score_message = render_template('mild', score=score)

    elif score > 13 and score <= 18:
        # Moderate Depression
        score_message = render_template('moderate', score=score)

    elif score > 18 and score <= 22:
        # Severe Depression (Will categorize in the same category as very severe depression)
        score_message = render_template('severe', score=score)

    elif score > 22:
        # Very Severe Depression
        score_message = render_template('very_severe', score=score)

    else:
        score_message = 'I was unable to calculate your Hamilton survey score. Sorry.'

    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('databaseTableName')
    return question(score_message)


@ask.intent("TalkToIntent")
def talk_to_someone():
    firstname = session.attributes[SESSION_FIRSTNAME]
    end_msg = "Hello %s ." % firstname
    return statement(end_msg + "This is the talk to intent.")


@ask.intent("GetQuoteTypeIntent")
def get_quote_type():
    dialog_state = get_dialog_state()
    session.attributes_encoder = json.JSONEncoder
    if dialog_state == 'STARTED':
        session.attributes['Category'] = 'positive'
        return delegate()
    elif dialog_state == 'IN_PROGRESS':
        session.attributes['Category'] = request['intent']['slots']['Category']['value']
        return delegate()
    elif dialog_state == 'COMPLETED':
        session.attributes['Category'] = request['intent']['slots']['Category']['value']
        return give_quote(category=session.attributes['Category'])


@ask.intent("QuoteIntent")
def give_quote(category='positive'):

    try:
        if category != request['intent']['slots']['Category']['value']:
            category = request['intent']['slots']['Category']['value']
            session.attributes['Category'] = category
    except KeyError:
        category = session.attributes['Category']

    num_quotes = get_brainy_quotes(category)
    quote_index = randint(1, num_quotes)

    quote = session.attributes['Quote{}'.format(num2words(quote_index).capitalize())]
    quote_msg = render_template('quote', category=category, quote=quote)
    return question(quote_msg)


##############################
# Overriding Required Intents
##############################

@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    try:
        firstname = session.attributes[SESSION_FIRSTNAME]
    except KeyError:
        firstname = 'my friend'
    bye_message = render_template("bye", firstname=firstname)
    return statement(bye_message)


@ask.session_ended
def session_ended():
    return "{}", 200


##############################
# Helper Functions
##############################
def get_brainy_quotes(category, number_of_quotes=10):
    popular_choice = ['motivational', 'inspirational',
                      'life', 'smile', 'family', 'positive',
                      'friendship', 'success', 'happiness', 'love']

    url = "http://www.brainyquote.com/quotes/topics/topic_" + category + ".html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quotes = []
    for i, quote in enumerate(soup.find_all('a', {'title': 'view quote'})):
        if isinstance(quote.contents[0], NavigableString):
            session.attributes['Quote{}'.format(num2words(i + 1).capitalize())] = \
                str(quote.contents[0]).replace('-', 'By')
            quotes.append(str(quote.contents[0]).replace('-', 'By'))
        elif isinstance(quote.contents[0], Tag):
            session.attributes['Quote{}'.format(num2words(i + 1).capitalize())] = \
                quote.contents[0].attrs['alt'].replace('-', 'By')
            quotes.append(quote.contents[0].attrs['alt'].replace('-', 'By'))

    result = quotes[:number_of_quotes]
    return len(result)


def get_dialog_state():
    return session['dialogState']


##############################
# Program Entry
##############################

if __name__ == '__main__':

    app.config['ASK_PRETTY_DEBUG_LOGS'] = True

    app.run(debug=True)
