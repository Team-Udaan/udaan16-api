from cerberus import cerberus

SCHEMA = {
    "teams": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "_id": {
                    "type": "string",
                    "required": True
                },
                "mobileNumber": {
                    "type": "integer",
                    "required": True
                },
                "receiptId": {
                    "type": "string"
                },
                "names": {
                    "type": "string"
                }
            }
        }
    },
    "date": {
        "type": "string",
        "required": True
    },
    "time": {
        "type": "string",
        "required": True
    },
    "venue": {
        "type": "string",
        "required": True
    },
    "test": {
        "type": "boolean",
    }
}


def validator(data):

    """This method will be called to validate the format of the request sent to the api, if an unappropriate request
    comes then a error message with missing details is sent as response."""

    request_validator = cerberus.Validator(SCHEMA)
    if request_validator.validate(data):
        return True
    else:
        return request_validator.errors
