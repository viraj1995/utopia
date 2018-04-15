import os
from flask import Flask, json, render_template
from flask_ask import Ask, request, session, question, statement, delegate, convert_errors, elicit_slot
import requests
import json
import logging
from pythonjsonlogger import jsonlogger
from num2words import num2words
from pprint import pprint, pformat
from datetime import datetime
import urllib
import re
import boto3
from textblob import TextBlob


SESSION_FIRSTNAME = "firstname"
SESSION_SCORE = "SESSION_SCORE"
WORDS = "SENTIMENT_WORD_LIST"
QUESTION = 'QUESTION'
NUM_OF_QUESTIONS = 17
COUNT = 0
BONUS_CONFIRMED = "bonus"
#LIST_OF_QUESTIONS = {num2words(x).title():None for x in range(1, 4)}
#LIST_OF_QUESTIONS = [num2words(x).title() for x in range(1, 4)]

app = Flask(__name__)
ask = Ask(app, "/")
formatter = jsonlogger.JsonFormatter(json_indent=4)
logHandler = logging.StreamHandler()
logger = logging.getLogger('flask_ask')
logger.setLevel(logging.DEBUG)
logHandler.setFormatter(formatter)
logger.addHandler(logHandler)


# When app is first launched, user will wind up here with this @ask.launch decorator
@ask.launch
def start_skill():
    welcome_message = render_template('initial_welcome')
    welcome_reprompt = render_template('initial_welcome_reprompt')
    return question(welcome_message).reprompt(welcome_reprompt)


@ask.intent("NameIntent",
            mapping= {'firstname':'FirstName'})
def get_name(firstname):
    name_message = render_template("official_welcome" , firstname=firstname)
    name_message_reprompt = render_template("official_welcome_reprompt")
    session.attributes[SESSION_FIRSTNAME] = firstname
    return question(name_message).reprompt(name_message_reprompt)


@ask.intent("SurveyIntent")
def start_survey():

    dialog_state = get_dialog_state()

    if dialog_state == "STARTED":
        session.attributes["COUNT"] = 0
        session.attributes["BONUS_COUNT"] = 0
        session.attributes["SCORE"] = 0
        # session.attributes["QUESTION"] = 'BonusOne'
        session.attributes["QUESTION"] = 'One'
        return delegate()
    elif dialog_state != "COMPLETED":

        # If do not want to continue survey:
        if request["intent"]["slots"]["StartSurvey"]["value"] == 'no':
            return stop()

        survey_question = session.attributes["QUESTION"]

        ## If regular survey questions
        if not re.match("Bonus", survey_question):
            if 'value' in request["intent"]["slots"][survey_question]:
                session.attributes["SCORE"] += int(request["intent"]["slots"][survey_question]["value"])

                if request["intent"]["slots"][survey_question]["value"] not in ('0', '1', '2', '3', '4'):
                    reprompt_answer = render_template("reprompt_survey")
                    return elicit_slot(survey_question, reprompt_answer)
        else:


            survey_wait = survey_question + "Wait"
            bonus_wait = request["intent"]["slots"][survey_wait]

            if 'value' in bonus_wait:
                if request["intent"]["slots"][survey_wait]["value"] == 'no':
                    if session.attributes["BONUS_COUNT"] > 0:
                        session.attributes["BONUS_COUNT"] -= 1
                    bonus_question = render_template(survey_wait)
                    return elicit_slot(survey_wait, bonus_question)

            if 'value' in request["intent"]["slots"][survey_question]:
                words = request["intent"]["slots"][survey_question]["value"]
                analysis = TextBlob(words)

                ## Increase score based on negative sentiment analysis of words in bonus section
                if analysis.sentiment.polarity < 0:
                    session.attributes["SCORE"] += (2 / 3) * (-analysis.sentiment.polarity)
                #word_list.append(words)

        if session.attributes["COUNT"] < 16:

            session.attributes["COUNT"] += 1
            survey_question = num2words(session.attributes["COUNT"]).capitalize()
        elif session.attributes["BONUS_COUNT"] < 3:
            session.attributes["BONUS_COUNT"] += 1
            survey_question = "Bonus" + num2words(session.attributes["BONUS_COUNT"]).capitalize()


        #session.attributes["SCORE"] += int(request["intent"]["slots"][session.attributes["QUESTION"]]["value"])
        session.attributes["QUESTION"] = survey_question

        return delegate()

    score = round(float(session.attributes["SCORE"]), 2)

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
        # Severe Depression
        score_message = render_template('severe', score=score)

    elif score > 22:
        # Very Severe Depression
        score_message = render_template('very_severe', score=score)

    else:
        score_message = 'I was unable to calculate your Hamilton survey score. Sorry.'

    # dynamodb = boto3.resource('dynamodb')
    # table = dynamodb.Table('databaseTableName')

    #session.attributes[WORDS] = word_list
    #session.attributes[SESSION_SCORE] = score
    return question(score_message)

    #firstname =  session.attributes[SESSION_FIRSTNAME]
    #end_msg = "Hello %s ." % firstname
    #eturn statement(end_msg + "This is the survey intent.")


@ask.intent("TalkToIntent")
def talk_to_someone():
    #if firstname is None:
    #    return get_name()
    firstname = session.attributes[SESSION_FIRSTNAME]
    end_msg = "Hello %s ." % firstname
    return statement(end_msg + "This is the talk to intent.")



#@ask.intent('BonusConfirmation')
#def confirm(survey_question):
#    return start_survey()


#@ask.intent('AMAZON.RepeatIntent')
#def repeat(question):
    ## Do some processing to figure out what question needs to be repeated
#    prompt = "I did not quite get that. Can you please repeat your answer?"
#    return elicit_slot(question, prompt)


@ask.intent('AMAZON.HelpIntent')
def help():
    help_text = render_template('help')
    return question(help_text)


@ask.intent('AMAZON.StopIntent')
def stop():
    #firstname = session.attributes[SESSION_FIRSTNAME]
    bye_message = render_template("bye")
    return statement(bye_message)


@ask.session_ended
def session_ended():
    return "{}", 200

def elicit():
    pass

# def create_question_list():
#     LIST_OF_QUESTIONS = (num2words(x).title() for x in range(1, 4))
#     return LIST_OF_QUESTIONS

def get_dialog_state():
    return session['dialogState']


if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)
