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

app = Flask(__name__)
CORS(app)

#TODO: transcript 
#TODO: highlight keywords in transcript
#return sentiment for the chunk as well as the overall analysis object 

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

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)

#class Analyze(Resource):
@app.route("/api/v1/analyze", methods=['POST','PUT'])
def analyze():
    text = ""
    print("//////",file=sys.stderr)
    print(request,file=sys.stderr)
    print(request.form,file=sys.stderr)
    print(request.files,file=sys.stderr)
    
    if 'audio' in request.form:
        print("saw audio", file=sys.stderr)
        #print(bytes(base64.b64decode(request.form['audio'])),file=sys.stderr)
        #text = STT(BytesIO(bytes(base64.b64decode(request.form['audio']))))
        text = STT(BytesIO(bytes(decode_base64(request.form['audio']))))
        pass
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