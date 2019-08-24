from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from textblob import TextBlob
import unicodedata

import speech_recognition as sr

import sys

from flask_cors import CORS

from google.cloud import speech_v1 as speech
client = speech.SpeechClient()

app = Flask(__name__)
CORS(app)

#TODO: transcript 
#TODO: highlight keywords in transcript
#return sentiment for the chunk as well as the overall analysis object 

def getSpeakers(content):
    audio = speech.types.RecognitionAudio(content=content)

    config = speech.types.RecognitionConfig(
    encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=8000,
    language_code='en-US',
    enable_speaker_diarization=True,
    diarization_speaker_count=2)

    print('Waiting for operation to complete...', file=sys.stderr)
    response = client.recognize(config, audio)

    print(result, file=sys.stderr)

def getSentiment(text): 
    blob = TextBlob(str(unicodedata.normalize('NFKD', text).encode('ascii','ignore').lower()))
    return blob

r = sr.Recognizer()
def STT(audio):
    
    text = ""
    with sr.AudioFile(audio.stream) as fl:

        getSpeakers(fl) 

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
    if 'audio' in request.files:
        text = STT(request.files['audio'])
    elif 'text' in request.form:
        text = request.form['text']
    else:
        return "Invalid Request", 400
        
    sentiment = getSentiment(text)

    resp = '{ "sentinment": { "polarity": %s, "subjectivity": %s , "noun_phrases": %s, "text": "%s" }, ' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity, sentiment.noun_phrases, text)

    

    if 'aggregate' in request.form:
        
        polarity = str(((23.0/24.0)*float(request.form["aggregate"]["polarity"])) + ((1.0/24.0)*float(sentiment.sentiment.polarity)))
        subjectivity = str(((23.0/24.0)*float(request.form["aggregate"]["subjectivity"])) + ((1.0/24.0)*float(sentiment.sentiment.subjectivity)))
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s} }' % (polarity, subjectivity)
        resp += aggregate
    else:
        aggregate = ' "aggregate": {"polarity": %s, "subjectivity": %s} }' % (sentiment.sentiment.polarity, sentiment.sentiment.subjectivity)
        resp += aggregate

    return resp, 200
        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=False)