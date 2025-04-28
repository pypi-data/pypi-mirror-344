from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.key import MaleoSecurityKeyHTTPClientController
from maleo_security.models.transfers.results.key import MaleoSecurityKeyResultsTransfers
from maleo_security.models.transfers.parameters.key import MaleoSecurityKeyParametersTransfers
from maleo_security.types.results.key import MaleoSecurityKeyResultsTypes

class MaleoSecurityKeyClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="creating private key",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityKeyResultsTransfers.Fail
    )
    async def create_private(
        parameters:MaleoSecurityKeyParametersTransfers.CreatePrivateOrPair,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityKeyResultsTypes.CreatePrivate:
        """Create an RSA private key with X.509 encoding in .pem format."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Create private key using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityKeyHTTPClientController.create_private(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityKeyResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityKeyResultsTransfers.SinglePrivate.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="creating public key",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityKeyResultsTransfers.Fail
    )
    async def create_public(
        parameters:MaleoSecurityKeyParametersTransfers.CreatePublic,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityKeyResultsTypes.CreatePublic:
        """Create an RSA public key with X.509 encoding in .pem format."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Create public key using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityKeyHTTPClientController.create_public(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityKeyResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityKeyResultsTransfers.SinglePublic.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="creating key pair",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityKeyResultsTransfers.Fail
    )
    async def create_pair(
        parameters:MaleoSecurityKeyParametersTransfers.CreatePrivateOrPair,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityKeyResultsTypes.CreatePair:
        """Create an RSA key pair with X.509 encoding in .pem format."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Create public key using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityKeyHTTPClientController.create_pair(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityKeyResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityKeyResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityKeyResultsTransfers.SinglePair.model_validate(controller_result.content)