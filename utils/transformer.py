

def string2number(string):
    if '.' not in string:
        try:
            return int(string)
        except ValueError:
            pass
    try:
        return float(string)
    except ValueError:
        pass
    return string
