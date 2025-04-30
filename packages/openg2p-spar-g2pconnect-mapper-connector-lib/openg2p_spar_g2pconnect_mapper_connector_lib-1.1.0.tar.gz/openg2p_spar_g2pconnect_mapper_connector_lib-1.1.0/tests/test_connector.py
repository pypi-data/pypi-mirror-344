from unittest.mock import AsyncMock, patch

import pytest
from openg2p_spar_g2pconnect_mapper_connector_lib.connector import (
    MapperConnector,
)
from openg2p_spar_mapper_interface_lib.response import MapperResponse


@pytest.fixture()
def setup():
    test_id = "123"
    test_fa = "456"
    test_name = "John Doe"
    test_phone_number = "555-1234"
    test_additional_info = [{"key": "value"}]

    expected_mapper_response = MapperResponse(
        id=test_id,
        fa=test_fa,
        name=test_name,
        phone_number=test_phone_number,
        additional_info=test_additional_info,
        status="succ",
        mapper_error_code=None,
        mapper_error_message="",
    )
    return (
        test_id,
        test_fa,
        test_name,
        test_phone_number,
        test_additional_info,
        expected_mapper_response,
    )


class MockLinkRequest:
    def __init__(self, id, fa, name, phone_number, additional_info):
        self.id = id
        self.fa = fa
        self.name = name
        self.phone_number = phone_number
        self.additional_info = additional_info

    def dict(self):
        return {
            "id": self.id,
            "fa": self.fa,
            "name": self.name,
            "phone_number": self.phone_number,
            "additional_info": self.additional_info,
        }


class MockUnlinkRequest:
    def __init__(self, id):
        self.id = id

    def dict(self):
        return {"id": self.id}


class MockResolveRequest:
    def __init__(self, id):
        self.id = id

    def dict(self):
        return {"id": self.id}


class MockUpdateRequest:
    def __init__(self, id, fa, name, phone_number, additional_info):
        self.id = id
        self.fa = fa
        self.name = name
        self.phone_number = phone_number
        self.additional_info = additional_info

    def dict(self):
        return {
            "id": self.id,
            "fa": self.fa,
            "name": self.name,
            "phone_number": self.phone_number,
            "additional_info": self.additional_info,
        }


@pytest.mark.asyncio
async def test_link(setup):
    (
        test_id,
        test_fa,
        test_name,
        test_phone_number,
        test_additional_info,
        expected_mapper_response,
    ) = setup
    with patch(
        "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperConnectorHelper.get_component",
        return_value=AsyncMock(),
    ) as mock_helper:
        with patch(
            "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperLinkClient.get_component",
            return_value=AsyncMock(),
        ) as mock_service:
            # Adjust this line to use the MockLinkRequest class instead of a string
            mock_helper.return_value.construct_link_request.side_effect = (
                lambda id, fa, name, phone_number, additional_info: MockLinkRequest(
                    id, fa, name, phone_number, additional_info
                )
            )
            mock_helper.return_value.create_jwt_token = AsyncMock(
                return_value="mock_jwt_token"
            )
            mock_helper.return_value.construct_mapper_response_link.return_value = (
                expected_mapper_response
            )
            mock_service.return_value.link_request.return_value = (
                expected_mapper_response
            )
            mapper_connector = MapperConnector()
            result = await mapper_connector.link(
                id=test_id,
                fa=test_fa,
                name=test_name,
                phone_number=test_phone_number,
                additional_info=test_additional_info,
                link_url="",
            )

            assert result == expected_mapper_response

            mock_helper.return_value.construct_link_request.assert_called_once_with(
                test_id, test_fa, test_name, test_phone_number, test_additional_info
            )
            mock_helper.return_value.create_jwt_token.assert_called_once_with(
                {
                    "id": test_id,
                    "fa": test_fa,
                    "name": test_name,
                    "phone_number": test_phone_number,
                    "additional_info": test_additional_info,
                }
            )
            mock_helper.return_value.construct_mapper_response_link.assert_called_once_with(
                expected_mapper_response
            )


@pytest.mark.asyncio
async def test_unlink(setup):
    test_id, test_fa, _, _, _, expected_mapper_response = setup
    with patch(
        "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperConnectorHelper.get_component",
        return_value=AsyncMock(),
    ) as mock_helper:
        with patch(
            "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperUnlinkClient.get_component",
            return_value=AsyncMock(),
        ) as mock_service:
            mock_helper.return_value.construct_unlink_request.side_effect = (
                lambda id: MockUnlinkRequest(id)
            )
            mock_helper.return_value.construct_mapper_response_unlink.return_value = (
                expected_mapper_response
            )
            mock_service.return_value.unlink_request.return_value = (
                expected_mapper_response
            )
            mapper_connector = MapperConnector()
            result = await mapper_connector.unlink(id=test_id, unlink_url="")

            assert result == expected_mapper_response

            mock_helper.return_value.construct_mapper_response_unlink.assert_called_once_with(
                expected_mapper_response
            )


@pytest.mark.asyncio
async def test_resolve(setup):
    test_id, _, _, _, _, expected_mapper_response = setup
    with patch(
        "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperConnectorHelper.get_component",
        return_value=AsyncMock(),
    ) as mock_helper:
        with patch(
            "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperResolveClient.get_component",
            return_value=AsyncMock(),
        ) as mock_service:
            mock_helper.return_value.construct_resolve_request.side_effect = (
                lambda id: MockResolveRequest(id)
            )
            mock_helper.return_value.construct_mapper_response_resolve.return_value = (
                expected_mapper_response
            )
            mock_service.return_value.resolve_request.return_value = (
                expected_mapper_response
            )
            mapper_connector = MapperConnector()
            result = await mapper_connector.resolve(id=test_id, resolve_url="")

            assert result == expected_mapper_response

            mock_helper.return_value.construct_resolve_request.assert_called_once_with(
                test_id
            )
            mock_helper.return_value.construct_mapper_response_resolve.assert_called_once_with(
                expected_mapper_response
            )


@pytest.mark.asyncio
async def test_update(setup):
    (
        test_id,
        test_fa,
        test_name,
        test_phone_number,
        test_additional_info,
        expected_mapper_response,
    ) = setup
    with patch(
        "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperConnectorHelper.get_component",
        return_value=AsyncMock(),
    ) as mock_helper:
        with patch(
            "openg2p_spar_g2pconnect_mapper_connector_lib.connector.MapperUpdateClient.get_component",
            return_value=AsyncMock(),
        ) as mock_service:
            mock_helper.return_value.construct_update_request.side_effect = (
                lambda id, fa, name, phone_number, additional_info: MockUpdateRequest(
                    id, fa, name, phone_number, additional_info
                )
            )
            mock_helper.return_value.construct_mapper_response_update.return_value = (
                expected_mapper_response
            )
            mock_service.return_value.update_request.return_value = (
                expected_mapper_response
            )
            mapper_connector = MapperConnector()
            result = await mapper_connector.update(
                id=test_id,
                fa=test_fa,
                name=test_name,
                phone_number=test_phone_number,
                additional_info=test_additional_info,
                update_url="",
            )

            assert result == expected_mapper_response

            mock_helper.return_value.construct_update_request.assert_called_once_with(
                test_id, test_fa, test_name, test_phone_number, test_additional_info
            )
            mock_helper.return_value.construct_mapper_response_update.assert_called_once_with(
                expected_mapper_response
            )
