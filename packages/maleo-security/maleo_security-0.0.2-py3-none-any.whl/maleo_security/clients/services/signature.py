from maleo_foundation.utils.exceptions import BaseExceptions
from maleo_security.enums.general import MaleoSecurityGeneralEnums
from maleo_security.utils.logger import MaleoSecurityLoggerManager
from maleo_security.clients.http.controllers.signature import MaleoSecuritySignatureHTTPClientController
from maleo_security.models.transfers.results.signature import MaleoSecuritySignatureResultsTransfers
from maleo_security.models.transfers.parameters.signature import MaleoSecuritySignatureParametersTransfers
from maleo_security.types.results.signature import MaleoSecuritySignatureResultsTypes

class MaleoSecuritySignatureClientService:
    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="signing single message",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecuritySignatureResultsTransfers.Fail
    )
    async def sign_single(
        parameters:MaleoSecuritySignatureParametersTransfers.SignSingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecuritySignatureResultsTypes.SingleSignature:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Sign single message using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecuritySignatureHTTPClientController.sign_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecuritySignatureResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecuritySignatureResultsTransfers.SingleSignature.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="signing multiple messages",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecuritySignatureResultsTransfers.Fail
    )
    async def sign_multiple(
        parameters:MaleoSecuritySignatureParametersTransfers.SignMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecuritySignatureResultsTypes.MultipleSignature:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Sign multiple messages using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecuritySignatureHTTPClientController.sign_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecuritySignatureResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecuritySignatureResultsTransfers.MultipleSignature.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="verifying single signature",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecuritySignatureResultsTransfers.Fail
    )
    async def verify_single(
        parameters:MaleoSecuritySignatureParametersTransfers.VerifySingle,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecuritySignatureResultsTypes.SingleVerify:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Verify single signature using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecuritySignatureHTTPClientController.verify_single(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecuritySignatureResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecuritySignatureResultsTransfers.SingleVerify.model_validate(controller_result.content)

    @staticmethod
    @BaseExceptions.service_exception_handler(
        operation="verifying multiple signatures",
        logger_factory=MaleoSecurityLoggerManager.get,
        fail_result_class=MaleoSecuritySignatureResultsTransfers.Fail
    )
    async def verify_multiple(
        parameters:MaleoSecuritySignatureParametersTransfers.VerifyMultiple,
        controller_type:MaleoSecurityGeneralEnums.ClientControllerType = MaleoSecurityGeneralEnums.ClientControllerType.HTTP
    ) -> MaleoSecuritySignatureResultsTypes.MultipleVerify:
        #* Validate chosen controller type
        if not isinstance(controller_type, MaleoSecurityGeneralEnums.ClientControllerType):
            message = "Invalid controller type"
            description = "The provided controller type did not exists"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Verify multiple signatures using chosen controller
        if controller_type == MaleoSecurityGeneralEnums.ClientControllerType.HTTP:
            controller_result = await MaleoSecuritySignatureHTTPClientController.verify_multiple(parameters=parameters)
        else:
            message = "Invalid controller type"
            description = "The provided controller type has not been implemented"
            return MaleoSecuritySignatureResultsTransfers.Fail(message=message, description=description)
        #* Return proper response
        if not controller_result.success:
            return MaleoSecuritySignatureResultsTransfers.Fail.model_validate(controller_result.content)
        else:
            return MaleoSecuritySignatureResultsTransfers.MultipleVerify.model_validate(controller_result.content)