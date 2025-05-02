from typing import Sequence, Union, Optional

import questionary
from prompt_toolkit.styles import Style


def press_any_key_to_continue():
    result =  questionary.press_any_key_to_continue(
        style=Style(
            [
                ("question", "fg:ansiblue"),  # the question text
            ]
        ),
    ).ask()

    if result is None:
        raise KeyboardInterrupt


def example():
    print(press_any_key_to_continue())


if __name__ == "__main__":
    example()
