from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.hash.hmac import MaleoSecurityHMACHashHTTPClientController
from maleo_security.models.transfers.results.hash import MaleoSecurityHashResultsTransfers
from maleo_security.models.transfers.parameters.hash.hmac import MaleoSecurityHMACHashParametersTransfers
from maleo_security.types.results.hash import MaleoSecurityHashResultsTypes

class MaleoSecurityHMACHashClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="hashing with HMAC",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityHashResultsTransfers.Fail
    )
    async def hash(
        parameters:MaleoSecurityHMACHashParametersTransfers.Hash,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityHashResultsTypes.Hash:
        """Generate a hmac hash for the given message."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Generate HMAC Hash using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityHMACHashHTTPClientController.hash(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityHashResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityHashResultsTransfers.Hash.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="verifying HMAC hash",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityHashResultsTransfers.Fail
    )
    async def verify(
        parameters:MaleoSecurityHMACHashParametersTransfers.Verify,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityHashResultsTypes.Verify:
        """Verify a message against the given message hash."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Generate HMAC Hash using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityHMACHashHTTPClientController.verify(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityHashResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityHashResultsTransfers.Verify.model_validate(controller_result.content)