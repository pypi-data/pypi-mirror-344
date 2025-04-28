from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_security.clients.http.manager import MaleoSecurityHTTPClientManager
from maleo_security.models.transfers.parameters.hash.bcrypt import MaleoSecurityBcryptHashParametersTransfers

class MaleoSecurityBcryptHashHTTPClientController:
    @staticmethod
    async def hash(parameters:MaleoSecurityBcryptHashParametersTransfers.Hash) -> BaseClientHTTPControllerResults:
        """Generate a bcrypt hash for the given message."""
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/hashes/bcrypt/hash"

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
    async def verify(parameters:MaleoSecurityBcryptHashParametersTransfers.Verify) -> BaseClientHTTPControllerResults:
        """Verify a message against the given message hash."""
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/hashes/bcrypt/verify"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)