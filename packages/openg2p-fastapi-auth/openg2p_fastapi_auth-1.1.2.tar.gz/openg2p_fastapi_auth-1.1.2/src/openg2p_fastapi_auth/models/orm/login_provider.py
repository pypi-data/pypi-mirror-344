from enum import Enum
from typing import Any, Dict, List, Optional

from openg2p_fastapi_common.models import BaseORMModelWithTimes
from sqlalchemy import JSON, String
from sqlalchemy import Enum as SaEnum
from sqlalchemy.orm import Mapped, mapped_column

from ...config import Settings

_config = Settings.get_config(strict=False)


class LoginProviderTypes(Enum):
    oauth2_auth_code = "oauth2_auth_code"


class LoginProvider(BaseORMModelWithTimes):
    __tablename__ = _config.login_providers_table_name

    name: Mapped[str] = mapped_column(String())
    type: Mapped[LoginProviderTypes] = mapped_column(SaEnum(LoginProviderTypes))

    description: Mapped[Optional[str]] = mapped_column(String())

    login_button_text: Mapped[Optional[str]] = mapped_column(String())
    login_button_image_url: Mapped[Optional[str]] = mapped_column(String())

    authorization_parameters: Mapped[Dict[str, Any]] = mapped_column(JSON(), default={})

    @classmethod
    async def get_login_provider_from_iss(cls, iss: str) -> "LoginProvider":
        # TODO: Modify the following to a direct database query
        # rather than getting all
        providers: List[LoginProvider] = await cls.get_all()
        for lp in providers:
            if lp.type == LoginProviderTypes.oauth2_auth_code:
                if iss in lp.authorization_parameters.get("token_endpoint", ""):
                    return lp
            else:
                raise NotImplementedError()
        return None
