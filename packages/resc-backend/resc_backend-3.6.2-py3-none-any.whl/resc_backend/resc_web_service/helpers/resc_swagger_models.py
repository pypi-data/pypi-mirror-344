# Third Party
from pydantic import BaseModel, ConfigDict


class RescResponseModel(BaseModel):
    """
    Generic schema to be used for a response from resc scanner.
    """


class Model400(RescResponseModel):
    """
    Response schema to be used for a 400 BAD REQUEST.
    """

    model_config = ConfigDict(json_schema_extra={"example": {"detail": "Bad Request"}})


class Model403(RescResponseModel):
    """
    Response schema to be used for a 403 FORBIDDEN.
    """

    model_config = ConfigDict(json_schema_extra={"example": {"data": {}, "detail": "Action Forbidden"}})


class Model404(RescResponseModel):
    """
    Response schema to be used for a 404 NOT FOUND.
    """

    model_config = ConfigDict(json_schema_extra={"example": {"data": {}, "detail": "<id> not found"}})


class Model409(RescResponseModel):
    """
    Response schema to be used for a 409 CONFLICT.
    """

    model_config = ConfigDict(json_schema_extra={"example": {"detail": "Unable to process entity due to conflict"}})


class Model422(RescResponseModel):
    """
    Response schema to be used for a 422 UNPROCESSABLE ENTITY.
    """

    model_config = ConfigDict(json_schema_extra={"example": {"detail": "Entity cannot be processed"}})
