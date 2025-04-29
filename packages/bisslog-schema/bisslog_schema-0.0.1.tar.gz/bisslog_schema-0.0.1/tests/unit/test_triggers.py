import pytest
from bisslog_schema.trigger_info import (
    TriggerInfo,
    TriggerHttp,
    TriggerWebsocket,
    TriggerConsumer,
    TriggerSchedule,
    TriggerEnum
)

def test_trigger_http_from_dict():
    data = {"method": "GET", "authenticator": None, "route": "/test", "apigw": "my-api"}
    trigger_http = TriggerHttp.from_dict(data)
    assert trigger_http.method == "GET"
    assert trigger_http.authenticator is None
    assert trigger_http.route == "/test"
    assert trigger_http.apigw == "my-api"

def test_trigger_websocket_from_dict():
    data = {"routeKey": "sendMessage"}
    trigger_ws = TriggerWebsocket.from_dict(data)
    assert trigger_ws.route_key == "sendMessage"

def test_trigger_consumer_from_dict():
    data = {"queue": "my-queue", "partition": "0"}
    trigger_consumer = TriggerConsumer.from_dict(data)
    assert trigger_consumer.queue == "my-queue"
    assert trigger_consumer.partition == "0"

def test_trigger_schedule_from_dict():
    data = {"cronjob": "0 12 * * *"}
    trigger_schedule = TriggerSchedule.from_dict(data)
    assert trigger_schedule.cronjob == "0 12 * * *"

def test_trigger_enum_from_str_valid():
    assert TriggerEnum.from_str("http") == TriggerEnum.HTTP
    assert TriggerEnum.from_str("websocket") == TriggerEnum.WEBSOCKET
    assert TriggerEnum.from_str("consumer") == TriggerEnum.CONSUMER
    assert TriggerEnum.from_str("schedule") == TriggerEnum.SCHEDULE

def test_trigger_enum_from_str_invalid():
    with pytest.raises(ValueError, match="Unknown trigger type: invalid"):
        TriggerEnum.from_str("invalid")

def test_trigger_from_dict_http():
    data = {
        "type": "http",
        "options": {
            "method": "POST",
            "authenticator": "token",
            "route": "/submit",
            "apigw": "api-123"
        }
    }
    trigger = TriggerInfo.from_dict(data.copy())
    assert trigger.type == TriggerEnum.HTTP
    assert isinstance(trigger.options, TriggerHttp)
    assert trigger.options.method == "POST"
    assert trigger.options.authenticator == "token"
    assert trigger.options.route == "/submit"
    assert trigger.options.apigw == "api-123"

def test_trigger_from_dict_missing_type_defaults_to_http():
    data = {
        "method": "GET",
        "authenticator": "none",
        "route": "/",
        "apigw": "api"
    }
    trigger = TriggerInfo.from_dict(data.copy())
    assert trigger.type == TriggerEnum.HTTP
    assert isinstance(trigger.options, TriggerHttp)

def test_trigger_from_dict_invalid_type():
    data = {
        "type": "invalid",
        "foo": "bar"
    }
    with pytest.raises(ValueError, match="Unknown trigger type: invalid"):
        TriggerInfo.from_dict(data.copy())

def test_trigger_from_dict_null():
    data = {
        "type": None,
    }
    with pytest.raises(ValueError, match="Trigger 'type' is required"):
        TriggerInfo.from_dict(data.copy())

