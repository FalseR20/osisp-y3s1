from logging import getLogger

from flask import Response, request
from flask_restful import Resource

from . import load_save

logger = getLogger()


class DataResource(Resource):
    @staticmethod
    def post():
        data = request.data
        logger.debug("Save data: %s", data)
        load_save.save_data(data)
        return Response()

    @staticmethod
    def get():
        data = load_save.load_data()
        logger.debug("Load data: %s", data)
        return Response(data)
