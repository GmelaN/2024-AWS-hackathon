from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from base.response_code import ResponseCode

T = TypeVar('T')


class CommonResponseModel(BaseModel, Generic[T]):
    success: bool
    code: Optional[ResponseCode] = None
    data: Optional[T] = None
