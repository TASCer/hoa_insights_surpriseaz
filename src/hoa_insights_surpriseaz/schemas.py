from datetime import date
from pydantic import BaseModel


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
    SALE_DATE: date | None = None
    SALE_PRICE: int
    DEED_DATE: date | None = None
    DEED_TYPE: str
    LEGAL_CODE: str
    RENTAL: bool


class Rentals(BaseModel):
    APN: str
    OWNER: str
    OWNER_TYPE: str
    CONTACT: str
    CONTACT_ADX: str
    CONTACT_PH: str


class Parcels(BaseModel):
    APN: str
    COMMUNITY: str
    SITUS: str
    LAT: str
    LONG: str
