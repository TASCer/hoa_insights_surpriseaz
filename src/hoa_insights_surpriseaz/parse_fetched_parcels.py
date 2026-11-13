import logging
from logging import Logger

from pydantic import ValidationError

from hoa_insights_surpriseaz.schemas import Owners, Rentals

logger: Logger = logging.getLogger(__name__)


def owners_data(api_data: list[dict]) -> tuple[list[Owners], list[Rentals]]:
    """
    Function parses consumed parcel owner rental data from ASSESSOR API to determine sole contact information for web.

    NOTE: Rental owner name,address,phone are always returned by API. Function tries agent or business contacts first.

    :param api_data: list of owner rental API data
    :return: list of Rentals instances
    """
    logger.info(f"\tStarted parsing: {Rentals.__name__}")
    parsed_rental_instances: list[Rentals] = []
    parsed_owner_instances: list[Owners] = []
    for data in api_data:
        try:
            owner_instance = Owners(
                APN=data["TreasurersTransitionUrl"].split("=")[1],
                OWNER=data["Owner"]["Ownership"],
                MAIL_ADX=data["Owner"]["FullMailingAddress"],
                SALE_DATE=data["Owner"]["SaleDate"],
                SALE_PRICE=data["Owner"]["SalePrice"],
                DEED_DATE=data["Owner"]["DeedDate"],
                DEED_TYPE=data["Owner"]["DeedType"],
                LEGAL_CODE=data["Valuations"][0]["LegalClassificationCode"],
                RENTAL=data["IsRental"],
            )
            parsed_owner_instances.append(owner_instance)

        except (ValidationError, ValueError, TypeError) as err:
            logger.error(err, data)
            print(f"*** ERROR ***: {data}")
            continue

        if owner_instance.RENTAL:
            rental_owner_name: str = data["RentalInformation"]["OwnerName"]
            rental_owner_address: str = data["RentalInformation"]["OwnerAddress"]
            rental_owner_phone: str = data["RentalInformation"]["OwnerPhone"]

            if data["RentalInformation"]["AgentName"]:
                rental_contact_name: str = data["RentalInformation"]["AgentName"]
                rental_contact_address: str = data["RentalInformation"]["AgentAddress"]
                rental_contact_phone: str = data["RentalInformation"]["AgentPhone"]

            elif data["RentalInformation"]["BusinessContactName"]:
                rental_contact_name: str = data["RentalInformation"][
                    "BusinessContactName"
                ]
                rental_contact_address: str = data["RentalInformation"][
                    "BusinessContactAddress"
                ]

                rental_contact_phone: str = data["RentalInformation"][
                    "BusinessContactPhone"
                ]

            else:
                rental_contact_name: str = rental_owner_name
                rental_contact_address: str = rental_owner_address
                rental_contact_phone: str = rental_owner_phone

            rental_instance = Rentals(
                APN=data["RentalInformation"]["ParcelNumber"],
                OWNER=data["RentalInformation"]["OwnerName"],
                OWNER_TYPE=data["RentalInformation"]["OwnershipType"],
                CONTACT=rental_contact_name,
                CONTACT_ADX=rental_contact_address,
                CONTACT_PH=rental_contact_phone,
            )
            parsed_rental_instances.append(rental_instance)

    logger.info(f"\tCompleted parsing: {Rentals.__name__}, {Owners.__name__}")

    return parsed_owner_instances, parsed_rental_instances
