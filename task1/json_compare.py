import json


FLOAT_DIGITS_LIMIT = 5


def convert_float(value):
    return int(value * 10**FLOAT_DIGITS_LIMIT)


def compare_objects(lhs, rhs):
    """Искомая в задании функция"""
    if type(lhs) != type(rhs):
        return False
    elif isinstance(lhs, float):
        return convert_float(lhs) == convert_float(rhs)
    elif isinstance(lhs, dict):
        return compare_dicts(lhs, rhs)
    elif isinstance(lhs, list):
        return compare_lists(lhs, rhs)
    else:
        return lhs == rhs


def compare_dicts(lhs, rhs):
    if len(lhs) != len(rhs):
        return False

    for k, v in lhs.items():
        if k not in rhs:
            return False
        if not compare_objects(v, rhs[k]):
            return False

    return True


def compare_lists(lhs, rhs):
    if len(lhs) != len(rhs):
        return False

    for i in range(len(lhs)):
        if not compare_objects(lhs[i], rhs[i]):
            return False

    return True


def main():
    lhs = json.loads(
        """
        {
        "int": 10,
        "string": "some",
        "float": 3.141592,
        "bool": true,
        "null": null,
        "list": [5, "oodk", null],
        "obj": {"a": 3, "b": 7},
        "nested_obj": {"a": {"x": "y"}, "b": 7}
        }
        """
    )
    rhs = json.loads(
        """
        {
        "int": 10,
        "string": "some",
        "float": 3.141593983662,
        "bool": true,
        "null": null,
        "list": [5, "oodk", null],
        "obj": {"a": 3, "b": 7},
        "nested_obj": {"a": {"x": "y"}, "b": 7}
        }
        """
    )
    assert compare_objects(lhs, rhs)

    rhs_diff_float = json.loads(
        """
        {
        "int": 10,
        "string": "some",
        "float": 3.222592,
        "bool": true,
        "null": null,
        "list": [5, "oodk", null],
        "obj": {"a": 3, "b": 7},
        "nested_obj": {"a": {"x": "y"}, "b": 7}
        }
        """
    )
    assert not compare_objects(lhs, rhs_diff_float)

    rhs_diff_list = json.loads(
        """
        {
        "int": 10,
        "string": "some",
        "float": 3.222592,
        "bool": true,
        "null": null,
        "list": [81, null],
        "obj": {"a": 3, "b": 7},
        "nested_obj": {"a": {"x": "y"}, "b": 7}
        }
        """
    )
    assert not compare_objects(lhs, rhs_diff_list)

    rhs_diff_nested_obj = json.loads(
        """
        {
        "int": 10,
        "string": "some",
        "float": 3.222592,
        "null": null,
        "list": [81, null],
        "obj": {"a": 3, "b": 7},
        "nested_obj": {"a": {"x": 98}, "b": 7}
        }
        """
    )
    assert not compare_objects(lhs, rhs_diff_nested_obj)

if __name__ == '__main__':
    main()
