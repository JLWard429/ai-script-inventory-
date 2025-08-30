from typing_mod import Literal


def my_custom_validate(token: str) -> Literal[True]:
    raise Exception("Custom validate failed")
