from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.encryption.aes import MaleoSecurityAESEncryptionHTTPClientController
from maleo_security.models.transfers.results.encryption.aes import MaleoSecurityAESEncryptionResultsTransfers
from maleo_security.models.transfers.parameters.encryption.aes import MaleoSecurityAESEncryptionParametersTransfers
from maleo_security.types.results.encryption.aes import MaleoSecurityAESEncryptionResultsTypes

class MaleoSecurityAESEncryptionClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="encrypting single plaintext",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityAESEncryptionResultsTransfers.Fail
    )
    async def encrypt_single(
        parameters:MaleoSecurityAESEncryptionParametersTransfers.EncryptSingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityAESEncryptionResultsTypes.SingleEncryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Encrypt single plaintext using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityAESEncryptionHTTPClientController.encrypt_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityAESEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityAESEncryptionResultsTransfers.SingleEncryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="encrypting multiple plaintexts",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityAESEncryptionResultsTransfers.Fail
    )
    async def encrypt_multiple(
        parameters:MaleoSecurityAESEncryptionParametersTransfers.EncryptMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityAESEncryptionResultsTypes.MultipleEncryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Encrypt multiple plaintexts using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityAESEncryptionHTTPClientController.encrypt_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityAESEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityAESEncryptionResultsTransfers.MultipleEncryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="decrypting single ciphertext",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityAESEncryptionResultsTransfers.Fail
    )
    async def decrypt_single(
        parameters:MaleoSecurityAESEncryptionParametersTransfers.DecryptSingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityAESEncryptionResultsTypes.SingleDecryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Decrypt single ciphertext using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityAESEncryptionHTTPClientController.decrypt_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityAESEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityAESEncryptionResultsTransfers.SingleDecryption.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="decrypting multiple ciphertexts",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityAESEncryptionResultsTransfers.Fail
    )
    async def decrypt_multiple(
        parameters:MaleoSecurityAESEncryptionParametersTransfers.DecryptMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityAESEncryptionResultsTypes.MultipleDecryption:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Decrypt multiple ciphertexts using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityAESEncryptionHTTPClientController.decrypt_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityAESEncryptionResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityAESEncryptionResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityAESEncryptionResultsTransfers.MultipleDecryption.model_validate(controller_result.content)