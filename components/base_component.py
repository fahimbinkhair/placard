import boto3


class BaseComponent:
    _db = None

    def __init__(self):
        if not BaseComponent._db:
            BaseComponent._db = boto3.resource('dynamodb')
