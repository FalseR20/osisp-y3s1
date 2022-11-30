from flask import Flask
from flask_restful import Api

from .resources import DataResource

app = Flask(__name__)
api = Api(app)
api.add_resource(DataResource, "/")

if __name__ == "__main__":
    app.run(debug=True)
