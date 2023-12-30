from typing import Optional

import pydantic


# создание объявления
class CreateAd(pydantic.BaseModel):
    title: str
    description: str
    owner_ad: int


# обновление пользователя
class UpdateAd(pydantic.BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner_ad: Optional[int] = None