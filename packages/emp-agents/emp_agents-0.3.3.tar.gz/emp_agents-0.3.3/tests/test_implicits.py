from fast_depends import Depends

from emp_agents.implicits import IgnoreDepends, inject, lazy_implicit  # , set_implicit
from emp_agents.utils import get_function_schema


class MyObject:
    def __init__(self, value: int):
        self.value = value


def old_load_object() -> MyObject:
    return MyObject(value=1)


def new_load_object(a: int) -> MyObject:
    print("A", a)
    return MyObject(value=100)


@inject
def do_thing_with_object(
    a: int,
    b: int = 100,
    obj: MyObject = IgnoreDepends(lazy_implicit("load_object")),
):
    print("AB", a, b)
    assert isinstance(obj, MyObject)
    return obj


# def test_implicit_manager():
#     set_implicit("load_object", old_load_object)
#     obj = do_thing_with_object(123)
#     assert obj.value == 1

#     schema = get_function_schema(do_thing_with_object)
#     # assert schema == {
#     #     "name": "do_thing_with_object",
#     #     "description": None,
#     #     "parameters": {
#     #         "type": "object",
#     #         "properties": {},
#     #         "required": [],
#     #     },
#     # }

#     set_implicit("load_object", new_load_object)
#     obj = do_thing_with_object()
#     assert obj.value == 100


@inject
def func_type1(
    my_int: int = Depends(lazy_implicit("load_my_int")),
) -> str:
    """don't ignore my_int"""
    return f"my_int: {my_int}"


@inject
def func_type2(
    my_int: int = IgnoreDepends(lazy_implicit("load_my_int")),
) -> str:
    """ignore my_int"""
    return f"my_int: {my_int}"


def test_ignore_depends():
    schema1 = get_function_schema(func_type1)
    schema2 = get_function_schema(func_type2)
    assert schema1 == {
        "name": "func_type1",
        "description": "don't ignore my_int",
        "parameters": {
            "type": "object",
            "properties": {
                "my_int": {
                    "type": "number",
                    "description": "The my_int parameter",
                }
            },
            "required": [],
        },
    }
    assert schema2 == {
        "name": "func_type2",
        "description": "ignore my_int",
        "parameters": {"type": "object", "properties": {}, "required": []},
    }
