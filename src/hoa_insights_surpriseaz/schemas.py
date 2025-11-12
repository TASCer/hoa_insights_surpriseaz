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
    SALE_PRICE: int | str | None = None
    DEED_DATE: str | None = None
    DEED_TYPE: str | None = None
    LEGAL_CODE: str
    RENTAL: bool

    @field_validator("APN")
    def format_apn(cls, value) -> str:
        return format_apn(value)

    @field_validator("DEED_DATE", "SALE_DATE")
    def format_date(cls, value) -> date:
        return date_parser.api_date(value)

    @field_validator("MAIL_ADX", "OWNER")
    def remove_comma(cls, value):
        return value.replace(",", "")

    def remove_apostrophe(cls, value):
        return value.replace("'", "''")

    @field_validator("SALE_PRICE")
    def empty_sale_price(cls, value) -> None:
        if isinstance(value, str) and value == "":
            value = None

        return value


class Rentals(BaseModel):
    APN: str
    OWNER: str
    OWNER_TYPE: str
    CONTACT: str
    CONTACT_ADX: str
    CONTACT_PH: str

    @field_validator("APN")
    def format_apn(cls, value) -> str:
        return format_apn(value)

    @field_validator("CONTACT_PH")
    def format_phone(cls, value) -> str:
        return format_phone(value)

    @field_validator("CONTACT_ADX", "CONTACT", "OWNER")
    def remove_comma(cls, value):  # -> Any:
        return value.replace(",", "")

    def remove_apostrophe(cls, value):
        return value.replace("'", "''")


class Parcels(BaseModel):
    APN: str
    COMMUNITY: str
    SITUS: str
    LAT: str
    LONG: str
