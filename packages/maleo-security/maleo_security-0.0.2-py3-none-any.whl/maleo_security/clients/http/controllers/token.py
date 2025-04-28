from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_security.clients.http.manager import MaleoSecurityHTTPClientManager
from maleo_security.models.transfers.parameters.token import MaleoSecurityTokenParametersTransfers

class MaleoSecurityTokenHTTPClientController:
    @staticmethod
    async def encode(parameters:MaleoSecurityTokenParametersTransfers.Encode) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/tokens/encode"

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
    async def decode(parameters:MaleoSecurityTokenParametersTransfers.Decode) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/tokens/decode"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)