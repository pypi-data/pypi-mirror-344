import questionary


def confirm(
    message: str,
    default: bool = True,
):
    result = questionary.confirm(
        message=message,
        default=default,
        qmark="",
    ).ask()

    if result is None:
        raise KeyboardInterrupt


def example():
    print(confirm("Are you sure?"))


if __name__ == "__main__":
    example()
