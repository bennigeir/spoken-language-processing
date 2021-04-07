import requests
import json
import boto3
import multiprocessing
import os
import requests
import wave
from base64 import b64encode

import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

from playsound import playsound


polly_client = boto3.Session(aws_access_key_id='AKIAZAAX7DNLBQDN6WGK',
                             aws_secret_access_key='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',
                             region_name='eu-west-2').client('polly')

# Token and endpoint for the API call
token = 'ak_Pa2KJXLmk8djBKmJLXM6D4ZGeoVQPE3q0Kw9p5RqvzOa7yl2gbWYA1rN04eyQBOG'
endpoint = 'https://tal.ru.is/v1/speech:syncrecognize'

sample_rate = 44100
fs = 44100

def record_speech():
    print ("Talk!")
    # fs = 44100  # Sample rate
    seconds = 5  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    write('input_from_user.wav', fs, myrecording)

    sound = "input_from_user.wav"

    # Open individual file, decode it as utf-8 and cast to base64
    obj = open(sound,'rb').read()
    obj64 = str(b64encode(obj).decode("utf-8"))
    
    # Get sample rate of WAV file
    # wave_obj = wave.open(sound,'r')
    # sample_rate = str(wave_obj.getframerate())
    
    # Define headers and data for the API call
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + token,
    }
    
    data = '{"config": {"encoding": "LINEAR16", "sampleRate": '\
            + str(sample_rate) + '}, "audio" : {"content": "' + obj64 + '"}}'
    
    # Make the API call
    response = requests.post(endpoint,
                            headers=headers,
                            data=data)
    
    res = response.text[44:-6]
    
    print("From user: {}".format(res))
    return res

def get_audio(text):

    response = polly_client.synthesize_speech(VoiceId='Dora',
                                              OutputFormat='mp3',
                                              Text=text)
    
    file = open('temp_rasa_speech.mp3', 'wb')
    file.write(response['AudioStream'].read())
    file.close()


def play_audio():
    
    p = multiprocessing.Process(target=playsound, args=("temp_rasa_speech.mp3",))
    p.start()
    input("press ENTER to stop playback")
    p.terminate()



conversation_id = input("Conversation ID: ")
url = f"http://localhost:5005/conversations/{conversation_id}/"
messages_url = url + "messages"
intents_url = url + "trigger_intent"

loop = True
while loop:
    
    message = record_speech()
    while message == '':
        print ("No speech detected!")
        message = record_speech()
    
    # message = input("Input: ") 
    if message.lower() in ['stop','stopp','hætta']:
        loop = False
        break
    
    message = message.replace('kaupmannahafnar','Copenhagen')
    message = message.replace('kaupmannahöfn','Copenhagen')
    
    message = message.replace('keflavík','Keflavik')
    message = message.replace('keflavíkur','Keflavik')
    
    message = message.replace('nýju jórvíkur','New York')
    message = message.replace('nýju jórvík','New York')
    
    message = message.replace('boston','Boston')
    
    payload = {
                "text": message,
                "sender": "user",
              }
    
    print('Altered message: {}'.format(message))
    
    messages_response = requests.post(messages_url, json=payload)
    messages_data = json.loads(messages_response.text)
    intent_name = messages_data['latest_message']['intent']['name']
    
    payload = {
               'name': intent_name,
              }
    
    entities = messages_data['latest_message']['entities']
    if len(entities) > 0:
        try:
            loc_from = entities[0]['value']
        except:
            loc_from = ''
        # payload['entities']['from'] = loc_from    
        
        try:
            loc_to = entities[1]['value']
        except:
            loc_to = ''
        # payload['entities']['to'] = loc_to            
        
        
        
        payload['entities'] = {'to': loc_to,
                               'from': loc_from}
        
        
    
    print('Intent: {}'.format(intent_name))
    print('Payload: {}'.format(payload))
    
    intents_response = requests.post(intents_url, json=payload)
    intents_data = json.loads(intents_response.text)
    text_to_speak = intents_data["messages"][0]["text"]
    print (text_to_speak)
    
    get_audio(text_to_speak)
    playsound('temp_rasa_speech.mp3')
    # play_audio()
    os.remove("temp_rasa_speech.mp3")
    
    if intent_name == 'goodbye':
        loop = False
        break

# %%


'''
Góðan daginn
Góðan dag
Halló

flugvellir í Stockholm

ég vil fljúga frá boston til new york

ég vil fljúga frá Boston til Chicago
ég vil fljúga frá Keflavik til Copenhagen
'''