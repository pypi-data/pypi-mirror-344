from typing import Any, Dict, List, Optional

from openg2p_g2pconnect_mapper_lib.client import (
    MapperLinkClient,
    MapperResolveClient,
    MapperUnlinkClient,
    MapperUpdateClient,
)
from openg2p_g2pconnect_mapper_lib.schemas import (
    LinkRequest,
    LinkResponse,
    ResolveRequest,
    ResolveResponse,
    UnlinkRequest,
    UnlinkResponse,
    UpdateRequest,
    UpdateResponse,
)
from openg2p_spar_mapper_interface_lib.interface import MapperInterface
from openg2p_spar_mapper_interface_lib.response import MapperResponse

from .helper import MapperConnectorHelper


class MapperConnector(MapperInterface):
    async def link(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
        link_url: str,
    ) -> MapperResponse:
        mapper_connector_helper = MapperConnectorHelper.get_component()
        link_request: LinkRequest = (
            await mapper_connector_helper.construct_link_request(
                id, fa, name, phone_number, additional_info
            )
        )
        jwt_token = await mapper_connector_helper.create_jwt_token(link_request.dict())
        headers = {"content-type": "application/json", "Authorization": jwt_token}
        link_response: (
            LinkResponse
        ) = await MapperLinkClient.get_component().link_request(
            link_url=link_url, link_request=link_request, headers=headers
        )
        mapper_response = await mapper_connector_helper.construct_mapper_response_link(
            link_response
        )
        return mapper_response

    async def unlink(self, id: str, unlink_url: str) -> MapperResponse:
        mapper_connector_helper = MapperConnectorHelper.get_component()
        unlink_request: UnlinkRequest = (
            await mapper_connector_helper.construct_unlink_request(id=id)
        )
        jwt_token = await mapper_connector_helper.create_jwt_token(
            unlink_request.dict()
        )
        headers = {"content-type": "application/json", "Authorization": jwt_token}
        unlink_response: (
            UnlinkResponse
        ) = await MapperUnlinkClient.get_component().unlink_request(
            unlink_request=unlink_request, unlink_url=unlink_url, headers=headers
        )
        mapper_response = (
            await mapper_connector_helper.construct_mapper_response_unlink(
                unlink_response
            )
        )
        return mapper_response

    async def resolve(self, id: str, resolve_url: str) -> MapperResponse:
        mapper_connector_helper = MapperConnectorHelper.get_component()
        resolve_request: ResolveRequest = (
            await mapper_connector_helper.construct_resolve_request(id)
        )
        jwt_token = await mapper_connector_helper.create_jwt_token(
            resolve_request.dict()
        )
        headers = {"content-type": "application/json", "Authorization": jwt_token}
        resolve_response: (
            ResolveResponse
        ) = await MapperResolveClient.get_component().resolve_request(
            resolve_request=resolve_request, resolve_url=resolve_url, headers=headers
        )
        mapper_response = (
            await mapper_connector_helper.construct_mapper_response_resolve(
                resolve_response
            )
        )
        return mapper_response

    async def update(
        self,
        id: str,
        fa: str,
        name: Optional[str],
        phone_number: Optional[str],
        additional_info: Optional[List[Dict[str, Any]]],
        update_url: str,
    ) -> MapperResponse:
        mapper_connector_helper = MapperConnectorHelper.get_component()
        update_request: UpdateRequest = (
            await mapper_connector_helper.construct_update_request(
                id, fa, name, phone_number, additional_info
            )
        )
        jwt_token = await mapper_connector_helper.create_jwt_token(
            update_request.dict()
        )
        headers = {"content-type": "application/json", "Authorization": jwt_token}
        update_response: (
            UpdateResponse
        ) = await MapperUpdateClient.get_component().update_request(
            update_request=update_request, update_url=update_url, headers=headers
        )
        mapper_response = (
            await mapper_connector_helper.construct_mapper_response_update(
                update_response
            )
        )
        return mapper_response
