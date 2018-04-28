import utopia
from utopia import app
import unittest
import json
import os
import tests.request_json as request_json
from flask import current_app
from mock import patch


class TestUtopiaApp(unittest.TestCase):

    def setUp(self):
        '''Test Suite set up by disabling ASK_VERIFY_REQUESTS and enabling testing to true'''
        app.config['ASK_VERIFY_REQUESTS'] = False
        app.config['SECRET_KEY'] = 'SUPERSECRETKEYBUTNOTREALLY!'
        app.config['TESTING'] = True
        # self.app_context = app.app_context()
        self.app = app.test_client()
        self.app.testing = True

        # with open('request_body.json', 'rb') as f:
        #     self.request_json = json.load(f)
        os.chdir(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    def tearDown(self):
        os.chdir(os.path.dirname(__file__))
        """ Test Suite Tear down."""
        pass

    def test_utopia_launch(self):
        """Test Launch Intent."""
        response = self.app.post('/', data=json.dumps(request_json.launch_body))
        self.assertEqual(200, response.status_code)
        self.assertTrue(b'Welcome to Utopia!' in response.data)

    def test_utopia_session_ended(self):
        """Test Session End."""
        response = self.app.post('/', data=json.dumps(request_json.sess_end_body))
        self.assertEqual(200, response.status_code)

    def test_name_intent(self):
        """Test NameIntent"""
        response = self.app.post('/', data=json.dumps(request_json.name_intent_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('Kevin', data['sessionAttributes']['firstname'])

    def test_get_brainy_quotes(self):
        """Testing helper function get_brainy_quotes"""
        zip_quotes = utopia.get_brainy_quotes(category='positive', number_of_quotes=50)
        quotes = list(zip_quotes)
        self.assertIsNotNone(quotes)
        self.assertNotEqual(len(quotes), 0)

    def test_suicide_hotline_intent(self):
        """Test SuicideHotLine Intent."""
        response = self.app.post('/', data=json.dumps(request_json.suicide_hotline_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))

        self.assertTrue('Thank you for being honest with me. Please don\'t hurt yourself or anyone else.' in
                        data['response']['outputSpeech']['text'])

    def test_recommend_therapist_intent_no_address_provided(self):
        """Test RecommendTherapist Intent"""
        response = self.app.post('/', data=json.dumps(request_json.recommend_therapist_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('AskForPermissionsConsent', data['response']['card']['type'])
        self.assertEqual('read::alexa:device:all:address', data['response']['card']['permissions'][0])

    @patch('utopia.get_location')
    def test_recommend_therapist_intent_address_mocked(self, mock_get_location):
        mock_get_location.return_value = '3007 Sycamore Street San Jose, California 95129'
        response = self.app.post('/', data=json.dumps(request_json.recommend_therapist_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('I\'ve found a nearby therapist that you can talk to', data['response']['card']['title'])
        self.assertTrue('I\'ve found a therapist near you.' in data['response']['outputSpeech']['text'])
        self.assertEqual('RecommendTherapist', data['sessionAttributes']['STATE'])

    def test_survey_intent_completed_mild_severity(self):
        """Test SurveyIntent"""
        response = self.app.post('/', data=json.dumps(request_json.take_survey_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(9.04, data['sessionAttributes']['HAMD_SCORE'])
        self.assertEqual('SurveyDone', data['sessionAttributes']['STATE'])
        self.assertEqual('Mild', data['sessionAttributes']['Severity'])

    # def test_survey_intent_completed_normal_severity(self):
    #     """Test SurveyIntent"""
    #     # original_survey_body = request_json.take_survey_body
    #     new_survey_body = request_json.take_survey_body
    #     for x in new_survey_body['request']['intent']['slots']:
    #         if isinstance(new_survey_body['request']['intent']['slots'][x]['value'], int):
    #             new_survey_body['request']['intent']['slots'][x]['value'] = 0
    #     for y in new_survey_body['session']['attributes']:
    #         if y.lower()
    #     response = self.app.post('/', data=json.dumps(request_json.take_survey_body))
    #     self.assertEqual(200, response.status_code)
    #     data = json.loads(response.data.decode('utf-8'))
    #     self.assertEqual(9.04, data['sessionAttributes']['HAMD_SCORE'])
    #     self.assertEqual('SurveyDone', data['sessionAttributes']['STATE'])
    #     self.assertEqual('Mild', data['sessionAttributes']['Severity'])


    def test_get_quote_type_intent(self):
        """Test GetQuoteTypeIntent."""
        response = self.app.post('/', data=json.dumps(request_json.get_quote_type_completed_body))
        self.assertEqual(200, response.status_code)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual('love', data['sessionAttributes']['Category'])

    def test_give_quote_intent(self):
        """Test QuoteIntent."""
        response = self.app.post('/', data=json.dumps(request_json.give_quote_body))
        self.assertEqual(200, response.status_code)

    def test_give_advice_intent(self):
        """Test QuoteIntent."""
        response = self.app.post('/', data=json.dumps(request_json.give_advice_body))
        self.assertEqual(200, response.status_code)

    def test_stop_intent(self):
        """Test Stop Intent."""
        response = self.app.post('/', data=json.dumps(request_json.stop_body))
        self.assertEqual(200, response.status_code)

    def test_help_intent(self):
        """Test Help Intent."""
        response = self.app.post('/', data=json.dumps(request_json.help_body))
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
