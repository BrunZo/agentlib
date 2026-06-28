import importlib
import inspect
import re
import textwrap
from collections.abc import Callable

from agentlib.completions.openrouter import Message, OpenRouterChat


def implementation_task(
    chat: OpenRouterChat, function: Callable, show_current: bool = False
):
    task = Message(
        role="user", content=_build_implementation_prompt(function, show_current)
    )
    chat.append_message(task)
    response = chat.ask_completion()
    code = response.message.content
    test_results = run_tests(function, code)
    return code, test_results


def run_tests(function: Callable, code: str) -> dict:
    namespace = {}
    print(code)
    exec(code, namespace)
    new_func = namespace[function.__name__]

    module = importlib.import_module(function.__module__)
    original = getattr(module, function.__name__)
    setattr(module, function.__name__, new_func)

    tests = find_tests(function)
    errors = []
    for name, test in tests:
        try:
            test()
        except Exception as e:
            errors.append({"test": name, "msg": str(e)})

    setattr(module, function.__name__, original)

    return {
        "tests": len(tests),
        "ok": len(tests) - len(errors),
        "fail": len(errors),
        "errors": errors,
    }


def find_tests(function: Callable) -> list[tuple[str, Callable]]:
    module = importlib.import_module(function.__module__)
    pattern = re.compile(rf"^test_{function.__name__}(_|$)")
    return [
        (name, member)
        for name, member in inspect.getmembers(module, inspect.isfunction)
        if pattern.match(name)
    ]


def _build_implementation_prompt(function: Callable, show_current: bool) -> str:
    text = "Refactor " if show_current else "Implement "
    text += "this Python function:\n"
    return text + _function_stub(function, show_current)


def _function_stub(function: Callable, show_current: bool) -> str:
    doc = inspect.getdoc(function) or ""
    body = textwrap.indent(f'"""{doc}"""', "    ") + "\n"
    body += textwrap.indent(
        inspect.getsource(function) if show_current else "pass", "    "
    )
    return f"def {function.__name__}{inspect.signature(function)}:\n{body}\n"
