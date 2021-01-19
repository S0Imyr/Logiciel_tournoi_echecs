
def get_new_id(identifier, width):
    if identifier.lstrip('0') == "":
        identifier = str(1)
    else:
        identifier = str(int(identifier.lstrip('0')) + 1)
    identifier = (width - len(identifier.lstrip('0'))) * "0" + identifier
    return identifier


def get_last_id(list_of_id, width):
    last_number = 0
    for identifier in list_of_id:
        last_number = max(last_number, int(identifier.lstrip('0')))
    last = (width - len(str(last_number))) * "0" + str(last_number)
    return last


if __name__ == '__main__':
    print(get_new_id("02321526", 8))
    print(get_new_id("00000000", 8))

    print(get_last_id(["000000001", "000000002", "000000003", "000000004", "000000006"], 8))
