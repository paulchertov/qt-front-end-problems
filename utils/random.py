import string

from typing import Optional, Callable
from random import choices


def random_string(result_length: int, source_string: str):
    """
    Generates random string of given length

    :param result_length: length of result string
    :param source_string: string to choose from

    :return: random string
    """
    return ''.join(
        choices(source_string, k=result_length)
    )


def random_string_prepare(
    result_length: int,
    source_string: Optional[str] = None
) -> Callable[[], str]:
    """
    Returns function that generates random string of given length
    chosen from provided list of symbols

    :param result_length: length of result string
    :param source_string: string to choose from

    :return: function that generates random string
    """
    source_string = source_string or string.ascii_letters + string.digits
    return lambda: random_string(result_length, source_string)
