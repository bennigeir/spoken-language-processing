# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
import requests

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet


airport_dict = {
    'san francisco' : 'SFO-sky',
    'chicago' : 'ORD-sky',
    'new york' : 'JFK-sky',
    'stockholm' : 'ARN-sky',
    'keflavik' : 'KEF-sky',
    'copenhagen' : 'CPH-sky',
    'boston' : 'BOS-sky',
}


def list_airports(query):
    
    url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/US/ISK/is-IS/"
    
    querystring = {"query":query}
    
    headers = {
        'x-rapidapi-key': "1d53092390msh872f0d518a7b979p184f2fjsna099fcd1dc2d",
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
        }
    
    try:
        response = requests.request("GET", url, headers=headers, params=querystring).json()['Places']
        
        response = [i['PlaceName'] for i in response]
    except:
        response = ''
        
    return response


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
    
    
class ActionGetAirportInfo(Action):  

    def name(self) -> Text:
        return "action_airport_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        try:
            location = next(tracker.get_latest_entity_values(entity_type='location'), None)
        except:
            location = 'Reykjavik'
            
        print(list_airports(location))
        response = ', '.join(list_airports(location))
        
        dispatcher.utter_message("Ég fann eftirfarandi flugvelli í {}: {}".format(location, str(response)))


class ActionGetFlightInfo(Action):
        
    '''def get_flights(self, origin_place, destination_place, outbound_partial_date, inbound_partial_date=''):
        
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
    
    
    def list_airports(self, query):
        
        url = "https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/US/ISK/is-IS/"
        
        querystring = {"query":query}
        
        headers = {
            'x-rapidapi-key': "1d53092390msh872f0d518a7b979p184f2fjsna099fcd1dc2d",
            'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com"
            }
        
        try:
            response = requests.request("GET", url, headers=headers, params=querystring).json()
        except:
            response = ''
            
        return response'''
    
    
    def name(self) -> Text:
        return "action_get_flight_info"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print('action_get_flight_info called !')
        print(next(item for item in tracker.latest_message['entities'] if item["entity"] == "from")['value'])
        print(next(item for item in tracker.latest_message['entities'] if item["entity"] == "to")['value'])
              
        try:
            location_from = airport_dict[(next(item for item in tracker.latest_message['entities'] if item["entity"] == "from")['value']).lower()]
            text_location_from = next(item for item in tracker.latest_message['entities'] if item["entity"] == "from")['value']
        except:
            location_from = 'KEF-sky'
            text_location_from = 'Keflavík'
        try:
            location_to = airport_dict[(next(item for item in tracker.latest_message['entities'] if item["entity"] == "to")['value']).lower()]
            text_location_to = next(item for item in tracker.latest_message['entities'] if item["entity"] == "to")['value']
        except:
            location_to = 'CPH-sky'
            text_location_to = 'Kaupmannahöfn'
            
        date = '2021-04-09'
        
        try:
            response = get_flights(location_from, location_to, date)
        
            min_price = str(response['Quotes'][0]['MinPrice']) + ' kr'
            carrier = str(response['Carriers'][0]['Name'])
            from_iata = str(response['Places'][0]['IataCode'])
            to_iata = str(response['Places'][1]['IataCode'])
            
            # flights = "Airport 1, Airport 2, Price: 125 USD, Departure time: 11:20 AM, Arrival time: 2:10 PM."
            #dispatcher.utter_message("Hér eru flug frá {} til {} á {} með {} fyrir {}".format(from_iata, to_iata, date, carrier, min_price))
            dispatcher.utter_message("Hér eru flug frá {} til {} þann {}, með {}, á {}".format(text_location_from, text_location_to, date, carrier, min_price))
        except:
            dispatcher.utter_message("Ég fann því miður engin flug frá {} til {} þann {}".format(text_location_from, text_location_to, date))

        # return [SlotSet("airline", carrier), SlotSet("airport_to", to_iata), SlotSet("airport_from", from_iata), SlotSet("cost_amount", min_price)]    