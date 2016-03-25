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
    request_validator = cerberus.Validator(SCHEMA)
    if request_validator.validate(data):
        return True
    else:
        return request_validator.errors
