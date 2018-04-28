# !/usr/bin/env python
# -*- coding: utf-8 -*-


launch_body = {
    "request": {
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:52:14Z",
        "type": "LaunchRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": True,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

sess_end_body = {
    "request": {
        "type": "SessionEndedRequest"
    },
    "version": "1.0"
}

stop_body = {
    "request": {
        "intent": {
            "name": "AMAZON.StopIntent"
        },
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

help_body = {
    "request": {
        "intent": {
            "name": "AMAZON.HelpIntent"
        },
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

suicide_hotline_body = {
    "request": {
        "intent": {
            "name": "SuicideHotLine"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

get_quote_type_completed_body = {
    "request": {
        "dialogState": "COMPLETED",
        "intent": {
          "confirmationStatus": "NONE",
          "name": "GetQuoteTypeIntent",
          "slots": {
            "Category": {
              "confirmationStatus": "NONE",
              "name": "Category",
              "value": "love"
            }
          }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": True,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}
name_intent_body ={
    "request": {
        "intent": {
            "name": "NameIntent",
            "slots": {
                "FirstName": {
                    "name": "FirstName",
                    "value": "Kevin"
                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

recommend_therapist_body = {
    "request": {
        "intent": {
            "name": "RecommendTherapist"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": "True",
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0",
    "context": {
        "System": {
          "application": {
            "applicationId": "fake-application-id"
          },
          "user": {
              "permissions": {
                  "consentToken": "FAKE_CONSENT_TEST_TOKEN"
              },
            "userId": "amzn1.account.AM3B00000000000000000000000"
          },
            "device": {
            "deviceId": "amzn1.ask.device",
            "supportedInterfaces": {
                "AudioPlayer": {},
                "Display": {
                    "markupVersion": "1.0",
                    "templateVersion": "1.0"
                    }
                }
            },
        }
    }
}

give_quote_body = {
    "request": {
        "intent": {
            "name": "QuoteIntent",
            "slots": {
                "Category": {
                    "name": "category",
                    "value": "inspirational"
                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

give_advice_body = {
    "request": {
        "intent": {
            "name": "GiveAdvice"
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T22:45:12Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "new": "True",
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}

take_survey_body = {
    "context": {
        "device": {
            "deviceId": "amzn1.ask.device"
            },
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "request": {
        "dialogState": "COMPLETED",
        "intent": {
            "confirmationStatus": "NONE",
            "name": "SurveyIntent",
            "slots": {
                "BonusOne": {
                    "name": "BonusOne",
                    "value": "happy great awesome"
                },
                "BonusOneWait": {
                    "name": "BonusOneWait",
                    "value": "yes"
                },
                "BonusThree": {
                    "name": "BonusThree",
                    "value": "confident happy content"
                },
                "BonusThreeWait": {
                    "name": "BonusThreeWait",
                    "value": "yes"
                },
                "BonusTwo": {
                    "name": "BonusTwo",
                    "value": "stressful busy hard"
                },
                "BonusTwoWait": {
                    "name": "BonusTwoWait",
                    "value": "yes"
                },
                "Eight": {
                    "name": "Eight",
                    "value": "0"
                },
                "Eleven": {
                    "name": "Eleven",
                    "value": "0"
                },
                "Fifteen": {
                    "name": "Fifteen",
                    "value": "1"
                },
                "Five": {
                    "name": "Five",
                    "value": "1"
                },
                "Four": {
                    "name": "Four",
                    "value": "0"
                },
                "Fourteen": {
                    "name": "Fourteen",
                    "value": "0"
                },
                "Nine": {
                    "name": "Nine",
                    "value": "1"
                },
                "One": {
                    "name": "One",
                    "value": "0"
                },
                "Seven": {
                    "name": "Seven",
                    "value": "2"
                },
                "Six": {
                    "name": "Six",
                    "value": "0"
                },
                "Sixteen": {
                    "name": "Sixteen",
                    "value": "2"
                },
                "StartSurvey": {
                    "name": "StartSurvey",
                    "value": "yes"
                },
                "Ten": {
                    "name": "Ten",
                    "value": "2"
                },
                "Thirteen": {
                    "name": "Thirteen",
                    "value": "0"
                },
                "Three": {
                    "name": "Three",
                    "value": "0"
                },
                "Twelve": {
                    "name": "Twelve",
                    "value": "0"
                },
                "Two": {
                    "name": "Two",
                    "value": "0"
                }
            }
        },
        "locale": "en-US",
        "requestId": "amzn1.echo-api.request",
        "timestamp": "2018-04-26T05:14:05Z",
        "type": "IntentRequest"
    },
    "session": {
        "application": {
            "applicationId": "amzn1.ask.skill"
        },
        "attributes": {
                "BONUS_COUNT": 3,
                "BonusOne": "happy great awesome",
                "BonusTwo": "stressful busy hard",
                "COUNT": 16,
                "Eight": 0,
                "Eleven": 0,
                "Fifteen": 1,
                "Five": 1,
                "Four": 0,
                "Fourteen": 0,
                "HAMD_SCORE": 9,
                "Nine": 1,
                "One": 0,
                "PREV_QUESTION": "BonusTwo",
                "QUESTION": "BonusThree",
                "STATE": "Survey",
                "Seven": 2,
                "Six": 0,
                "Sixteen": 2,
                "Ten": 2,
                "Thirteen": 0,
                "Three": 0,
                "Twelve": 0,
                "Two": 0
            },
        "new": False,
        "sessionId": "amzn1.echo-api.session",
        "user": {
            "userId": "amzn1.ask.account"
        }
    },
    "version": "1.0"
}
