from unittest import mock

import pytest

from bisslog_schema.enums.criticality_enum import CriticalityEnum
from bisslog_schema.read_metadata import read_service_metadata


def test_read_yml_webhook_example():
    service_data = read_service_metadata("./tests/examples/webhook.yml")
    assert service_data.type == "microservice"
    assert service_data.name == "webhook receiver"
    assert service_data.team == "code-infrastructure"


    assert service_data.use_cases["getWebhookEventType"].criticality == CriticalityEnum.VERY_HIGH


def test_read_yml_not_found_defined_path():

    with pytest.raises(ValueError, match=r"Path .+ of metadata does not exist"):
        read_service_metadata("./algo.yml")


def test_read_yml_not_found_non_defined_path():

    with pytest.raises(ValueError, match="No compatible default path could be found"):
        read_service_metadata()


@pytest.mark.parametrize("path_option", [
    "./tests/examples/webhook.yml",  # Usamos la ruta predeterminada modificada
])
def test_read_service_metadata(path_option):
    with mock.patch("bisslog_schema.read_metadata.default_path_options", (path_option,)):
        service_data = read_service_metadata()

        assert service_data.type == "microservice"
        assert service_data.name == "webhook receiver"
        assert service_data.team == "code-infrastructure"

        assert service_data.use_cases["getWebhookEventType"].criticality == CriticalityEnum.VERY_HIGH
