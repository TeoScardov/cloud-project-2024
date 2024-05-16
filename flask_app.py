#create a flask app that returns a json response
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins="*")  # Enable CORS for all routes

@app.route('/')
def hello_world():
    
    #wait for 5 seconds
    import time
    time.sleep(2)

    return jsonify({
        "books": [
            { "name": "The Alchemist", "price": 9.99 },
            { "name": "The Prophet", "price": 7.99 },
            { "name": "The Little Prince", "price": 6.99 }
        ]
    })

if __name__ == '__main__':
    app.run(port=9999 ,debug=True)
