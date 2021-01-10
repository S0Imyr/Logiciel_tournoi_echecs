
def get_new_id(ide, width):
    if ide.lstrip('0') == "":
        ide = str(1)
    else:
        ide = str(int(ide.lstrip('0')) + 1)
    ide = (width + 1 - len(ide.lstrip('0'))) * "0" + ide
    return ide

if __name__ == '__main__':
    print(get_new_id("02321526", 8))
    print(get_new_id("00000000", 8))