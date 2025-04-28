from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.encryption.rsa import MaleoSecurityRSAEncryptionHTTPClientController
from maleo_security.models.transfers.results.encryption.rsa import MaleoSecurityRSAEncryptionResultsTransfers
from maleo_security.models.transfers.parameters.encryption.rsa import MaleoSecurityRSAEncryptionParametersTransfers
from maleo_security.types.results.encryption.rsa import MaleoSecurityRSAEncryptionResultsTypes

class MaleoSecurityRSAEncryptionClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="encrypting single plaintext",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityRSAEncryptionResultsTransfers.Fail
    )
    async def encrypt_single(
        parameters:MaleoSecurityRSAEncryptionParametersTransfers.EncryptSingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityRSAEncryptionResultsTypes.SingleEncryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Encrypt single plaintext using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityRSAEncryptionHTTPClientController.encrypt_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityRSAEncryptionResultsTransfers.SingleEncryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="encrypting multiple plaintexts",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityRSAEncryptionResultsTransfers.Fail
    )
    async def encrypt_multiple(
        parameters:MaleoSecurityRSAEncryptionParametersTransfers.EncryptMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityRSAEncryptionResultsTypes.MultipleEncryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Encrypt multiple plaintexts using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityRSAEncryptionHTTPClientController.encrypt_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityRSAEncryptionResultsTransfers.MultipleEncryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="decrypting single ciphertext",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityRSAEncryptionResultsTransfers.Fail
    )
    async def decrypt_single(
        parameters:MaleoSecurityRSAEncryptionParametersTransfers.DecryptSingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityRSAEncryptionResultsTypes.SingleDecryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Decrypt single ciphertext using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityRSAEncryptionHTTPClientController.decrypt_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityRSAEncryptionResultsTransfers.SingleDecryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="decrypting multiple ciphertexts",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityRSAEncryptionResultsTransfers.Fail
    )
    async def decrypt_multiple(
        parameters:MaleoSecurityRSAEncryptionParametersTransfers.DecryptMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityRSAEncryptionResultsTypes.MultipleDecryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Decrypt multiple ciphertexts using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityRSAEncryptionHTTPClientController.decrypt_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityRSAEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityRSAEncryptionResultsTransfers.MultipleDecryption.model_validate(controller_result.content)