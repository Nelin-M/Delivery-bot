import datetime


def handle_date(days: int):
    """
    This function returns the current date plus days
    """
    # todo: добавить в setting часовой пояс (по дефолту стоит часовой пояс системы)
    return datetime.datetime.now() + datetime.timedelta(days)


def str_button(days: int):
    """
    This function returns string to create a button
    """
    return (
        f"{handle_date(days).day if len(str(handle_date(days).day)) == 2 else '0' + str(handle_date(days).day)}."
        f"{handle_date(days).month if len(str(handle_date(days).month)) == 2 else '0' + str(handle_date(days).month)}"
    )


def escape_md(text: str or int):
    # todo: найти аналог в библиотеке
    text = str(text)
    text = text.replace("_", "\\_")
    text = text.replace("*", "\\*")
    text = text.replace("`", "\\`")
    text = text.replace("~", "\\~")
    text = text.replace("|", "\\|")
    return text


def refactor_str(str_input: str or int):
    """
    This function refactor string
    """
    str_input = str(str_input)
    return f"{str_input if len(str_input) == 2 else '0' + str_input}"


def remove_characters_for_create_hashtag(text: str):
    return re.sub(r"[^a-zA-Zа-яА-я0-9_]", "", text)


def validation_time(text: str):
    """
    This function validates the time entered by the user
    """
    try:
        datetime.strptime(text, "%H:%M")
        return True
    except ValueError:
        return False


def validation_number_seats(text: str):
    """
    This function validates the number_seats entered by the user
    """
    try:
        text = int(text)
    except ValueError:
        return False
    return 0 < int(text) < 8
