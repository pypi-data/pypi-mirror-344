# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["ConnectionCreateResponse"]


class ConnectionCreateResponse(BaseModel):
    expires_in: str = FieldInfo(alias="expiresIn")

    magic_link: str = FieldInfo(alias="magicLink")
