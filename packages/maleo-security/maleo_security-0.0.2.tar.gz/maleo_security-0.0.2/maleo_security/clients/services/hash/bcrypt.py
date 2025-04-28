from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.hash.bcrypt import MaleoSecurityBcryptHashHTTPClientController
from maleo_security.models.transfers.results.hash import MaleoSecurityHashResultsTransfers
from maleo_security.models.transfers.parameters.hash.bcrypt import MaleoSecurityBcryptHashParametersTransfers
from maleo_security.types.results.hash import MaleoSecurityHashResultsTypes

class MaleoSecurityBcryptHashClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="hashing with Bcrypt",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityHashResultsTransfers.Fail
    )
    async def hash(
        parameters:MaleoSecurityBcryptHashParametersTransfers.Hash,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityHashResultsTypes.Hash:
        """Generate a bcrypt hash for the given message."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Generate Bcrypt Hash using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityBcryptHashHTTPClientController.hash(parameters=parameters)
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
        operation="verifying Bcrypt hash",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityHashResultsTransfers.Fail
    )
    async def verify(
        parameters:MaleoSecurityBcryptHashParametersTransfers.Verify,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityHashResultsTypes.Verify:
        """Verify a message against the given message hash."""
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Generate Bcrypt Hash using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityBcryptHashHTTPClientController.verify(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityHashResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityHashResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityHashResultsTransfers.Verify.model_validate(controller_result.content)