from os import environ
from purchaseApp import app

DEBUG = environ.get("DEBUG", "False").lower() == "true"

if __name__ == '__main__':
    app.run(debug=DEBUG)