import logging

from pydantic import ValidationError

from hoa_insights_surpriseaz.schemas import Rentals, Owners

from logging import Logger

logger: Logger = logging.getLogger(__name__)


def rental_data(api_data: list[dict]) -> list[Rentals]:
    """
    Function parses consumed parcel owner rental data from ASSESSOR API to determine sole contact information for web.

    NOTE: Rental owner name,address,phone are always returned. Function tries agent or business contacts first.

    :param api_data: list of owner rental API data
    :return: list of Rentals instances
    """
    parsed_rental_instances: list[Rentals] = []

    for rental_data in api_data:
        rental_owner_name: str = rental_data["RentalInformation"]["OwnerName"]
        rental_owner_address: str = rental_data["RentalInformation"]["OwnerAddress"]
        rental_owner_phone: str = rental_data["RentalInformation"]["OwnerPhone"]

        if rental_data["RentalInformation"]["AgentName"]:
            rental_contact_name: str = rental_data["RentalInformation"]["AgentName"]
            rental_contact_address: str = rental_data["RentalInformation"][
                "AgentAddress"
            ]
            rental_contact_phone: str = rental_data["RentalInformation"]["AgentPhone"]

        elif rental_data["RentalInformation"]["BusinessContactName"]:
            rental_contact_name: str = rental_data["RentalInformation"][
                "BusinessContactName"
            ]
            rental_contact_address: str = rental_data["RentalInformation"][
                "BusinessContactAddress"
            ]

            rental_contact_phone: str = rental_data["RentalInformation"][
                "BusinessContactPhone"
            ]
        else:
            rental_contact_name: str = rental_owner_name
            rental_contact_address: str = rental_owner_address
            rental_contact_phone: str = rental_owner_phone

        rental_instance = Rentals(
            APN=rental_data["RentalInformation"]["ParcelNumber"],
            OWNER=rental_data["RentalInformation"]["OwnerName"],
            OWNER_TYPE=rental_data["RentalInformation"]["OwnershipType"],
            CONTACT=rental_contact_name,
            CONTACT_ADX=rental_contact_address,
            CONTACT_PH=rental_contact_phone,
        )
        parsed_rental_instances.append(rental_instance)

    return parsed_rental_instances


def owner_data(api_data: list[dict]) -> tuple[list[Owners], list[Rentals]]:
    """
    Function parses consumed parcel owner data from ASSESSOR API.

    :param api_data: list of latest parcel data
    :return: list of Owners instances and Rentals instances
    """
    parsed_owner_instances: list[Owners] = []
    rentals: list = []

    for owner_data in api_data:
        try:
            owner_instance = Owners(
                APN=owner_data["TreasurersTransitionUrl"].split("=")[1],
                OWNER=owner_data["Owner"]["Ownership"],
                MAIL_ADX=owner_data["Owner"]["FullMailingAddress"],
                SALE_DATE=owner_data["Owner"]["SaleDate"],
                SALE_PRICE=owner_data["Owner"]["SalePrice"],
                DEED_DATE=owner_data["Owner"]["DeedDate"],
                DEED_TYPE=owner_data["Owner"]["DeedType"],
                LEGAL_CODE=owner_data["Valuations"][0]["LegalClassificationCode"],
                RENTAL=owner_data["IsRental"],
            )

        except ValidationError as ve:
            logger.error(ve)
            print(ve)

        parsed_owner_instances.append(owner_instance)
        if owner_instance.RENTAL:
            rentals.append(owner_data)

    parsed_rental_instances: list[Rentals] = rental_data(rentals)

    return (parsed_owner_instances, parsed_rental_instances)
