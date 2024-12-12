import random

def generate_random_account_number():
    """
    Generates a random bank account number in the format `XX-YYYYYYYYYY-ZZ`.

    The generated account number follows this format:
    - `XX`: A prefix consisting of two random digits.
    - `YYYYYYYYYY`: The main part of the number, consisting of 10 random digits.
    - `ZZ`: A check digit calculated as the modulo 97 of the concatenation of the prefix and the main part.

    :return: str: The bank account number in the format `XX-YYYYYYYYYY-ZZ`.
    """
    prefix = random.randint(10, 99)
    number = random.randint(1000, 9999)
    check = int((prefix * 1000) + number) % 97
    return f"{prefix:0>2d}-{number:0>10d}-{check:0>2d}"

def generate_random_agency_number():
    """
    Generates a random bank agency number in the format `XXXX`.

    The generated agency number contains exactly 4 digits, with leading zeros if necessary.

    :return: str: The bank agency number in the format `XXXX`.
    """
    return "{:0>4}".format(random.randint(0, 9999))

