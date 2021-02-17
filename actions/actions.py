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


airport_dict = {
        'San Fransisco' : 'SFO-sky',
        'Chicago' : 'ORD-sky',
        'New York' : 'JFK-sky',
        'Stockholm' : 'ARN-sky',
        'Keflavik' : 'KEF-sky',
        'Copenhagen' : 'CPH-sky',
        'Boston' : 'BOS-sky',
    }


class ActionGetFlightInfo(Action):
    
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
    
    def name(self) -> Text:
        return "action_get_flight_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            location_from = airport_dict[tracker.get_slot("location_from")]
        except:
            location_from = 'KEF-sky'
            
        try:
            location_to = airport_dict[tracker.get_slot("location_to")]
        except:
            location_to = 'CPH-sky'
            
        date = '2021-02-19'
        
        response = get_flights(location_from, location_to, date)
        
        min_price = response['Quotes'][0]['MinPrice'] + ' ISK'
        carrier = response['Carriers'][0]['Name']
        from_iata = response['Places'][1]['IataCode']
        to_iata = response['Places'][0]['IataCode']
        
        # flights = "Airport 1, Airport 2, Price: 125 USD, Departure time: 11:20 AM, Arrival time: 2:10 PM."
        dispatcher.utter_message("Here are flights from {} to {} on {} with {} for {}".format(from_iata, to_iata, date, carrier, min_price))

        # return [SlotSet("address", address)]
    
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
    
    '''
    