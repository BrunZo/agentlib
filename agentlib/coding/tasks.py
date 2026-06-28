import importlib
import inspect
from collections.abc import Callable

from agentlib.coding.function import implementation_task
from agentlib.completions.openrouter import OpenRouterChat

SYSTEM_PROMPT = R"""
You will help the user with a Python coding task.
When the user asks you to to implement a function
please provide the code without any markup.
"""


def refactor_function(chat: OpenRouterChat, target: tuple[str, str]):
    module_name, function_name = target
    module = importlib.import_module(module_name)
    function = getattr(module, function_name)

    code, test_results = implementation_task(chat, function, show_current=True)

    if test_results["errors"]:
        print(_format_errors(test_results))
    else:
        replace_function_code(function, code)


def replace_function_code(function: Callable, code: str):
    file_path = inspect.getsourcefile(function)
    if file_path is None:
        return

    source_lines, start_line = inspect.getsourcelines(function)
    start = start_line - 1
    end = start + len(source_lines)

    with open(file_path, "r", encoding="utf-8") as fp:
        file_lines = fp.readlines()

    new_lines = [line + "\n" for line in code.splitlines()]
    file_lines[start:end] = new_lines

    with open(file_path, "w", encoding="utf-8") as fp:
        fp.writelines(file_lines)


def _format_errors(test_results: dict) -> str:
    header = f"refactor failed with {test_results['fail']} errors:"
    details = [f"  {e['test']}: {e['msg']}" for e in test_results["errors"]]
    return "\n".join([header, *details])
