# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import TypedDict

from .validation_message_dto_param import ValidationMessageDtoParam

__all__ = ["ValidationMessagesDtoParam"]


class ValidationMessagesDtoParam(TypedDict, total=False):
    errors: Iterable[ValidationMessageDtoParam]

    warnings: Iterable[ValidationMessageDtoParam]
