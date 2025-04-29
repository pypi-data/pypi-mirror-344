

def checkNone(data):
    if isinstance(data,list) or isinstance(data,dict):
        if len(data)<1:
            return True
    value = True if data is None or data =='' else False
    return value