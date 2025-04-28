from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.token import MaleoSecurityTokenHTTPClientController
from maleo_security.models.transfers.results.token import MaleoSecurityTokenResultsTransfers
from maleo_security.models.transfers.parameters.token import MaleoSecurityTokenParametersTransfers
from maleo_security.types.results.token import MaleoSecurityTokenResultsTypes

class MaleoSecurityTokenClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="encoding a payload",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityTokenResultsTransfers.Fail
    )
    async def encode(
        parameters:MaleoSecurityTokenParametersTransfers.Encode,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityTokenResultsTypes.Encode:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityTokenResultsTransfers.Fail(message=message, description=description)
        #* Encode payload using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityTokenHTTPClientController.encode(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityTokenResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityTokenResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityTokenResultsTransfers.Encode.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="decoding a token",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecurityTokenResultsTransfers.Fail
    )
    async def decode(
        parameters:MaleoSecurityTokenParametersTransfers.Decode,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecurityTokenResultsTypes.Decode:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecurityTokenResultsTransfers.Fail(message=message, description=description)
        #* Decode token using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecurityTokenHTTPClientController.decode(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecurityTokenResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecurityTokenResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecurityTokenResultsTransfers.Decode.model_validate(controller_result.content)