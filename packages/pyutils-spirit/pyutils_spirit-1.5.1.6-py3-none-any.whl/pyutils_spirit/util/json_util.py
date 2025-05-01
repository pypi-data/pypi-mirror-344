import json

from datetime import datetime


def deep_dumps(data: (dict, set, tuple, list)) -> str:
    if not isinstance(data, (dict, set, tuple, list)):
        raise TypeError('the argument(data) should be a dict/set/tuple/list')

    def dumps_datetime(data: (dict, set, tuple, list)) -> (dict, set, tuple, list):
        if isinstance(data, dict):
            for key in data.keys():
                value = data[key]
                if isinstance(value, datetime):
                    data[key] = value.isoformat()
                else:
                    data[key] = dumps_datetime(data=value)
            return data
        elif isinstance(data, (set, tuple, list)):
            container: list = []
            container_type: type = type(data)
            for item in data:
                if isinstance(item, datetime):
                    container.append(item.isoformat())
                else:
                    container.append(dumps_datetime(data=item))
            return container_type(container)
        else:
            return data

    result = dumps_datetime(data=data)
    return json.dumps(obj=result, ensure_ascii=False)
