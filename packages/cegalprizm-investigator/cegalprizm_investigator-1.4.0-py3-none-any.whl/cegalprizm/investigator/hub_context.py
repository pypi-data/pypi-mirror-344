# Copyright 2025 Cegal AS
# All rights reserved.
# Unauthorized copying of this file, via any medium is strictly prohibited.

"""This file contains the definition of the InvPyHubContext class

This class is used internally to interact with a Hub connection
"""

from typing import Dict, Iterable

from google.protobuf.any_pb2 import Any
from grpc import RpcError

from cegalprizm.hub import BaseContext, ConnectorFilter, ConnectionParameters, Hub, HubClient

# pylint: disable=relative-beyond-top-level
# pylint: disable=logging-fstring-interpolation

from . import logger

_VERIFY_PAYLOADS: str = "investigator.ListInvestigations"

class InvPyHubContext():

    def __init__(self, use_licensed_features: bool, hub_petrel_context: BaseContext = None, hub_connection_parameters: ConnectionParameters = None):
        logger.debug("Creating InvPyHubContext")
        self._use_licensed_features = use_licensed_features
        self._hub_client = None
        self._original_connection_parameters = None
        self._connection_parameters = None
        self._connector_filter = None
        self._wellknown_connector_identifier = None
        self._token_provider = None

        if hub_petrel_context is not None:
            self._original_connection_parameters = hub_petrel_context.connection_parameters
            self._connector_filter = hub_petrel_context.connector_filter
            self._token_provider = hub_petrel_context._hub_client._token_provider
        elif hub_connection_parameters is not None:
            self._original_connection_parameters = hub_connection_parameters
            self._connector_filter = ConnectorFilter()
        else:
            self._original_connection_parameters = ConnectionParameters()
            self._connector_filter = ConnectorFilter()

        self._client()

    def _check_hub_status(self)->bool:
        try:
            logger.debug("Checking Hub status")
            if self._use_licensed_features:
                logger.debug("Full Investigator API available (if Keystone licensing permits)")
            else:
                logger.debug("Only unlicensed Investigator API is available")

            self._connection_parameters = ConnectionParameters(host=self._original_connection_parameters.host,
                                                               port=self._original_connection_parameters.port,
                                                               use_tls=self._original_connection_parameters.use_tls,
                                                               use_auth=self._use_licensed_features)
            self._set_target_connector()
            return True
        except RpcError:
            logger.warning("Please check if a Hub Server is running and available for connections.\n" +
                           "This information can be found in the Hub Connection Settings tool under Hub in Marina in Petrel.\n" +
                           "For local connections; start a local Hub Server.\n" +
                           "For remote connections; please contact the Hub admin in your organisation.")
            return False
        except Exception as e:
            logger.debug(e)
            logger.debug("Do not use Keystone licensing")
            self._connection_parameters = self._original_connection_parameters
            return False

    def _set_target_connector(self)->bool:
        try:
            if self._find_target_connector("cegal.hub.petrel", False):
                return True

            if self._find_target_connector("cegal.investigator", False):
                return True

            if self._find_target_connector("cegal.investigator", True):
                return True

            logger.warning("Cannot establish communication with Hub connector")
            return False
        except:
            logger.warning("Cannot establish communication with Hub connector")
            return False

    def _find_target_connector(self, wellknown_identifier: str, check_public: bool)->bool:
        connection_parameters = self._connection_parameters if self._connection_parameters else self._original_connection_parameters
        hub = Hub(connection_parameters=connection_parameters)
        if len(self._connector_filter.target_connector_id) > 0:
            for conn in hub.query_connectors():
                if conn.connector_id == self._connector_filter.target_connector_id:
                    if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                        logger.info(f"Connector {conn.wellknown_identifier}: {conn.connector_id}")
                        self._wellknown_connector_identifier = conn.wellknown_identifier
                        return True
            logger.warning(f"Connector {self._connector_filter.target_connector_id} cannot be used with cegalprizm.investigator")
            return False

        for conn in hub.query_connectors():
            if conn.wellknown_identifier == wellknown_identifier:
                if check_public:
                    if conn.supports_public_requests:
                        if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                            logger.info(f"Public {wellknown_identifier}: {conn.connector_id}")
                            self._connector_filter.target_connector_id = conn.connector_id
                            self._wellknown_connector_identifier = wellknown_identifier
                            return True
                else:
                    if not conn.supports_public_requests:
                        if _VERIFY_PAYLOADS in conn.supported_payloads.keys():
                            logger.info(f"Private {wellknown_identifier}: {conn.connector_id}")
                            self._connector_filter.target_connector_id = conn.connector_id
                            self._wellknown_connector_identifier = wellknown_identifier
                            return True
        return False

    def _client(self) -> HubClient:
        if self._hub_client is None:
            logger.debug("Creating new HubClient")
            self._check_hub_status()
            self._hub_client = HubClient(connection_parameters=self._connection_parameters, token_provider=self._token_provider)
        return self._hub_client

    def force_new(self):
        self.close()

    def close(self):
        if self._hub_client is not None:
            self._hub_client.close()
        self._hub_client = None

    def set_connector_labels(self, labels: Dict[str, str]):
        self._connector_filter.labels = labels
        self._hub_client = None

    def do_unary_request(self, wellknown_payload_identifier: str, payload: Any, wellknown_connector_identifier: str = None, major_version: int = 0, minor_version: int = 0):
        if wellknown_connector_identifier is None:
            wellknown_connector_identifier = self._wellknown_connector_identifier

        logger.debug(f"do_unary_request: {wellknown_payload_identifier}")
        result = self._client().do_unary_request(wellknown_connector_identifier=wellknown_connector_identifier,
                                                 wellknown_payload_identifier=wellknown_payload_identifier,
                                                 payload=payload,
                                                 connector_filter=self._connector_filter,
                                                 major_version=major_version,
                                                 minor_version=minor_version)
        if result[0]:
            logger.debug("Success")
        else:
            logger.debug(f"Failed: {result[1]}")
        return result

    def do_client_streaming(self, wellknown_payload_identifier: str, iter_payloads: Iterable[Any], major_version: int = 0, minor_version: int = 0):
        logger.debug(f"do_client_streaming: {wellknown_payload_identifier}")
        result = self._client().do_client_streaming(wellknown_connector_identifier=self._wellknown_connector_identifier,
                                                    wellknown_payload_identifier=wellknown_payload_identifier,
                                                    iterable_payloads=iter_payloads,
                                                    connector_filter=self._connector_filter,
                                                    major_version=major_version,
                                                    minor_version=minor_version)
        if result[0]:
            logger.debug("Success")
        else:
            logger.debug(f"Failed: {result[1]}")
        return result

    def do_server_streaming(self, wellknown_payload_identifier: str, payload: Any, major_version: int = 0, minor_version: int = 0):
        logger.debug(f"do_server_streaming: {wellknown_payload_identifier}")
        return self._client().do_server_streaming(wellknown_connector_identifier=self._wellknown_connector_identifier,
                                                  wellknown_payload_identifier=wellknown_payload_identifier,
                                                  payload=payload,
                                                  connector_filter=self._connector_filter,
                                                  major_version=major_version,
                                                  minor_version=minor_version)
                                                      