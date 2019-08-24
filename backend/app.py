from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from textblob import TextBlob
import unicodedata

import speech_recognition as sr

import sys

from flask_cors import CORS


from google.cloud import speech_v1p1beta1 as speech

import hashlib

import time

from copy import deepcopy

client = speech.SpeechClient()

app = Flask(__name__)
CORS(app)


activeIDs = dict() 
#(audio, annotatedText, time)

def getSpeakers(fl):
    content = fl

    audio = speech.types.RecognitionAudio(content=content.stream.read())

    config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=2)

    #print('Waiting for operation to complete...', file=sys.stderr)
    response = client.recognize(config, audio)

    print(response, file=sys.stderr)

    #print(response.results, file=sys.stderr)

    text= response.results[-1].alternatives[0].transcript 
    #print(text, file=sys.stderr)

    newList = []
    for word in response.results[-1].alternatives[0].words:
        newList.append(((float(word.end_time.nanos)/1000000000.0) + word.end_time.seconds, word.speaker_tag, word.word)) 

    newList.sort()

    annotatedText = "@"+str(word.speaker_tag) + " " 
    oldSpeaker = word.speaker_tag
    numSpeakers = 0
    for x in newList:
        if int(x[1]) > numSpeakers:
            numSpeakers = int(x[1])
        newSpeaker = x[1]
        if oldSpeaker != newSpeaker:
            oldSpeaker = newSpeaker
            twoSpeakers=True
            annotatedText += " @" + str(oldSpeaker)

        annotatedText += str(x[2]) + " " 


    #print(annotatedText, file=sys.stderr)
    return text, annotatedText, numSpeakers

#local sentiment analysis
def getSentiment(text): 
    blob = TextBlob(str(unicodedata.normalize('NFKD', text).encode('ascii','ignore').lower()))
    return blob

#local speech to text 
r = sr.Recognizer()
def STT(audio):
    
    text = ""
    with sr.AudioFile(audio.stream) as fl:

        aud = r.record(fl)

    
        try:
            text = r.recognize_sphinx(aud)
            #print(text, file=sys.stderr)
        except Exception as e:
            print(e,file=sys.stderr)
            return ""

        return text 
    
    return ""

#The main function
@app.route("/api/v1/analyze", methods=['POST','PUT'])
def analyze():

    ID = None 
    if "identifier" in request.form:
        ID = str(request.form["identifier"]) 

    print(ID, file=sys.stderr)
             
    text = ""
    if 'audio' in request.files:
        if ID != None and ID in activeIDs and activeIDs[ID][0] != None:
            with sr.AudioFile(request.files['audio'].stream) as fl1:
                with sr.AudioFile(activeIDs[ID][0]) as fl2:
                    fullFl = fl1 + fl2
                    text,annotatedText,numSpeakers = getSpeakers(fullFl)

                    lst1 = annotatedText.split(" ") 
                    lst2 = activeIDs[ID][1]
                    for x in lst2:
                        del lst1[0] 

                    annotatedText = ""
                    for x in lst2:
                        annotatedText += x + " "
        elif ID == None or ID not in activeIDs:
            with sr.AudioFile(request.files['audio'].stream) as fl1:
                text,annotatedText,numSpeakers = getSpeakers(fl1)
                strThing = text + str(time.time())
                ID = str(hashlib.md5(strThing.encode('utf-8')).hexdigest())
                activeIDs[ID] = (None, None, None) 
                if numSpeakers > 0:
                    activeIDs[ID] = (request.files['audio'].stream, annotatedText, time.time())

        else:
            with sr.AudioFile(request.files['audio'].stream) as fl1:
                text,annotatedText,numSpeakers = getSpeakers(fl1)
                if numSpeakers > 0:
                    activeIDs[ID] = (request.files['audio'].stream, annotatedText, time.time())
    
    elif 'text' in request.form:
        text = request.form['text']
    else:
        return "Invalid Request", 400

    
        
    sentiment = getSentiment(text)

    resp = '{ "sentiment": { "polarity": %s, "subjectivity": %s , "noun_phrases": %s, "text": "%s" }, ' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity, sentiment.noun_phrases, annotatedText)

    

    if 'aggregate' in request.form:
        
        polarity = str(((23.0/24.0)*float(request.form["aggregate"]["polarity"])) + ((1.0/24.0)*float(sentiment.sentiment.polarity)))
        subjectivity = str(((23.0/24.0)*float(request.form["aggregate"]["subjectivity"])) + ((1.0/24.0)*float(sentiment.sentiment.subjectivity)))
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s} }' % (polarity, subjectivity)
        resp += aggregate
    else:
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s}, ' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity)
        resp += aggregate
         
    resp += '"identifier": ' + str(ID) + "}"
    return resp, 200
        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=False)