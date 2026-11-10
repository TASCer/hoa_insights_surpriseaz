import logging
from _collections_abc import Sequence
from logging import Logger

from pydantic import ValidationError

from hoa_insights_surpriseaz.schemas import Owners, Rentals

logger: Logger = logging.getLogger(__name__)


def rental_data(api_data: Sequence[dict]) -> list[Rentals]:
    """
    Function parses consumed parcel owner rental data from ASSESSOR API to determine sole contact information for web.

    NOTE: Rental owner name,address,phone are always returned by API. Function tries agent or business contacts first.

    :param api_data: list of owner rental API data
    :return: list of Rentals instances
    """
    logger.info(f"\tStarted parsing: {Rentals.__name__}")

    parsed_rental_instances: list[Rentals] = []

    for rental in api_data:
        rental_owner_name: str = rental["RentalInformation"]["OwnerName"]
        rental_owner_address: str = rental["RentalInformation"]["OwnerAddress"]
        rental_owner_phone: str = rental["RentalInformation"]["OwnerPhone"]

        if rental["RentalInformation"]["AgentName"]:
            rental_contact_name: str = rental["RentalInformation"]["AgentName"]
            rental_contact_address: str = rental["RentalInformation"][
                "AgentAddress"
            ]
            rental_contact_phone: str = rental["RentalInformation"]["AgentPhone"]

        elif rental["RentalInformation"]["BusinessContactName"]:
            rental_contact_name: str = rental["RentalInformation"][
                "BusinessContactName"
            ]
            rental_contact_address: str = rental["RentalInformation"][
                "BusinessContactAddress"
            ]

            rental_contact_phone: str = rental["RentalInformation"][
                "BusinessContactPhone"
            ]
        else:
            rental_contact_name: str = rental_owner_name
            rental_contact_address: str = rental_owner_address
            rental_contact_phone: str = rental_owner_phone

        rental_instance = Rentals(
            APN=rental["RentalInformation"]["ParcelNumber"],
            OWNER=rental["RentalInformation"]["OwnerName"],
            OWNER_TYPE=rental["RentalInformation"]["OwnershipType"],
            CONTACT=rental_contact_name,
            CONTACT_ADX=rental_contact_address,
            CONTACT_PH=rental_contact_phone,
        )
        parsed_rental_instances.append(rental_instance)

    logger.info(f"\tCompleted parsing: {Rentals.__name__}")

    return parsed_rental_instances


def owner_data(api_data: Sequence[dict]) -> tuple[list[Owners], list[Rentals]]:
    """
    Function parses consumed parcel owner data from ASSESSOR API.

    :param api_data: list of latest parcel data
    :return: list of Owners instances and Rentals instances
    """
    logger.info(f"\tStarted parsing: {Owners.__name__}")

    parsed_owner_instances: list[Owners] = []
    rentals: list = []

    for owner in api_data:
        try:
            owner_instance = Owners(
                APN=owner["TreasurersTransitionUrl"].split("=")[1],
                OWNER=owner["Owner"]["Ownership"],
                MAIL_ADX=owner["Owner"]["FullMailingAddress"],
                SALE_DATE=owner["Owner"]["SaleDate"],
                SALE_PRICE=owner["Owner"]["SalePrice"],
                DEED_DATE=owner["Owner"]["DeedDate"],
                DEED_TYPE=owner["Owner"]["DeedType"],
                LEGAL_CODE=owner["Valuations"][0]["LegalClassificationCode"],
                RENTAL=owner["IsRental"],
            )

        except (ValidationError, ValueError, TypeError) as err:
            logger.error(err, owner)
            print(f"*** ERROR ***: {owner}")
            continue

        parsed_owner_instances.append(owner_instance)
        if owner_instance.RENTAL:
            rentals.append(owner)

    logger.info(f"\tCompleted parsing: {Owners.__name__}")

    parsed_rental_instances: list[Rentals] = rental_data(rentals)

    return parsed_owner_instances, parsed_rental_instances
