def dumps(inst):
    import json
    return json.dumps(to_dict(inst))
