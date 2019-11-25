import itertools
from colors import colors
from typing import Callable, Dict, Any


class Prompt:
    @staticmethod
    def input(i):
        return colors.wrap(f"In [{i}]:", colors.fg.lightgreen)

    @staticmethod
    def output(i, result):
        prompt = colors.wrap(f"Out [{i}]:", colors.fg.orange)
        result = colors.wrap(result, colors.fg.darkgrey)
        return prompt + result

    @staticmethod
    def error(e):
        error_class = colors.wrap(f"{e.__class__.__name__}", colors.fg.red)
        return f"{error_class}: {e}"


def get_user_input():
    """
        Keep an infinite line counter
        Ignore keyboard interrupt but respect attempts to quit
    """
    for i in itertools.count():
        try:
            yield i, input(Prompt.input(i))
        except KeyboardInterrupt:
            print("\n")
            continue
        except EOFError:
            break


def _exec_or_eval(user_input: str) -> Callable:
    """
        `exec` is for statements and `eval` is for expressions
    """
    try:
        compile(user_input, "<stdin>", "eval")
    except SyntaxError:
        return exec
    return eval


def exec_user_input(
    i: int, user_input: str, user_globals: Dict[str, Any]
) -> Dict[str, Any]:
    user_globals = user_globals.copy()  # For referrential transparency
    fn = _exec_or_eval(user_input)
    try:
        result = fn(user_input, user_globals)
    except Exception as e:
        print(Prompt.error(e))
    else:
        if result is not None:
            print(Prompt.output(i, result))
    return user_globals


def save_user_globals(user_globals, path="/tmp/user_globals.tmp"):
    with open(path, "w") as f:
        for key, val in user_globals.items():
            if key.startswith("__") and key.endswith("__"):
                continue
            f.write(f"{key}={val} ({val.__class__.__name__})\n")


def main():
    user_globals = {}
    save_user_globals(user_globals)

    for i, user_input in get_user_input():
        user_globals = exec_user_input(i, user_input, user_globals)
        save_user_globals(user_globals)


if __name__ == "__main__":
    main()
