import logging

from datetime import datetime
from hoa_insights_surpriseaz.schemas import Rentals, Owners
from hoa_insights_surpriseaz.utils.number_formatter import format_apn, format_phone
from hoa_insights_surpriseaz.utils import date_parser
from logging import Logger

logger: Logger = logging.getLogger(__name__)


def rental_data(api_data: list[dict]) -> list[Rentals]:
    """
    Function parses consumed parcel owner rental data from ASSESSOR API.

    :param api_data: sequence of owner rental API data
    :return: sequence of parsed owner rental data
    """
    parsed_rental_data: list[Rentals] = []

    for rental_data in api_data:
        apn: str = format_apn(rental_data["TreasurersTransitionUrl"].split("=")[1])
        rental_owner_type: str = rental_data["RentalInformation"]["OwnershipType"]
        rental_owner_name: str = rental_data["RentalInformation"]["OwnerName"]
        rental_owner_address: str = rental_data["RentalInformation"][
            "OwnerAddress"
        ].replace(",", " ")
        rental_owner_phone: str = format_phone(
            rental_data["RentalInformation"]["OwnerPhone"]
        )

        if isinstance(rental_owner_name, str):
            rental_owner_name: str = rental_owner_name.replace(",", " ")
        else:
            rental_owner_name: str = rental_data["RentalInformation"]["OwnerName"][
                "Name"
            ].replace(",", " ")

        if rental_data["RentalInformation"]["AgentName"]:
            rental_contact_name: str = rental_data["RentalInformation"][
                "AgentName"
            ].replace(",", "")
            rental_contact_address: str = rental_data["RentalInformation"][
                "AgentAddress"
            ].replace(",", "")
            rental_contact_phone: str = format_phone(
                rental_data["RentalInformation"]["AgentPhone"]
            )

        elif rental_data["RentalInformation"]["BusinessContactName"]:
            rental_contact_name: str = rental_data["RentalInformation"][
                "BusinessContactName"
            ].replace(",", "")
            rental_contact_address: str = rental_data["RentalInformation"][
                "BusinessContactAddress"
            ].replace(",", "")
            rental_contact_phone: str = format_phone(
                rental_data["RentalInformation"]["BusinessContactPhone"]
            )
        else:
            rental_contact_name: str = rental_owner_name
            rental_contact_address: str = rental_owner_address
            rental_contact_phone: str = rental_owner_phone

        rental_instance = Rentals(
            APN=apn,
            OWNER=rental_owner_name,
            OWNER_TYPE=rental_owner_type,
            CONTACT=rental_contact_name,
            CONTACT_ADX=rental_contact_address,
            CONTACT_PH=rental_contact_phone,
        )

        parsed_rental_data.append(rental_instance)

    return parsed_rental_data


def owner_data(api_data: list[dict]) -> tuple[list[Owners], list[Rentals]]:
    """
    Function parses consumed parcel owner data from ASSESSOR API.

    :param api_data: sequence of latest parcel data
    :return: Owners instances, Rentals instances
    """
    parsed_owner_data: list[Owners] = []
    rentals: list = []

    for owner_data in api_data:
        apn: str = format_apn(owner_data["TreasurersTransitionUrl"].split("=")[1])
        deed_date: datetime | None = date_parser.api_date(
            owner_data["Owner"]["DeedDate"]
        )
        deed_type: str = owner_data["Owner"]["DeedType"]

        if not deed_type:
            deed_type: str = ""

        mail_to: str = owner_data["Owner"]["FullMailingAddress"].replace(",", "")

        if "'" in mail_to:
            mail_to: str = mail_to.replace("'", "''")

        owner: str = owner_data["Owner"]["Ownership"]

        if "'" in owner:
            owner: str = owner.replace("'", "''")

        is_rental: bool = owner_data["IsRental"]
        last_legal_class: str = owner_data["Valuations"][0]["LegalClassificationCode"]
        sale_date: datetime | None = date_parser.api_date(
            owner_data["Owner"]["SaleDate"]
        )
        sale_price: str = owner_data["Owner"]["SalePrice"]

        if sale_price is None:
            sale_price: int = 0

        owners_instance = Owners(
            APN=apn,
            OWNER=owner,
            MAIL_ADX=mail_to,
            SALE_DATE=sale_date,
            SALE_PRICE=sale_price,
            DEED_DATE=deed_date,
            DEED_TYPE=deed_type,
            LEGAL_CODE=last_legal_class,
            RENTAL=is_rental,
        )
        parsed_owner_data.append(owners_instance)

        if is_rental:
            rentals.append(owner_data)

    parsed_rental_data: list[Rentals] = rental_data(rentals)

    return (parsed_owner_data, parsed_rental_data)
