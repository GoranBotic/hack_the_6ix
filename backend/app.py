from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from textblob import TextBlob
import unicodedata

import speech_recognition as sr

import sys

from flask_cors import CORS

from io import BytesIO

import base64
from google.cloud import speech_v1p1beta1 as speech


app = Flask(__name__)
CORS(app)

client = speech.SpeechClient()

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
    
    try:
        text= response.results[-1].alternatives[0].transcript 
        return text 
    except Exception as e:
        return "" 

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
    return text


def getSentiment(text): 
    blob = TextBlob(str(unicodedata.normalize('NFKD', text).encode('ascii','ignore').lower()))
    return blob

r = sr.Recognizer()
def STT(audio):
    
    text = ""
    with sr.AudioFile(audio) as fl:
        aud = r.record(fl)

    
        try:
            text = r.recognize_sphinx(aud)
            #print(text, file=sys.stderr)
        except Exception as e:
            print(e,file=sys.stderr)
            return ""

        return text 
    
    return ""



#class Analyze(Resource):
@app.route("/api/v1/analyze", methods=['POST','PUT'])
def analyze():
    text = ""
    #print("//////",file=sys.stderr)
    #print(request,file=sys.stderr)
    #print(request.form,file=sys.stderr)
    #print(request.files,file=sys.stderr)
    
    if 'audio' in request.files:   
        print(request.files,file=sys.stderr)
        with sr.AudioFile(request.files['audio']) as fl:
        	text = getSpeakers(fl)
    elif 'audio' in request.form:
        #print("saw audio", file=sys.stderr)
        #print(bytes(base64.b64decode(request.form['audio'])),file=sys.stderr)
        #text = STT(BytesIO(bytes(base64.b64decode(request.form['audio']))))
        
        #text = STT(BytesIO(bytes(base64.b64decode(request.form['audio'] + '=' * (-len(request.form['audio']) % 4)))))
        
        theBytes = BytesIO(bytes(base64.b64decode(request.form['audio'] + '=' * (-len(request.form['audio']) % 4))))
        
        with sr.AudioFile(theBytes) as fl: 
            text = getSpeakers(fl)
        if len(text) > 0:
            print(text,file=sys.stderr)
    elif 'text' in request.form:
        text = request.form['text']
    else:
        return "Invalid Request", 400
        
    sentiment = getSentiment(text)

    resp = '{ "sentiment": { "polarity": %s, "subjectivity": %s , "text": "%s" }, ' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity, text)

    

    if 'aggregate' in request.form:
        
        polarity = str(((23.0/24.0)*float(request.form["aggregate"]["polarity"])) + ((1.0/24.0)*float(sentiment.sentiment.polarity)))
        subjectivity = str(((23.0/24.0)*float(request.form["aggregate"]["subjectivity"])) + ((1.0/24.0)*float(sentiment.sentiment.subjectivity)))
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s} }' % (polarity, subjectivity)
        resp += aggregate
    else:
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s} }' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity)
        resp += aggregate

    
    jsonData = resp

    return jsonData, 200
        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=False)
