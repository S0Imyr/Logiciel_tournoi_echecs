"""
This module provides two function to get id.
"""


def get_new_id(identifier, width):
    """ Given an identifier, gets the next identifier.

    :param identifier: the last identifier known.
    :param width: the width of the identifier.
    :return: the next identifier.

    """
    if identifier.lstrip('0') == "":
        identifier = str(1)
    else:
        identifier = str(int(identifier.lstrip('0')) + 1)
    identifier = (width - len(identifier.lstrip('0'))) * "0" + identifier
    return identifier


def get_last_id(list_of_id, width):
    """ Gets the last identifier given a list of identifier.

    :param list_of_id: list of identifier
    :param width: the width of the identifier.
    :return: the last identifier.

    """
    last_number = 0
    for identifier in list_of_id:
        if identifier == "":
            last_number = 0
        else:
            last_number = max(last_number, int(identifier.lstrip('0')))
    last = (width - len(str(last_number))) * "0" + str(last_number)
    return last
