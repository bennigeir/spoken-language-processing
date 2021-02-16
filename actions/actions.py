# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

import requests


class ActionGetFlightInfo(Action):
    
    '''
    TODO:
        Figure out how to return responses
        Use variables for queries    
    '''

    def list_airports(query):
        
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/US/ISK/is-IS/"
        
        querystring = {"query":query}
        
        headers = {
            'x-rapidapi-key': "1d53092390msh872f0d518a7b979p184f2fjsna099fcd1dc2d",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
            }
        
        response = requests.request("GET", url, headers=headers, params=querystring)
    
        return response.json()['Places']
    
    
    def get_flights(origin_place, destination_place, outbound_partial_date, inbound_partial_date=''):
        
        url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/'
    
        data = {
            'country' : 'US',
            'currency' : 'ISK',
            'locale' : 'en-US',
            'origin_place' : origin_place, #'SFO-sky',
            'destination_place' : destination_place, #'JFK-sky',
            'outbound_partial_date' : outbound_partial_date, #'2021-02-05',
            'inbound_partial_date' : inbound_partial_date, #'',
        }
        
        tmp = [val for key, val in data.items() if len(val) > 0]
        
        url += '/'.join(tmp)
            
        headers = {
            'x-rapidapi-key': "1d53092390msh872f0d518a7b979p184f2fjsna099fcd1dc2d",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
            }
        
        response = requests.request("GET", url, headers=headers)
        
        return response.json()