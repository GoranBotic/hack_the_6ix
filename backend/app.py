from datetime import datetime

from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from textblob import TextBlob
import unicodedata

import speech_recognition as sr

import sys

app = Flask(__name__)
#api = Api(app)

#TODO: transcript 
#TODO: highlight keywords in transcript
#return sentiment for the chunk as well as the overall analysis object 

def getSentiment(text): 
    blob = TextBlob(str(unicodedata.normalize('NFKD', text).encode('ascii','ignore').lower()))
    noun_phrases = blob.noun_phrases
    status = '{ "sentinment": { "polarity": %s, "subjectivity": %s , "noun_phrases": %s, "text": %s } }' % (blob.sentiment.polarity, blob.sentiment.subjectivity, noun_phrases, text)
    return status

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

#class Analyze(Resource):
@app.route("/api/v1/analyze", methods=['POST','PUT'])
def analyze():
    text = ""
    if 'audio' in request.files:
        text = STT(request.files['audio'])
    else:
        text = request.form['text']
        
    sentiment = getSentiment(text)

    return sentiment, 200
        
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4500, debug=True)