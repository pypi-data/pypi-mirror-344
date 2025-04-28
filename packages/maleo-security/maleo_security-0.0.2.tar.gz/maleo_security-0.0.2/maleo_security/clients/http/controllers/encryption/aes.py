from maleo_foundation.models.transfers.results.client.controllers.http import BaseClientHTTPControllerResults
from maleo_security.clients.http.manager import MaleoSecurityHTTPClientManager
from maleo_security.models.transfers.parameters.encryption.aes import MaleoSecurityAESEncryptionParametersTransfers

class MaleoSecurityAESEncryptionHTTPClientController:
    @staticmethod
    async def encrypt_single(parameters:MaleoSecurityAESEncryptionParametersTransfers.EncryptSingle) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/encryptions/aes/encrypt/single"

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
    async def encrypt_multiple(parameters:MaleoSecurityAESEncryptionParametersTransfers.EncryptMultiple) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/encryptions/aes/encrypt/multiple"

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
    async def decrypt_single(parameters:MaleoSecurityAESEncryptionParametersTransfers.DecryptSingle) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/encryptions/aes/decrypt/single"

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
    async def decrypt_multiple(parameters:MaleoSecurityAESEncryptionParametersTransfers.DecryptMultiple) -> BaseClientHTTPControllerResults:
        async with MaleoSecurityHTTPClientManager.get_client() as client:
            #* Define URL
            url = f"{MaleoSecurityHTTPClientManager.get_url()}/v1/encryptions/aes/decrypt/multiple"

            #* Define headers
            headers = {
                "Content-Type": "application/json"
            }

            #* Construct body
            json = parameters.model_dump()

            #* Get Response
            response = await client.post(url=url, json=json, headers=headers)
            return BaseClientHTTPControllerResults(response=response)