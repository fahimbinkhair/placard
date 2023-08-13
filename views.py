import json


def json_view(status_code: int = 200, message: str = '', data: dict = None) -> dict:
    if data is None:
        data = {}

    return_val = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            'message': message,
            'data': data
        })
    }

    print(return_val)
    return return_val
