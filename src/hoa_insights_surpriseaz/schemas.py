from datetime import date
from pydantic import BaseModel, field_validator
from hoa_insights_surpriseaz.utils.number_formatter import format_apn, format_phone
from hoa_insights_surpriseaz.utils import date_parser


class Community(BaseModel):
    COMMUNITY: str
    LAT: float
    LONG: float
    COUNT: int
    MANAGED_ID: int


class CommunityManagement(BaseModel):
    COMMUNITY: str
    BOARD_SITUS: str
    BOARD_CITY: str
    MANAGER: str
    CONTACT_ADX: str
    CONTACT_PH: str


class Owners(BaseModel):
    APN: str
    OWNER: str
    MAIL_ADX: str
    SALE_DATE: str | None = None
    SALE_PRICE: str | None = None
    DEED_DATE: str | None = None
    DEED_TYPE: str | None = None
    LEGAL_CODE: str
    RENTAL: bool

    @field_validator("APN")
    def format_apn(cls, v) -> str:
        return format_apn(v)

    @field_validator("DEED_DATE", "SALE_DATE")
    def format_date(cls, v) -> date:
        return date_parser.api_date(v)

    @field_validator("MAIL_ADX", "OWNER")
    def remove_comma(cls, v):
        return v.replace(",", "")

    def remove_apostrophe(cls, v):
        return v.replace("'", "''")

    @field_validator("SALE_PRICE")
    def empty_sale_price(cls, v) -> int:
        if v is None or v == "":
            return int(0)
        else:
            return v


class Rentals(BaseModel):
    APN: str
    OWNER: str
    OWNER_TYPE: str
    CONTACT: str
    CONTACT_ADX: str
    CONTACT_PH: str

    @field_validator("APN")
    def format_apn(cls, v) -> str:
        return format_apn(v)

    @field_validator("CONTACT_PH")
    def format_phone(cls, v) -> str:
        return format_phone(v)

    @field_validator("CONTACT_ADX", "CONTACT", "OWNER")
    def remove_comma(cls, v):  # -> Any:
        return v.replace(",", "")

    def remove_apostrophe(cls, v):
        return v.replace("'", "''")


class Parcels(BaseModel):
    APN: str
    COMMUNITY: str
    SITUS: str
    LAT: str
    LONG: str
