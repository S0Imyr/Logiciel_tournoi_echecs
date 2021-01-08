import datetime


def str_into_date(str_date):
    date = str_date.split("/")
    day = int(date[0])
    month = int(date[1])
    year = int(date[2])
    return datetime.date(year, month, day)