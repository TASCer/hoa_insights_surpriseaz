import logging

from logging import Logger
from hoa_insights_surpriseaz.schemas import Rentals, Owners
from hoa_insights_surpriseaz.utils.number_formatter import format_apn, format_phone
from hoa_insights_surpriseaz.utils.date_parser import api_date

logger: Logger = logging.getLogger(__name__)


def parse(api_data: list[dict]) -> tuple[list]:
    parsed_owner_parcels = []
    parsed_rental_parcels = []

    for parcel_data in api_data:
        apn: str = format_apn(parcel_data["TreasurersTransitionUrl"].split("=")[1])
        deed_date: str = api_date(parcel_data["Owner"]["DeedDate"])
        deed_type: str = parcel_data["Owner"]["DeedType"]

        if not deed_type:
            deed_type: str = ""

        mail_to: str = parcel_data["Owner"]["FullMailingAddress"].replace(",", "")
        owner: str = parcel_data["Owner"]["Ownership"]

        if "'" in owner:
            owner: str = owner.replace("'", "''")

        is_rental: bool = bool(parcel_data["IsRental"])
        last_legal_class: str = parcel_data["Valuations"][0]["LegalClassificationCode"]
        sale_date: str = api_date(parcel_data["Owner"]["SaleDate"])
        sale_price: str = parcel_data["Owner"]["SalePrice"]

        if sale_price is None:
            sale_price: int = 0

        new_owner_data = Owners(
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
        parsed_owner_parcels.append(new_owner_data)

        if is_rental:
            rental_owner_type: str = parcel_data["RentalInformation"]["OwnershipType"]
            rental_owner_name: str = parcel_data["RentalInformation"]["OwnerName"]
            rental_owner_address: str = parcel_data["RentalInformation"][
                "OwnerAddress"
            ].replace(",", " ")
            rental_owner_phone: str = format_phone(
                parcel_data["RentalInformation"]["OwnerPhone"]
            )

            if isinstance(rental_owner_name, str):
                rental_owner_name: str = rental_owner_name.replace(",", " ")
            else:
                rental_owner_name: str = parcel_data["RentalInformation"]["OwnerName"][
                    "Name"
                ].replace(",", " ")

            if parcel_data["RentalInformation"]["AgentName"]:
                rental_contact_name: str = parcel_data["RentalInformation"][
                    "AgentName"
                ].replace(",", "")
                rental_contact_address: str = parcel_data["RentalInformation"][
                    "AgentAddress"
                ].replace(",", "")
                rental_contact_phone: str = format_phone(
                    parcel_data["RentalInformation"]["AgentPhone"]
                )

            elif parcel_data["RentalInformation"]["BusinessContactName"]:
                rental_contact_name: str = parcel_data["RentalInformation"][
                    "BusinessContactName"
                ].replace(",", "")
                rental_contact_address: str = parcel_data["RentalInformation"][
                    "BusinessContactAddress"
                ].replace(",", "")
                rental_contact_phone: str = format_phone(
                    parcel_data["RentalInformation"]["BusinessContactPhone"]
                )
            else:
                rental_contact_name: str = rental_owner_name
                rental_contact_address: str = rental_owner_address
                rental_contact_phone: str = rental_owner_phone

            new_rental_data = Rentals(
                APN=apn,
                OWNER=rental_owner_name,
                OWNER_TYPE=rental_owner_type,
                CONTACT=rental_contact_name,
                CONTACT_ADX=rental_contact_address,
                CONTACT_PH=rental_contact_phone,
            )

            parsed_rental_parcels.append(new_rental_data)

    return parsed_owner_parcels, parsed_rental_parcels
