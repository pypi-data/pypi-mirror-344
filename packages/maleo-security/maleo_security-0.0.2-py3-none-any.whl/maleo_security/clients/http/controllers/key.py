from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_security.clients.http.manager import MaleoSecurityHTTPClientManager
from maleo_security.models.transfers.parameters.key import MaleoSecurityKeyParametersTransfers

class MaleoSecurityKeyHTTPClientController:
    @staticmethod
    async def create_private(parameters:MaleoSecurityKeyParametersTransfers.CreatePrivateOrPair) -> BaseClientHTTPControllerResults:
        """Create an RSA private key with X.509 encoding in .pem format."""
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/keys/private"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def create_public(parameters:MaleoSecurityKeyParametersTransfers.CreatePublic) -> BaseClientHTTPControllerResults:
        """Create an RSA public key with X.509 encoding in .pem format."""
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/keys/public"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)

    @staticmethod
    async def create_pair(parameters:MaleoSecurityKeyParametersTransfers.CreatePrivateOrPair) -> BaseClientHTTPControllerResults:
        """Create an RSA key pair with X.509 encoding in .pem format."""
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/keys/pair"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)