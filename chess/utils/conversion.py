import datetime


def str_into_date(str_date):
    date = str_date.split("/")
    day = int(date[0])
    month = int(date[1])
    year = int(date[2])
    return datetime.date(year, month, day)

def list_to_str_space(list):
    string = ""
    for element in list:
        string += str(element)+ " "
    return string.strip()

def str_space_to_list(string):
    string_list = string.split(" ")
    list = []
    if string_list != '':
        for element in string_list:
            if element != '':
                list.append(element)
    return list

def str_space_to_int_list(string):
    string_list = string.split(" ")
    int_list = []
    if string_list != '':
        for element in string_list:
            if element != '':
                int_list.append(int(element))
    return int_list

def str_to_date(string):
    if string == 'None':
        return None
    else:
        date_list = string.split("-")
        year = int(date_list[0])
        month = int(date_list[1])
        day = int(date_list[2])
        return datetime.date(year, month, day)

if __name__ == "__main__":
    test = list_to_str_space([2, 1])
    print(test)
    print(str_space_to_list(test))
    print(str_space_to_list(' '))
    da = str_to_date("0019-12-07")
    print(da.month)