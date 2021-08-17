import sys
from recognize import recognizeAudio 
from classify import classifyAudio
from flask import Flask
from flask_restful import Api, Resource, reqparse


import random
app = Flask(__name__)

api = Api(app)

recognized_audios = [
    {
        "id": 0,
        "filepath": "/Desktop/file1.wav",
        "recognition": "hello world"
    }
]

classified_audios = [
    {
        "id":0,
        "filepath": "Desktop/file.2wav",
        "classification": "Affirmative"
    }
]

class RecognizedAudios(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(recognized_audios), 200
        for audio in recognized_audios:
            if(audio["id"] == id):
                return audio, 200
        return "Audio not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("filepath")
        params = parser.parse_args()
        for audio in recognized_audios:
            if(id == audio["id"]):
                return f"Audio with id {id} already exists", 400

        audio = {
            "id": int(id),
            "filepath": params["filepath"],
            "recognition": recognizeAudio(params["filepath"])
        }
        recognized_audios.append(audio)
    
        return audio, 201

    def put(self, id):

        print(recognized_audios)

        parser = reqparse.RequestParser()
        parser.add_argument("filepath")
        
        params = parser.parse_args()
        for audio in recognized_audios:
            if(id == audio["id"]):
                audio["filepath"] = params["filepath"]
                audio["recognition"] = recognizeAudio(params["filepath"])
                return audio, 200
             
        audio = {
            "id": id,
            "filepath": params["filepath"],
            "recognition": recognizeAudio(params["filepath"])
        }
      
        recognized_audios.append(audio)
        
        return audio, 201

    def delete(self, id):
        global recognized_audios
        recognized_audios= [audio for audio in recognized_audios if audio["id"] != id]
        return f"Audio with id {id} is deleted.", 200

class ClassifiedAudios(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(classified_audios), 200
        for audio2 in classified_audios:
            if(audio2["id"] == id):
                return audio2, 200
        return "Audio not found", 404

    def post(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("filepath")
        params = parser.parse_args()
        for audio2 in classified_audios:
            if(id == audio2["id"]):
                return f"Audio with id {id} already exists", 400

               
        audio2 = {
            "id": int(id),
            "filepath": params["filepath"],
            "classification": classifyAudio(params["filepath"])
        }
        classified_audios.append(audio2)
        return audio2, 201

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("filepath")
        params = parser.parse_args()
        for audio2 in classified_audios:
            if(id == audio2["id"]):
                audio2["filepath"] = params["filepath"]
                audio2["classification"] = classifyAudio(params["filepath"])
                return audio2, 200
      
        audio2 = {
            "id": id,
            "filepath": params["filepath"],
            "classification": classifyAudio(params["filepath"])
        }
      
        classified_audios.append(audio2)
        return audio2, 201

    def delete(self, id):
        global classified_audios
        classified_audios= [audio2 for audio2 in classified_audios if audio2["id"] != id]
        return f"Audio with id {id} is deleted.", 200

api.add_resource(RecognizedAudios, "/recognized-audios", "/recognized-audios/", "/recognized-audios/<int:id>")
api.add_resource(ClassifiedAudios, "/classified-audios", "/classified-audios/", "/classified-audios/<int:id>")
if __name__ == '__main__':
    app.run(debug=True)