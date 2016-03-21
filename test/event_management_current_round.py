from bson import ObjectId
from tornado.testing import gen_test
from test.base import TestBaseHandler


class CurrentRoundTestHandler(TestBaseHandler):

    @gen_test
    def test_get_current_round_valid_request(self):
        db = self.get_db_client().udaan
        current_round = 0
        event = dict(
            eventName="dummyEvent",
            currentRound=current_round
        )

        event_id = yield db.events.insert(event)
        str_event_id = str(event_id)
        expected_response = dict(
            code=200,
            body=dict(
                status=200,
                message=str(current_round)
            )
        )
        yield self.check("/api/event_management/current_round", method="GET",
                         headers=dict(Authorization=str_event_id), expected_response=expected_response)
        current_round += 1
        expected_response["body"]["message"] = str(current_round)
        yield db.events.update({"_id": event_id}, {"$inc": {"currentRound": 1}})
        yield self.check("/api/event_management/current_round", method="GET",
                         headers=dict(Authorization=str_event_id), expected_response=expected_response)
        yield db.events.remove({"_id": event_id})

    @gen_test
    def test_get_current_round_invalid_request(self):
        expected_response = dict(
            code=200,
            body=dict(
                status=403,
                message="Forbidden"
            )
        )
        yield self.check("/api/event_management/current_round", method="GET",
                         headers=None, expected_response=expected_response)

        expected_response["body"]["status"] = 401
        expected_response["body"]["message"] = "Invalid Token"
        yield self.check("/api/event_management/current_round", method="GET",
                         headers=dict(Authorization=ObjectId().__str__()),
                         expected_response=expected_response)
