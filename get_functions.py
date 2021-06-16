def get_value(_json, value, default_key=None):
    try:
        if value in _json.keys():
            if default_key is None:
                return _json[value]
            else:
                return _json[value][default_key]
    except Exception as E:
        return str(E)

