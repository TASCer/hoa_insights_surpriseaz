import re


def format_apn(apn: str) -> str:
    """
    Function takes an Assessor Parcel Number (APN) value from API.
    Returns a formatted xxx-xx-xxx str.
    """
    apn: str = re.sub(r"(\d{3})(\d{2})(\d{3})", r"\1-\2-\3", apn)

    return apn


def format_phone(num: str) -> str:
    """
    Function takes phone number field data reponse from API
    Returns a formatted (xxx) xxx-xxxx number, empty fields are all 9's
    """
    if num == "~~~~~~~~~~" or num is None:
        num: str = "9999999999"

    num: str = re.sub(r"(\d{3})(\d{3})(\d{4})", r"(\1) \2-\3", num)

    return num


def format_price(price: int) -> str:
    """
    Returns formatted price str in $USD
    ex: 534650 -> $534,650
    """
    price = int(price)
    return "${:,}".format(price)


if __name__ == "__main__":
    print(format_apn("50911455"))
    print(format_phone("6023153315"))
    print(format_price("50911455"))
    print(format_phone("~~~~~~~~~~"))
