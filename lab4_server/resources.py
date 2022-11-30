from http import HTTPStatus

from flask import request
from flask_restful import Resource

from . import load_save


class DataResource(Resource):
    @staticmethod
    def get():
        return load_save.load_data_str()

    @staticmethod
    def post():
        load_save.save_data(request.data)
        return HTTPStatus.OK
