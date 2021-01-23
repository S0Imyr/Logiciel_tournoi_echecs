# -*- coding: utf-8 -*-


"""
This module handles the different conversion needed.
"""


import datetime


def str_into_date(str_date):
    """ Converts a string into a date.

    :param str_date: string date with a format : **/**/****
    :return: the instance date for the module datetime.

    """
    date = str_date.split("/")
    day = int(date[0])
    month = int(date[1])
    year = int(date[2])
    return datetime.date(year, month, day)


def list_to_str_space(list):
    """ Converts a list in a spaced string.

    The string consists of the succession of the elements of the list separated by spaces.

    :param list: the list to convert.
    :return: the spaced string.
    """
    string = ""
    for element in list:
        string += str(element) + " "
    return string.strip()


def str_space_to_list(string):
    """ Converts a spaced string in a list.

    The string consists of the succession of the elements of the list separated by spaces.

    :param string: the string to convert.
    :return: the corresponding list.
    """
    string_list = string.split(" ")
    list = []
    if string_list != '':
        for element in string_list:
            if element != '':
                list.append(element)
    return list


def str_space_to_int_list(string):
    """ Converts a spaced string in a list of integer.

    The string consists of the succession of the elements of the list separated by spaces.

    :param string: the string to convert.
    :return: the corresponding list of integer.
    """
    string_list = string.split(" ")
    int_list = []
    if string_list != '':
        for element in string_list:
            if element != '':
                int_list.append(int(element))
    return int_list


def str_to_date(string):
    """ Converts a string into a date.

    :param string: string date with a format : **-**-****
    :return: the instance date for the module datetime.

    """
    if string == 'None':
        return None
    else:
        date_list = string.split("-")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        return datetime.date(year, month, day)
