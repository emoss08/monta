from typing import Type

from ninja import ModelSchema, Schema

from monta_billing import models


class ChargeTypeIn(Schema):
    """
    Schema for creating a charge type.
    """

    name: str
    description: str


class ChargeTypeSchema(ModelSchema):
    """
    ChargeTypeSchema
    """

    class Config:
        """
        Config class
        """

        model: Type[models.ChargeType] = models.ChargeType
        model_fields: list[str] = ["id", "name", "description"]
