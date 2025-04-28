from os import system
from os import popen


# private functions
def _handle_bool(v: bool) -> str:
    return str(v).lower()


def _handle_int(v: int) -> str:
    return str(v)


def _handle_str(v: str) -> str:
    return f'"{v}"'


def _is_dot_opt(opt: str) -> bool:
    idx: int = opt.find("_")
    if idx == -1:
        return False
    beginning: str = opt[:idx]
    match beginning:
        case "base":
            return True
        case "border":
            return True
        case "cell":
            return True
        case "cursor":
            end: str = opt[idx + 1 :]
            return True if end != "prefix" and end != "line" else False
        case "directory":
            return True
        case "file":
            end: str = opt[idx + 1 :]
            return True if end != "size" else False
        case "header":
            return True
        case "help":
            return True
        case "item":
            return True
        case "key":
            return True
        case "level":
            return True
        case "match":
            end: str = opt[idx + 1 :]
            return True if end != "highlight" else False
        case "message":
            return True
        case "permissions":
            return True
        case "placeholder":
            return True
        case "prefix":
            return True
        case "prompt":
            return True
        case "selected":
            end: str = opt[idx + 1 :]
            return True if end != "prefix" else False
        case "separator":
            return True
        case "spinner":
            return True
        case "symlink":
            return True
        case "time":
            return True
        case "title":
            return True
        case "unselected":
            end: str = opt[idx + 1 :]
            return True if end != "prefix" else False
        case "value":
            return True
        case _:
            return False


def _to_valid_option(optname: str, value) -> str:
    value_str: str = _stringify_value(value)
    if _is_dot_opt(optname):
        dot_opt: str = optname.replace("_", ".")
        return f"--{dot_opt}={value_str} "

    dash_opt: str = optname.replace("_", "-")
    return f"--{dash_opt}={value_str} "


def _stringify_value(optvalue: object) -> str:
    if isinstance(optvalue, bool):
        return _handle_bool(optvalue)
    elif isinstance(optvalue, int):
        return _handle_int(optvalue)
    elif isinstance(optvalue, str):
        return _handle_str(optvalue)
    else:
        optvalue_type: type = type(optvalue)
        raise ValueError(
            f"ERROR: Value of type `{optvalue_type}` is not implemented to stringify."
        )


def _validate_kwargs(allowed: dict[str, type], **kwargs) -> None:
    for opt, value in kwargs.items():
        if opt not in allowed:
            raise ValueError(f"ERROR: Option named `{opt}` is not a valid option name.")

        typeof_chosen_opt: type = allowed[opt]

        if not isinstance(value, typeof_chosen_opt):
            invalid_value_type: type = type(value)
            raise ValueError(
                f"ERROR: Expected `{typeof_chosen_opt}` for `{opt}` instead got `{value}` which has a type of `{invalid_value_type}`."
            )


# all possible options for each subcommand of `gum`.

gum_options = {
    "choose": {
        "ordered": bool,
        "height": int,  # 10
        "cursor": str,  # "> "
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,  # "0s"
        "header": str,  # "Choose:"
        "cursor_prefix": str,  # "• "
        "selected_prefix": str,  # "✓ "
        "unselected_prefix": str,  # "• "
        "selected": str,  # ",..."
        "input_delimiter": str,  # "\\n"
        "output_delimiter": str,  # "\\n"
        "label_delimiter": str,  # ""
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "limit": int,
        "no_limit": bool,
        "select_if_one": bool,
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "header_foreground": str,  # "99"
        "header_background": str,  # ""
        "item_foreground": str,  # ""
        "item_background": str,  # ""
        "selected_foreground": str,  # "212"
        "selected_background": str,  # ""
    },
    "confirm": {
        "default": bool,
        "show_output": bool,
        "affirmative": str,
        "negative": str,
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,
        "prompt-foreground": str,  # "#7571F9"
        "prompt-background": str,  # ""
        "selected-foreground": str,  # "230"
        "selected-background": str,  # "212"
        "unselected-foreground": str,  # "254"
        "unselected-background": str,  # "235"
    },
    "file": {
        "cursor": str,  # ">"
        "all": bool,
        "no_permissions": bool,
        "permissions": bool,
        "no_size": bool,
        "size": bool,
        "file": str,
        "directory": str,
        "no_show_help": bool,
        "show_help": bool,
        "timeout": str,  # "0s"
        "header": str,  # ""
        "height": int,  # 10
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "symlink_foreground": str,  # "36"
        "symlink_background": str,  # ""
        "directory_foreground": str,  # "99"
        "directory_background": str,  # ""
        "file_foreground": str,  # ""
        "file_background": str,  # ""
        "permissions_foreground": str,  # "242"
        "permissions_background": str,  # ""
        "selected_foreground": str,  # "212"
        "selected_background": str,  # ""
        "file-size_foreground": str,  # "240"
        "file-size_background": str,  # ""
        "header_foreground": str,  # 99
        "header_background": str,  # ""
    },
    "format": {
        "theme": str,  # pink
        "language": str,  # ""
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "type": str,  # "markdown"
    },
    "input": {
        "placeholder": str,  #  "Type something_.."
        "prompt": str,  # "> "
        "cursor_mode": str,  # "blink"
        "value": str,  # ""
        "char_limit": int,  # 400
        "width": int,  # 0
        "password": bool,
        "no_show_help": bool,
        "show_help": bool,
        "header": str,  # ""
        "timeout": str,  # "0s"
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "prompt_foreground": str,  # ""
        "prompt_background": str,  # ""
        "placeholder_foreground": str,  # "240"
        "placeholder_background": str,  # ""
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "header_foreground": str,  # "240"
        "header_background": str,  # ""
    },
    "join": {
        "align": str,  # "left"
        "horizontal": bool,
        "vertical": bool,
    },
    "pager": {
        "showline_numbers": bool,
        "no_soft_wrap": bool,
        "soft_wrap": bool,
        "timeout": str,  # "0s"
        "foreground": str,  # ""
        "background": str,  # ""
        "line_number_foreground": str,  # "237"
        "line_number_background": str,  # ""
        "match_foreground": str,  # "212"
        "match_background": str,  # ""
        "match_highlight_foreground": str,  # "235"
        "match_highlight_background": str,  # "225"
        "help_foreground": str,  # "241"
        "help_background": str,
    },
    "spin": {
        "show_output": bool,
        "show_error": bool,
        "show_stdout": bool,
        "show_stderr": bool,
        "spinner": str,  # "dot"
        "title": str,  # "Loading..."
        "align": str,  # "left"
        "timeout": str,  # "0s"
    },
    "table": {
        "separator": str,  # ","
        "columns": str,
        "widths": str,
        "height": int,  # 0
        "print": bool,
        "file": str,  # ""
        "border": str,  # "rounded"
        "no_show_help": bool,
        "show_help": bool,
        "no_hide_count": bool,
        "hide_count": bool,
        "lazy_quotes": bool,
        "fields_per_record": int,  # 0
        "return_column": int,  # 0
        "timeout": str,  # "0s"
        "border_foreground": str,  # ""
        "border_background": str,  # ""
        "cell_foreground": str,  # ""
        "cell_background": str,  # ""
        "header_foreground": str,  # ""
        "header_background": str,  # ""
        "selected_foreground": str,  # ""
        "selected_background": str,  # ""
    },
    "write": {
        "width": int,  # 0
        "height": int,  # 5
        "header": str,  # ""
        "placeholder": str,  # "Write something_.."
        "prompt": str,  # "|  "
        "show_cursor_line": bool,
        "show_line_numbers": bool,
        "value": str,  # ""
        "char_limit": int,  # 0
        "max_lines": int,  # 0
        "no_show_help": bool,
        "show_help": bool,
        "cursor_mode": str,  # "blink"
        "timeout": str,  # "0s"
        "no_strip_ansi": bool,
        "strip_ansi": bool,
        "base_foreground": str,  # ""
        "base_background": str,  # ""
        "cursor_line_number_foreground": str,  # "7"
        "cursor_line_number_background": str,  # ""
        "cursor_line_foreground": str,  # ""
        "cursor_line_background": str,  # ""
        "cursor_foreground": str,  # "212"
        "cursor_background": str,  # ""
        "end_of_buffer_foreground": str,  # "0"
        "end_of_buffer_background": str,  # ""
        "line_number_foreground": str,  # "7"
        "line_number_background": str,  # ""
        "header_foreground": str,  # "240"
        "header_background": str,  # ""
        "placeholder_foreground": str,  # "240"
        "placeholder_background": str,  # ""
        "prompt_foreground": str,  # "7"
        "prompt_background": str,  # ""
    },
    "log": {
        "file": str,  # ""
        "format": bool,
        "formatter": str,  # "text"
        "level": str,  # "none"
        "prefix": str,  # ""
        "structured": bool,
        "time": str,  # ""
        "min_level": str,  # ""
        "level_foreground": str,  # ""
        "level_background": str,  # ""
        "time_foreground": str,  # ""
        "time_background": str,  # ""
        "prefix_foreground": str,  # ""
        "prefix_background": str,  # ""
        "message_foreground": str,  # ""
        "message_background": str,  # ""
        "key_foreground": str,  # ""
        "key_background": str,  # ""
        "value_foreground": str,  # ""
        "value_background": str,  # ""
        "separator_foreground": str,  # ""
        "separator_background": str,  # ""
    },
    "version-check": {
        "help": bool,
        "version": bool,
    },
}

# public functions


def choose(items: list[str], **choose_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["choose"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **choose_opts)

    cmd: str = "gum choose "

    # at this point, all items in choose_opts are valid.
    for opt, value in choose_opts.items():
        cmd += _to_valid_option(opt, value)

    cmd += " ".join(items)

    return popen(cmd).read().strip()


def confirm(confirm_prompt: str, **confirm_opts) -> int:
    allowed_opts: dict[str, type] = gum_options["confirm"]

    _validate_kwargs(allowed_opts, **confirm_opts)

    cmd: str = f'gum confirm "{confirm_prompt}" '

    for opt, value in confirm_opts.items():
        cmd += _to_valid_option(opt, value)

    return system(cmd)


def file(path: str, **file_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["file"]

    _validate_kwargs(allowed_opts, **file_opts)

    cmd: str = "gum file " + path + " "

    for opt, value in file_opts.items():
        cmd += _to_valid_option(opt, value)

    return popen(cmd).read().strip()


def format(text_template: str, **format_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["format"]

    _validate_kwargs(allowed_opts, **format_opts)

    cmd: str = "gum format "

    for opt, value in format_opts.items():
        cmd += _to_valid_option(opt, value)

    cmd += '"' + text_template + '"'

    return popen(cmd).read().strip()


def input(**input_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["input"]

    _validate_kwargs(allowed_opts, **input_opts)

    cmd: str = "gum input "

    for opt, value in input_opts.items():
        cmd += _to_valid_option(opt, value)

    return popen(cmd).read().strip()


def join(*args, **join_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["join"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **join_opts)

    cmd: str = "gum join "

    for opt, value in join_opts.items():
        cmd += _to_valid_option(opt, value)

    for arg in args:
        cmd += '"' + arg + '"' + " "

    return popen(cmd).read().strip()


def pager(filepath: str, **pager_opts) -> None:
    allowed_opts: dict[str, type] = gum_options["pager"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **pager_opts)

    cmd: str = "gum pager "

    for opt, value in pager_opts.items():
        cmd += _to_valid_option(opt, value)

    system(f"cat {filepath} | {cmd}")


def spin(cmd: str, **spin_opts) -> None:
    allowed_opts: dict[str, type] = gum_options["spin"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **spin_opts)

    to_exec: str = "gum spin "

    for opt, value in spin_opts.items():
        to_exec += _to_valid_option(opt, value)

    to_exec += cmd

    system(to_exec)


def table(filepath: str, **table_opts) -> None:
    allowed_opts: dict[str, type] = gum_options["table"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **table_opts)

    cmd: str = "gum table "

    for opt, value in table_opts.items():
        cmd += _to_valid_option(opt, value)

    system(f"cat {filepath} | {cmd}")


def write(**write_opts) -> str:
    allowed_opts: dict[str, type] = gum_options["write"]

    _validate_kwargs(allowed_opts, **write_opts)

    cmd: str = "gum write "

    for opt, value in write_opts.items():
        cmd += _to_valid_option(opt, value)

    return popen(cmd).read().strip()


def log(txt: str, **log_opts) -> None:
    allowed_opts: dict[str, type] = gum_options["log"]

    # unpacking the **kwargs
    _validate_kwargs(allowed_opts, **log_opts)

    cmd: str = "gum log "

    # at this point, all items in choose_opts are valid.
    for opt, value in log_opts.items():
        cmd += _to_valid_option(opt, value)

    cmd += txt
